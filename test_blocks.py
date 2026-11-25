"""Finite oracle checks for the source-led arithmetic implementation.

The checks use ordinary arithmetic as independent oracles. The default decision route
also uses a derived stopping bound, documented in blocks.py. The optional modern-layer
comparison is skipped when its external prime_model.py dependency is absent.
"""
import ast
import math
import random
import sys
import time

import blocks as B
import check_verses as CV

results = []


class SkipTest(Exception):
    pass


def test(fn):
    t = time.perf_counter()
    try:
        d = fn() or ""
        results.append((fn.__name__, "PASS", time.perf_counter() - t, d))
    except SkipTest as e:
        results.append((fn.__name__, "SKIP", time.perf_counter() - t, str(e)))
    except AssertionError as e:
        results.append((fn.__name__, "FAIL", time.perf_counter() - t, str(e)))
    return fn


def oracle_prime(n):
    if n < 2:
        return False
    return all(n % d for d in range(2, math.isqrt(n) + 1))


# ------------------------------------------------------------------ the blocks contain no modern operations
@test
def blocks_use_no_modern_operations():
    tree = ast.parse(open("blocks.py").read())
    bad = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.BinOp, ast.AugAssign)) and isinstance(node.op, (ast.Mod, ast.FloorDiv, ast.Div, ast.Pow)):
            bad.append(f"line {node.lineno}: {type(node.op).__name__}")
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [a.name for a in node.names] + ([node.module] if isinstance(node, ast.ImportFrom) else [])
            if any(n and n not in ("annotations", "dataclasses", "__future__", "dataclass", "field") for n in names):
                bad.append(f"line {node.lineno}: import {names}")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("pow", "divmod", "round"):
            bad.append(f"line {node.lineno}: {node.func.id}()")
    assert not bad, bad
    return "no %, //, /, **, pow, divmod or math imports in blocks.py"


# ------------------------------------------------------------------ arithmetic blocks vs oracles
@test
def bhagahara_matches_ordinary_division():
    random.seed(1)
    cases = [(0, 1), (7, 7), (720, 24), (1, 9), (10**40 + 7, 97)] + \
            [(random.randrange(0, 10**random.randrange(1, 30)), random.randrange(1, 10**random.randrange(1, 12))) for _ in range(3000)]
    for a, b in cases:
        assert B.bhagahara(a, b) == divmod(a, b), (a, b)
    return f"{len(cases)} divisions, up to 40-digit dividends"


@test
def vargamula_matches_integer_root():
    random.seed(2)
    xs = list(range(0, 20001)) + [random.randrange(0, 10**random.randrange(5, 40)) for _ in range(2000)]
    for n in xs:
        r, s = B.vargamula(n)
        assert r == math.isqrt(n) and r * r + s == n, n
    return f"{len(xs)} roots (all n <= 20,000 and random up to 40 digits)"


@test
def mutual_division_gives_common_measure():
    random.seed(3)
    for _ in range(3000):
        a, b = random.randrange(1, 10**9), random.randrange(1, 10**9)
        g = B.paraspara_bhajana(a, b).last_remainder
        assert g == math.gcd(a, b)
        a2, b2, g2 = B.apavartana(a, b)
        assert (a2 * g2, b2 * g2) == (a, b) and math.gcd(a2, b2) == 1
    return "3,000 pairs: last remainder = common measure; reduced pairs share nothing further"


@test
def pingala_powers():
    for b in range(2, 8):
        for e in range(0, 70):
            assert B.dvir_ardhe(b, e) == b ** e
    assert B.dvir_ardhe(2, 11) == 2048 and B.dvir_ardhe(5, 5) == 3125
    return "bases 2..7, exponents 0..69; 2^11 = 2048, 5^5 = 3125 (GK exercises)"


# ------------------------------------------------------------------ ŚB 10.4.2
@test
def sb_720_reproduced_from_the_sanskrit():
    divisions, failures = CV.check_sb()
    rec = B.vibhaga_record(720, 24)
    got_div = {s.k: s.bricks for s in rec if s.bricks is not None}
    got_fail = {s.k for s in rec if s.bricks is None}
    assert got_div == divisions, (got_div, divisions)
    assert got_fail == failures, (got_fail, failures)
    return "14 divisions with brick counts and 9 failures, all read from the Sanskrit (Weber)"


# ------------------------------------------------------------------ Gaṇita Kaumudī 11 exercises
@test
def gk_exercises():
    expect = {2048: [2] * 11, 3125: [5] * 5, 7250: [2, 5, 5, 5, 29], 7520: [2] * 5 + [5, 47],
              10201: [101, 101], 1161: [3, 3, 3, 43], 1001: [7, 11, 13], 4620: [2, 2, 3, 5, 7, 11],
              3927: [3, 7, 11, 17], 120: [2, 2, 2, 3, 5], 231: [3, 7, 11]}
    for n, f in expect.items():
        assert sorted(B.gk_trial(n)) == f, (n, B.gk_trial(n))
        g, _ = B.bhagadana(n, trial_upto=1)               # square method only, no trial division
        assert g == f, (n, g)
    v = B.vargantara(1161)
    assert (v.m, v.r, v.tries[0], v.factors) == (34, 5, (64, True), (27, 43))      # blog: 34^2+5, 64 = 8^2
    assert B.vargantara(10201).factors == (101, 101)                                 # v5: square, root twice
    assert len(B.sarva_hara([2, 2, 3, 5, 7, 11])) == 47                              # 48 divisors less 1
    assert B.sarva_hara([2, 3, 5, 7, 7])[:6] == [2, 3, 5, 6, 7, 10]
    return "11 exercise numbers by trial (11.2-4) and by squares alone (11.4-8); 1161 = 35^2 - 8^2; 4620 has 47 divisors besides 1"


@test
def gk_m_minus_x_and_remainder_check():
    # 120 = 10^2 + 20: the blog's worked choices of x
    assert [B.m_minus_x(120, x) for x in (2, 4, 5, 6, 3)] == [(8, True), (6, True), (5, True), (4, True), (7, False)]
    assert B.m_minus_x(231, 4) == (11, True)                    # 231 = 15^2 + 6
    for k, rr in ((3, (2, 2, 1, 1)), (5, (4, 2, 3, 3)), (8, (5, 1, 5, 5))):
        ok, det = B.sesha_pariksa(29, 17, 493, k)
        assert ok and det == rr, (k, det)
    assert not B.sesha_pariksa(29, 17, 494, 3)[0]
    return "120 with x = 2,4,5,6,3 and 231 with x = 4 as in the text's solutions; 29 x 17 = 493 by remainders 3, 5, 8"


# ------------------------------------------------------------------ the acchedya decision
@test
def three_routes_agree_with_definition():
    for n in range(0, 3001):
        truth = oracle_prime(n)
        for route in ("vibhaga", "gk-trial", "vargantara"):
            if n < 2 and route == "gk-trial":
                continue
            got, f = B.acchedya(n, route) if n >= 2 or route != "gk-trial" else (False, None)
            assert got == truth, (n, route, got, f)
            if not got and n >= 2:
                assert n % f == 0 and 1 < f < n, (n, route, f)
    return "every n <= 3,000, all three routes, divisor witnesses checked"


@test
def acchedya_list_and_larger_numbers():
    lst = B.acchedyas_upto(20_000)
    assert lst == [n for n in range(2, 20_001) if oracle_prime(n)]
    random.seed(4)
    sample = [random.randrange(2, 200_000) for _ in range(300)] + [99991, 99989, 100003, 199999]
    for n in sample:
        assert B.acchedya(n, "vibhaga")[0] == oracle_prime(n), n
        if n % 2:
            assert B.acchedya(n, "vargantara")[0] == oracle_prime(n), n
    return f"{len(lst):,} acchedyas to 20,000; 304 numbers to 200,000 by two routes"


@test
def reductions_give_the_same_answers():
    assert B.square_last_digits() == (0, 1, 4, 5, 6, 9)
    for n in range(3, 20_001, 2):
        assert B.vargantara(n).factors == B.vargantara_fast(n).factors, n
    for n in range(2, 20_001):
        r = B.acchedya_meet(n)
        assert r.acchedya == oracle_prime(n), (n, r)
        if not r.acchedya:
            assert n % r.factor == 0 and 1 < r.factor < n, (n, r)
    random.seed(5)
    big = [random.randrange(10**6, 10**10) for _ in range(400)] + [999_983, 1_000_003 * 1_000_033, 101 * 9901]
    for n in big:
        r = B.acchedya_meet(n)
        assert r.acchedya == oracle_prime(n), (n, r)
    return "fast squares = plain squares for odd n <= 20,000; meet route exact for n <= 20,000 and 403 numbers to 10^10"


@test
def steps_saved():
    rows = []
    for n in (999_983, 99_991, 101 * 9901):
        plain = len(B.vargantara(n).tries)
        fast = B.vargantara_fast(n)
        meet = B.acchedya_meet(n)
        rows.append(f"{n:,}: squares {plain:,} -> fast {fast.big_tried:,} steps / {fast.roots_taken:,} roots"
                    f" -> meet {meet.divisions}+{meet.big_tried}")
    p = 1_000_000_007
    t = time.perf_counter(); r = B.acchedya_meet(p); dt = time.perf_counter() - t
    assert r.acchedya and r.stopped_by.startswith("searches met")
    rows.append(f"1,000,000,007 proved acchedya by meet: {r.divisions}+{r.big_tried} steps, {dt:.2f}s")
    return "; ".join(rows)


@test
def source_led_three_outcomes():
    o = B.decide(341)
    assert o.status == "composite" and o.factors == (11, 31)
    o = B.decide(999_983, max_steps=50)
    assert o.status == "unresolved" and o.factors is None          # a budget never yields "acchedya"
    assert B.decide(999_983).status == "acchedya"
    for n in range(2, 5001):
        o = B.decide(n, max_steps=6)
        assert o.status == "unresolved" or (o.status == "acchedya") == oracle_prime(n), (n, o)
    survivors = [n for n in range(31, 61) if B.gk_v2_passes(n) and not B.divides(3, n)]
    assert len(survivors) == 8
    return "341 -> 11 x 31; 999,983 unresolved at 50 steps, acchedya at 224; tight budget never gives a false prime; 8 of 30 survive GK v2 + 3"


@test
def two_layers_agree():
    try:
        import engines as E
        E._load_modern()
    except (ModuleNotFoundError, RuntimeError) as exc:
        raise SkipTest(f"optional modern comparison unavailable: {exc}") from exc
    r = E.cross_check(2, 25_000)
    assert r["agree"] and not r["source_led_unresolved"], r
    r2 = E.cross_check(10**6, 10**6 + 3000, max_steps=40)
    assert r2["agree"], r2
    d = E.decide(10**12 + 39, "modern")
    assert d["status"] == "prime" and d["layer"] == "modern"
    t = time.perf_counter(); E.primes_between(2, 25_000, "source-led"); a = time.perf_counter() - t
    t = time.perf_counter(); E.primes_between(2, 25_000, "modern"); b = time.perf_counter() - t
    return (f"2..25,000: identical ({r['primes']:,} primes); 10^6..10^6+3000 with budget 40: "
            f"{len(r2['source_led_unresolved'])} unresolved, none wrong; time to 25,000: source-led {a:.2f}s, modern {b*1000:.1f}ms")


@test
def verse_checks_flag_only_known_text_problems():
    res = CV.run()
    flagged = {item for s, item, ok, d in res if ok is False}
    expected = {"Gaṇita Kaumudī 11.1 (āryā family)", "Gaṇita Kaumudī 11.9 (āryā family)",
                "Gaṇita Kaumudī 11.11 (āryā family)", "Līlāvatī 41 (vasantatilakā)"}
    assert flagged == expected, flagged
    return f"{len(res)} verse checks; only the {len(expected)} known textual problems flagged"


@test
def cost_report():
    t = time.perf_counter(); B.acchedya(999_983, "vibhaga"); a = time.perf_counter() - t
    t = time.perf_counter(); B.acchedya(99_991, "vargantara"); b = time.perf_counter() - t
    t = time.perf_counter(); B.bhagadana(1_000_009 * 1_000_033); c = time.perf_counter() - t
    return (f"999,983 by vibhaga {a:.1f}s (999,981 divisions); 99,991 by squares {b:.1f}s; "
            f"close 13-digit product by GK squares {c:.2f}s")


if __name__ == "__main__":
    w = max(len(r[0]) for r in results)
    for name, status, dt, d in results:
        print(f"{status:<4}  {name:<{w}}  {dt:6.2f}s  {d}")
    failed = sum(1 for r in results if r[1] == "FAIL")
    passed = sum(1 for r in results if r[1] == "PASS")
    skipped = sum(1 for r in results if r[1] == "SKIP")
    print(f"\n{passed} passed, {failed} failed, {skipped} skipped")
    sys.exit(1 if failed else 0)
