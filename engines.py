"""Two layers, kept apart, with every answer labelled by the layer that produced it.

source-led   blocks.py — procedures stated in the verses (division, mutual division,
             square root, GK v2-11 (edition numbering) searches) plus the derived meeting bound. Three outcomes:
             composite (with a factor pair), acchedya, or unresolved (step budget used).
modern       optional external prime_model.py — not included here, so its implementation,
             exactness bounds and benchmark results are not reproducible from this bundle.
             Any probable-prime result must retain that label. None of this is Sanskrit.

cross_check() runs both and reports any disagreement.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "prime_model"))

import blocks as SL          # noqa: E402
MOD = None


def _load_modern():
    """Load the optional modern engine on demand; it is not included in this bundle."""
    global MOD
    if MOD is not None:
        return MOD
    try:
        import prime_model as modern  # noqa: E402
    except ModuleNotFoundError as exc:
        if exc.name == "prime_model":
            raise RuntimeError("modern comparison requires the separate prime_model.py package") from exc
        raise
    MOD = modern
    return MOD


def decide(n: int, layer: str = "source-led", max_steps=None) -> dict:
    if layer == "source-led":
        o = SL.decide(n, max_steps)
        return {"n": n, "layer": "source-led", "status": o.status, "factors": o.factors,
                "steps": o.steps, "how": o.how}
    if layer == "modern":
        modern = _load_modern()
        v = modern.check(n)
        certainty = getattr(v, "certainty", None)
        certainty_text = str(certainty).lower()
        proven = certainty is True or any(word in certainty_text for word in
                                          ("proven", "deterministic", "exact", "certified"))
        status = ("neither" if n < 2 else
                  ("composite" if not v.prime else ("prime" if proven else "probable prime")))
        f = (v.factor, n // v.factor) if (not v.prime and v.factor) else None
        return {"n": n, "layer": "modern", "status": status, "factors": f,
                "certainty": certainty, "how": v.method}
    raise ValueError("layer must be 'source-led' or 'modern'")


def primes_between(a: int, b: int, layer: str = "source-led", max_steps=None) -> dict:
    if layer == "source-led":
        found, unresolved = SL.acchedyas_between(a, b, max_steps)
        return {"layer": "source-led", "primes": found, "unresolved": unresolved}
    if layer == "modern":
        modern = _load_modern()
        return {"layer": "modern", "primes": modern.primes_between(a, b), "unresolved": []}
    raise ValueError("layer must be 'source-led' or 'modern'")


def cross_check(a: int, b: int, max_steps=None) -> dict:
    """Both layers over [a, b]; source-led 'unresolved' numbers are listed, not counted as wrong."""
    s = primes_between(a, b, "source-led", max_steps)
    m = set(primes_between(a, b, "modern")["primes"])
    sl = set(s["primes"])
    wrong = sorted((sl - m) | ((m - sl) - set(s["unresolved"])))
    return {"range": (a, b), "agree": not wrong, "disagreements": wrong,
            "source_led_unresolved": s["unresolved"], "primes": len(m)}
