"""Evidence audit: quote check, agreement, and the pre-registered tests H1-H5.

Usage: python3 analyze.py codes.jsonl [second_pass.jsonl]
Every number in the paper comes from this script's output.
"""
import json, re, sys, os, math, random
from statistics import median

# Folder holding papers.jsonl and the extracted full texts (text_path in each
# record). The texts are not redistributed here; see the README.
CORPUS = os.path.expanduser(os.environ.get("EVIDENCE_AUDIT_CORPUS", "corpus"))
norm = lambda s: re.sub(r"\s+", " ", s or "").strip().lower()

def load(p):
    return [json.loads(l) for l in open(p) if l.strip()]

def text_of(pid):
    rows = {json.loads(l)["id"]: json.loads(l) for l in open(f"{CORPUS}/papers.jsonl")}
    return norm(open(f"{CORPUS}/{rows[pid]['text_path']}", errors="ignore").read())

def quote_check(codes):
    bad = []
    for c in codes:
        t = text_of(c["id"])
        for f, q in (c.get("quotes") or {}).items():
            if q and norm(q) not in t:
                bad.append((c["id"], f, q[:80]))
    return bad

def spearman(x, y):
    def rank(v):
        o = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
        while i < len(v):
            j = i
            while j + 1 < len(v) and v[o[j + 1]] == v[o[i]]: j += 1
            for k in range(i, j + 1): r[o[k]] = (i + j) / 2 + 1
            i = j + 1
        return r
    rx, ry = rank(x), rank(y); n = len(x)
    mx, my = sum(rx) / n, sum(ry) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    return cov / math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))

def perm_p_spearman_neg(x, y, n=20000, seed=7):
    rho = spearman(x, y); rnd = random.Random(seed); ys = list(y); k = 0
    for _ in range(n):
        rnd.shuffle(ys); k += spearman(x, ys) <= rho
    return rho, (k + 1) / (n + 1)

def mw_p_less(a, b, n=20000, seed=7):
    """One-sided permutation test that a's median-rank is below b's (Mann-Whitney U)."""
    def u(a, b): return sum((x > y) + 0.5 * (x == y) for x in a for y in b)
    obs = u(a, b); pool = a + b; rnd = random.Random(seed); k = 0
    for _ in range(n):
        rnd.shuffle(pool); k += u(pool[:len(a)], pool[len(a):]) <= obs
    return obs, (k + 1) / (n + 1)

def main():
    codes = load(sys.argv[1]); N = len(codes)
    out = {"N": N}
    out["quote_errors"] = (quote_check(codes) if os.path.exists(f"{CORPUS}/papers.jsonl")
                           else "skipped: no corpus (set EVIDENCE_AUDIT_CORPUS)")
    trade = [c for c in codes if c.get("costs") != "na"]
    out["n_trading_test"] = len(trade)
    tr = [c.get("trials") for c in trade]
    out["H1"] = {"count_or_adjusted": sum(t in ("count", "adjusted") for t in tr) / len(trade),
                 "adjusted": sum(t == "adjusted" for t in tr) / len(trade),
                 "pass": None}
    out["H1"]["pass"] = out["H1"]["count_or_adjusted"] < 0.10 and out["H1"]["adjusted"] < 0.05
    tm = [c["test_months"] for c in trade if c.get("test_months")]
    out["H2"] = {"n": len(tm), "median_months": median(tm) if tm else None}
    out["H2"]["pass"] = bool(tm) and median(tm) <= 12
    both = [(c["test_months"], c["sharpe"]) for c in trade
            if c.get("test_months") and isinstance(c.get("sharpe"), (int, float))
            and "relative_improvement" not in (c.get("sharpe_flags") or [])]
    if len(both) >= 5:
        rho, p = perm_p_spearman_neg([a for a, _ in both], [b for _, b in both])
        out["H3"] = {"n": len(both), "rho": rho, "p_one_sided": p, "pass": rho < 0 and p < 0.05}
    # Pre-registered definition: test window not known to lie wholly after the LLM's training cutoff.
    pre = [c for c in trade if c.get("llm_cutoff_before_test") != "y"]
    out["H4"] = {"n_not_after_cutoff": len(pre),
                 "share_none_or_ack": (sum(c.get("leakage") in ("none", "acknowledged") for c in pre) / len(pre)) if pre else None}
    out["H4"]["pass"] = bool(pre) and out["H4"]["share_none_or_ack"] > 0.5
    sh = lambda c: isinstance(c.get("sharpe"), (int, float)) and "relative_improvement" not in (c.get("sharpe_flags") or [])
    wc = [c["sharpe"] for c in trade if sh(c) and c.get("costs") in ("flat", "realistic")]
    nc = [c["sharpe"] for c in trade if sh(c) and c.get("costs") == "none"]
    if wc and nc:
        u, p = mw_p_less(wc, nc)
        out["H5"] = {"n_cost": len(wc), "n_nocost": len(nc), "median_cost": median(wc),
                     "median_nocost": median(nc), "p_one_sided": p, "pass": p < 0.05}
    out["secondary"] = {
        "code_rate": sum(bool(c.get("code")) for c in codes) / N,
        "bh_rate": sum(bool(c.get("baseline_bh")) for c in trade) / len(trade),
        "live_rate": sum(c.get("leakage") == "live" for c in trade) / len(trade),
        "costs": {k: sum(c.get("costs") == k for c in codes) for k in ("none", "flat", "realistic", "na")},
        "leakage": {k: sum(c.get("leakage") == k for c in codes) for k in ("none", "acknowledged", "post_cutoff", "live", "chrono", "na")},
        "trials": {k: sum(c.get("trials") == k for c in codes) for k in ("none", "mentioned", "count", "adjusted")},
        "median_sharpe": median([c["sharpe"] for c in trade if sh(c)]) if any(sh(c) for c in trade) else None,
        "n_sharpe": sum(sh(c) for c in trade),
    }
    if len(sys.argv) > 2:
        sec = {c["id"]: c for c in load(sys.argv[2])}; first = {c["id"]: c for c in codes}
        ag = {}
        for f in ("costs", "leakage", "trials", "baseline_bh", "code"):
            pairs = [(first[i].get(f), sec[i].get(f)) for i in sec if i in first]
            ag[f] = sum(a == b for a, b in pairs) / len(pairs)
        def close(a, b, tol):
            return (a is None and b is None) or (a is not None and b is not None and abs(a - b) <= tol * max(1, abs(a)))
        pairs = [(first[i].get("test_months"), sec[i].get("test_months")) for i in sec if i in first]
        ag["test_months_within_10pct"] = sum(close(a, b, .10) for a, b in pairs) / len(pairs)
        pairs = [(first[i].get("sharpe"), sec[i].get("sharpe")) for i in sec if i in first]
        ag["sharpe_within_5pct"] = sum(close(a, b, .05) for a, b in pairs) / len(pairs)
        out["agreement"] = ag
    print(json.dumps(out, indent=1, default=str))

if __name__ == "__main__":
    main()
