"""Source-led arithmetic blocks and a prime-decision experiment.

The arithmetic routines implement operations represented in the Sanskrit sources:
division with remainder, mutual division, square-root extraction, trial divisors and
factoring by a difference of squares. This is a modern program, not a transcription of
a historical algorithm, and it does not claim that any source states a prime-generation
formula.

This module avoids Python's %, //, / and ** operators and math-library calls. It builds
division and square-root extraction from decimal digits, multiplication and comparison.
Python strings, lists, loops and control flow remain part of the implementation.

The default `decide()` route uses `acchedya_meet()`, which combines two source-inspired
searches and uses a newly derived stopping bound. That bound is not stated in a Sanskrit
text. The literal routes (`vibhaga`, `gk-trial`, `vargantara`) continue their searches
without that bound and are much slower. No cited verse states the modern square-root
stopping theorem; `use_root_stop=True` is an explicit optional shortcut, off by default.

Attestation levels used below:
  stated     the verse states the procedure
  applied    the verse's procedure, applied in a way the verse does not itself spell out
  ours       a choice we made where the text leaves it open (marked at the point of use)
"""
from __future__ import annotations

from dataclasses import dataclass, field

VERSES = {
    "bhagahara": ("Līlāvatī, division rule", "stated",
                  "bhājyād dharaḥ śudhyati yadguṇaḥ syād antyāt phalaṃ tat khalu bhāgahāre"),
    "apavartana": ("Līlāvatī, same verse; Gaṇitasārasaṅgraha 2.18-19; Bhāskara I on Āryabhaṭīya", "stated operation; general use applied",
                   "samena kenāpy apavartya hāra-bhājyau bhajed vā sati saṃbhave tu"),
    "paraspara": ("Āryabhaṭīya 2.32", "mutual-remainder operation stated in kuṭṭaka; general GCD use applied",
                  "adhikāgrabhāgahāraṃ chindyād ūnāgrabhāgahāreṇa | śeṣaparasparabhaktaṃ …"),
    "vargamula": ("Āryabhaṭīya 2.4", "stated",
                  "bhāgaṃ hared avargān nityaṃ dviguṇena vargamūlena | vargād varge śuddhe labdhaṃ sthānāntare mūlam"),
    "vibhaga": ("Śatapatha Brāhmaṇa 10.4.2.4-17", "applied",
                "ātmano 'kuruta … sa naiva vyāpnot  /  na …-dhā vyabhavat"),
    "sama_pancaka": ("Gaṇita Kaumudī 11 v2", "provisional OCR; stated if the reading holds",
                     "repeatedly divide an even number by 2 …; if 5 is in the units place, divide by 5"),
    "acchedya_trial": ("Gaṇita Kaumudī 11 v3-4", "provisional OCR; stated if the reading holds",
                       "acchedyāḥ kalpyante tri-saptaikādaśādayaś chedāḥ; while you find divisors, keep finding"),
    "varga": ("Gaṇita Kaumudī 11 v4", "provisional OCR; stated if the reading holds", "if N is a square, its root is a factor, twice"),
    "vargantara": ("Gaṇita Kaumudī 11 v5-8", "provisional OCR; stated if the reading holds",
                   "add a square to make a square; m^2 + r: 2m+1-r, then add 2m+3, 2m+5 … until a square"),
    "sarva_hara": ("Gaṇita Kaumudī 11 v8-9", "provisional OCR; v9 incomplete",
                   "put the previous products in front of each new divisor, and again separately"),
    "m_minus_x": ("Gaṇita Kaumudī 11 v9-10", "provisional reconstruction; v9 incomplete",
                  "the nearest root less a chosen number is a divisor [when it divides]; else choose again"),
    "sesha_pariksa": ("Gaṇita Kaumudī 11 v11", "provisional OCR; stated if the reading holds",
                      "by a chosen number, take remainders of both numbers being multiplied"),
    "dvir_ardhe": ("Chandaḥśāstra 8.28-31", "stated", "dvir ardhe | rūpe śūnyam | dviḥ śūnye | tāvad ardhe tad-guṇitam"),
}


def _whole(name, n, least=0):
    if not isinstance(n, int) or isinstance(n, bool) or n < least:
        raise ValueError(f"{name} must be a whole number >= {least}")


def _digits(n):
    """The decimal places of n, highest first (aṅka-sthāna)."""
    return [int(c) for c in str(n)]


# ================================================================== bhāgahāra — division
def bhagahara(bhajya: int, hara: int):
    """Divide by the Līlāvatī rule. Returns (phala, śeṣa): quotient and remainder.

    'From the last (highest) digits of the dividend the divisor is cleanly subtracted
    with some multiplier; that multiplier is the quotient [digit].' Each step finds the
    largest multiplier 0..9 for which divisor x multiplier can be subtracted.
    """
    _whole("bhājya", bhajya)
    _whole("hāra", hara, 1)
    phala, sesa = 0, 0
    for d in _digits(bhajya):
        sesa = sesa * 10 + d                      # bring down the next place
        g = 9
        while hara * g > sesa:                    # yad-guṇaḥ śudhyati
            g -= 1
        sesa -= hara * g
        phala = phala * 10 + g
    return phala, sesa


def divides(hara: int, bhajya: int) -> bool:
    return bhagahara(bhajya, hara)[1] == 0


# ================================================================== paraspara-bhajana — mutual division
@dataclass
class Paraspara:
    steps: list                 # (dividend, divisor, quotient, remainder)
    last_remainder: int         # the last non-zero remainder — the common measure (apavartanāṅka)


def paraspara_bhajana(a: int, b: int) -> Paraspara:
    """Āryabhaṭīya 2.32: divide the larger by the smaller, then the remainders by each other."""
    _whole("a", a, 1)
    _whole("b", b, 1)
    big, small = (a, b) if a >= b else (b, a)
    steps = []
    while True:
        q, r = bhagahara(big, small)
        steps.append((big, small, q, r))
        if r == 0:
            return Paraspara(steps, small)
        big, small = small, r


def apavartana(a: int, b: int):
    """Reduce a pair by its common measure (Līlāvatī; Gaṇitasārasaṅgraha 2.18-19).

    The reducer is the last remainder of the mutual division (the commentary practice:
    Bhāskara I reduces divisor and dividend 'by one reducer' before the kuṭṭaka).
    Nothing is assumed about it: both divisions are carried out and must leave no remainder.
    Returns (a', b', reducer).
    """
    g = paraspara_bhajana(a, b).last_remainder
    qa, ra = bhagahara(a, g)
    qb, rb = bhagahara(b, g)
    if ra or rb:
        raise ArithmeticError("reducer does not divide both numbers")   # never expected; checked, not assumed
    return qa, qb, g


# ================================================================== vargamūla — square root
def vargamula(n: int):
    """Āryabhaṭīya 2.4. Returns (mūla, śeṣa) with mūla x mūla + śeṣa = n and śeṣa as small as possible.

    Places are marked alternately varga (odd places from the units) and avarga (even places).
    From the highest varga place take the largest square; then repeatedly: divide the avarga
    place (with what remains) by twice the root found so far; subtract the square of the
    quotient from the next varga place; the quotient is the next digit of the root.
    """
    _whole("n", n)
    d = _digits(n)
    place = "avarga"                               # mark places from the units: varga, avarga, varga, …
    for _ in d:
        place = "varga" if place == "avarga" else "avarga"
    if place == "varga":                           # highest place is varga: pad so places pair as (avarga, varga)
        d = [0] + d
    root, rem, first = 0, 0, True
    for i in range(0, len(d), 2):
        av, vg = d[i], d[i + 1]
        if first:                                  # highest varga group: largest square in it
            grp = av * 10 + vg
            r = 9
            while r * r > grp:
                r -= 1
            root, rem, first = r, grp - r * r, False
            continue
        x = rem * 10 + av                          # bring down the avarga place
        q = bhagahara(x, 2 * root)[0] if root else 0   # bhāgaṃ hared avargāt … dviguṇena vargamūlena
        q = min(q, 9)
        while True:
            y = (x - q * 2 * root) * 10 + vg       # bring down the varga place
            if y - q * q >= 0:                     # vargād varge śuddhe
                break
            q -= 1
        root, rem = root * 10 + q, y - q * q       # labdhaṃ sthānāntare mūlam
    return root, rem


def is_varga(n: int) -> bool:
    return vargamula(n)[1] == 0


# ================================================================== ŚB 10.4.2 — division into bodies
@dataclass
class VibhagaStep:
    k: int
    bricks: int | None          # quotient if k divides n, else None

    def words(self):
        return (f"{self.k} bodies of {self.bricks} — ātmano 'kuruta" if self.bricks is not None
                else f"na {self.k}-dhā vyabhavat")


def vibhaga(n: int, k: int) -> VibhagaStep:
    q, r = bhagahara(n, k)
    return VibhagaStep(k, q if r == 0 else None)


def vibhaga_record(n: int, upto: int):
    """Try k = 2 .. upto bodies, as ŚB 10.4.2 does for 720 (where the text stops at 24)."""
    _whole("n", n, 2)
    return [vibhaga(n, k) for k in range(2, upto + 1)]


# ================================================================== Gaṇita Kaumudī 11
def sama(n: int) -> bool:
    """Even: the units place is 0, 2, 4, 6 or 8 (GK v2 'sama')."""
    return _digits(n)[-1] in (0, 2, 4, 6, 8)


def pancaka_sthane(n: int) -> bool:
    """GK v2: 5 in the units place."""
    return _digits(n)[-1] == 5


def asakrd_bhaga(n: int, d: int):
    """GK v2/v4 'asakṛt': divide repeatedly while d divides. Returns (times, what remains)."""
    t = 0
    while n > 1:
        q, r = bhagahara(n, d)
        if r:
            break
        n, t = q, t + 1
    return t, n


_ACCHEDYA = [2]


def _extend_acchedyas(limit: int):
    """Grow the list of acchedyas up to limit: c is acchedya when no acchedya found so far divides it.
    Applied form of ŚB/GK: each earlier acchedya is tried as a divisor ('na …-dhā vyabhavat')."""
    c = _ACCHEDYA[-1] + 1
    while c <= limit:
        if not any(divides(a, c) for a in _ACCHEDYA):
            _ACCHEDYA.append(c)
        c += 1


def _acchedya_at(i: int) -> int:
    """The i-th acchedya (0-based), growing the list as needed."""
    while len(_ACCHEDYA) <= i:
        _extend_acchedyas(_ACCHEDYA[-1] * 2)
    return _ACCHEDYA[i]


def acchedyas_upto(limit: int):
    _whole("limit", limit)
    _extend_acchedyas(limit)
    return [a for a in _ACCHEDYA if a <= limit]


@dataclass
class Trace:
    steps: list = field(default_factory=list)

    def add(self, verse, text):
        self.steps.append((verse, text))


def gk_trial(n: int, trace: Trace | None = None):
    """GK v2-4: remove 2s and 5s, then try the acchedyas 3, 7, 11 … and keep finding divisors.

    Stop rule (ours — the text gives none): stop when the next acchedya to try exceeds what
    remains; what remains is then itself acchedya (no smaller acchedya divides it).
    Returns the list of acchedya factors (with repeats).
    """
    _whole("n", n, 2)
    tr = trace or Trace()
    out, m = [], n
    t, m = asakrd_bhaga(m, 2) if sama(m) else (0, m)
    if t:
        out += [2] * t
        tr.add("GK v2", f"even: divided by 2, {t} time(s) -> {m}")
    if m > 1 and pancaka_sthane(m):
        t, m = asakrd_bhaga(m, 5)
        out += [5] * t
        tr.add("GK v2", f"5 in the units place: divided by 5, {t} time(s) -> {m}")
    i = 0
    while m > 1:
        _extend_acchedyas(m)
        while i < len(_ACCHEDYA) and _ACCHEDYA[i] in (2, 5):
            i += 1
        a = _ACCHEDYA[i]
        if a == m:                                    # nothing smaller divided: m is acchedya
            out.append(m)
            tr.add("GK v3-4", f"no acchedya below {m} divides it: {m} is acchedya")
            break
        t, m2 = asakrd_bhaga(m, a)
        if t:
            out += [a] * t
            tr.add("GK v3-4", f"acchedya {a} divides, {t} time(s) -> {m2}")
            m = m2
        i += 1
    return out


@dataclass
class Vargantara:
    n: int
    m: int                      # nearest root
    r: int                      # n = m*m + r
    tries: list                 # (amount added so far, square?) in order
    big: int                    # (m + k) — root of the square reached
    s: int                      # root of the square that was added
    factors: tuple              # (big - s, big + s)


def vargantara(n: int) -> Vargantara:
    """GK v4-8, for odd n: add squares until a square is reached.

    n = m^2 + r (Āryabhaṭa's root). The first amount to add is 2m + 1 - r; while it is not a
    square, add 2m + 3, then 2m + 5, … ('in arithmetic progression until you get a square').
    When n + s^2 = b^2, the factors are b - s and b + s. If n is itself a square, its root
    is the factor, twice (v4).
    """
    _whole("n", n, 1)
    if sama(n):
        raise ValueError("GK applies the square method after the 2s are removed (n must be odd)")
    m, r = vargamula(n)
    if r == 0:
        return Vargantara(n, m, 0, [], m, 0, (m, m))
    add, step, big, tries = 2 * m + 1 - r, 2 * m + 3, m + 1, []
    while True:
        s, rest = vargamula(add)
        tries.append((add, rest == 0))
        if rest == 0:
            return Vargantara(n, m, r, tries, big, s, (big - s, big + s))
        add, step, big = add + step, step + 2, big + 1


def sarva_hara(factors):
    """GK v8-9: list every divisor (other than 1) from the factors, by the text's procedure."""
    out = []
    for f in factors:
        new = [d * f for d in out] + [f]           # previous products put in front, and f separately
        for x in new:
            if x not in out:
                out.append(x)
    return sorted(out)


def m_minus_x(n: int, x: int):
    """GK v9-10: with n = m^2 + r, the number m - x divides n when it divides x^2 + r.
    Returns (m - x, divides?). Which x to choose is left to ingenuity by the text."""
    m, r = vargamula(n)
    d = m - x
    if d < 2:
        return d, False
    return d, divides(d, x * x + r)


def sesha_pariksa(a: int, b: int, c: int, k: int):
    """GK v11: check a x b = c by remainders under a chosen k. Returns (consistent?, detail)."""
    ra, rb, rc = bhagahara(a, k)[1], bhagahara(b, k)[1], bhagahara(c, k)[1]
    rab = bhagahara(ra * rb, k)[1]
    return rab == rc, (ra, rb, rab, rc)


def bhagadana(n: int, trial_upto: int = 100):
    """GK 11 factorisation, verse by verse.

    v2: take out 2s and 5s. v3-4: try the acchedyas up to trial_upto (how far to go is
    our choice). v4-8: on what remains (odd), add squares until a square appears;
    v7: factor the two parts found 'as before'. A part whose square method yields only
    1 x part has no other factor and is recorded as acchedya. Returns (factors, trace).
    """
    _whole("n", n, 2)
    tr, out, m = Trace(), [], n
    t, m = asakrd_bhaga(m, 2) if sama(m) else (0, m)
    if t:
        out += [2] * t
        tr.add("GK v2", f"divided by 2, {t} time(s) -> {m}")
    if m > 1 and pancaka_sthane(m):
        t, m = asakrd_bhaga(m, 5)
        out += [5] * t
        tr.add("GK v2", f"divided by 5, {t} time(s) -> {m}")
    for a in acchedyas_upto(trial_upto):
        if a in (2, 5) or m == 1:
            continue
        t, m2 = asakrd_bhaga(m, a)
        if t:
            out += [a] * t
            tr.add("GK v3-4", f"acchedya {a}, {t} time(s) -> {m2}")
            m = m2
    stack = [m] if m > 1 else []
    while stack:
        x = stack.pop()
        v = vargantara(x)
        lo, hi = v.factors
        if lo == 1:
            out.append(x)
            tr.add("GK v5-8", f"{x}: the first square reached gives 1 x {x}: {x} is acchedya")
        elif lo == hi and v.r == 0:
            stack += [lo, lo]
            tr.add("GK v4", f"{x} is the square of {lo}: factor twice")
        else:
            stack += [lo, hi]
            tr.add("GK v5-8", f"{x} + {v.s}^2 = {v.big}^2 -> factors {lo} and {hi}")
    return sorted(out), tr


# ================================================================== the acchedya decision
def acchedya(n: int, route: str = "vibhaga"):
    """Is n acchedya (indivisible)? Three routes, each built only from the procedures above.

    vibhaga     try every k = 2 .. n-1 as the number of bodies (ŚB form, complete enumeration)
    gk-trial    GK v2-4 with the stop rule described in gk_trial
    vargantara  GK v5-8 (odd n): acchedya exactly when the first square reached gives 1 x n
    meet        GK v3-4 and v5-8 run toward each other, with the derived meeting bound
    Returns (is_acchedya, smallest divisor found or None).
    """
    _whole("n", n)
    if n < 2:
        return False, None
    if route == "vibhaga":
        for k in range(2, n):
            if divides(k, n):
                return False, k
        return True, None
    if route == "gk-trial":
        f = gk_trial(n)
        return (f == [n]), (None if f == [n] else f[0])
    if route == "vargantara":
        if sama(n):
            return (n == 2), (None if n == 2 else 2)
        if n == 1:
            return False, None
        v = vargantara(n)
        return (v.factors[0] == 1), (None if v.factors[0] == 1 else v.factors[0])
    if route == "meet":
        r = acchedya_meet(n)
        return r.acchedya, r.factor
    raise ValueError("route must be 'vibhaga', 'gk-trial', 'vargantara' or 'meet'")


# ================================================================== reducing the work
# Each reduction below is labelled:
#   derived  follows from the text's own identity n + s^2 = b^2 (GK v5) by a short argument
#            in the style of GK v11 (reasoning with remainders); no verse states it
# None changes an answer; the tests check that against the plain versions.

_SQUARE_LAST_DIGITS = (0, 1, 4, 5, 6, 9)        # last digits of 0x0 … 9x9 — computed, see square_last_digits()


def square_last_digits():
    """The units digits a square can end in, found by multiplying 0..9 by themselves."""
    return tuple(sorted({_digits(d * d)[-1] for d in range(10)}))


@dataclass
class VargantaraFast:
    n: int
    big_tried: int              # values of b actually stepped through
    roots_taken: int            # vargamūla calls actually made
    factors: tuple


def vargantara_fast(n: int) -> VargantaraFast:
    """GK v4-8 with two cuts, same result as vargantara().

    1. parity (derived): for odd n, b^2 - s^2 = n. By remainders on division by 4, a square
       leaves 0 or 1; so if n leaves 1, b must be odd, and if n leaves 3, b must be even.
       Every other b is skipped: the step between amounts becomes (2b+1) + (2b+3) = 4b + 4.
    2. last digit (derived): an amount whose units digit is 2, 3, 7 or 8 cannot be a square
       (square_last_digits), so its root is not taken.
    """
    _whole("n", n, 1)
    if sama(n):
        raise ValueError("n must be odd (GK removes the 2s first)")
    m, r = vargamula(n)
    if r == 0:
        return VargantaraFast(n, 0, 1, (m, m))
    b = m + 1
    rem4 = bhagahara(n, 4)[1]
    want_odd = rem4 == 1
    if (not sama(b)) != want_odd:                  # first b of the right parity
        b += 1
    amount = b * b - n
    tried, roots = 0, 1
    while True:
        tried += 1
        if _digits(amount)[-1] in _SQUARE_LAST_DIGITS:
            s, rest = vargamula(amount)
            roots += 1
            if rest == 0:
                return VargantaraFast(n, tried, roots, (b - s, b + s))
        amount += 4 * b + 4                        # (b+2)^2 - b^2
        b += 2


@dataclass
class Meet:
    n: int
    acchedya: bool | None       # None = unresolved (stopped by the step budget)
    factor: int | None
    divisions: int              # trial divisions made
    big_tried: int              # square-method steps made
    stopped_by: str


def acchedya_meet(n: int, use_root_stop: bool = False, max_steps: int | None = None) -> Meet:
    """Run GK's two searches toward each other: trial division upward from 3 (v3-4) and the
    square method upward from the nearest root (v4-8), alternately one step each.

    Stopping (derived; no square-root stopping rule used):
      * Let D be the next acchedya divisor not yet tried. All smaller possible prime
        divisors have either been tried or removed by the earlier 2/5 checks. Any
        factorisation n = a*c with a <= c therefore has a >= D; otherwise a would have
        a prime divisor below D that already divides n.
      * Then a + c <= D + n/D, because
        (a + n/a) - (D + n/D) = (a - D)(1 - n/(a*D)). With D <= a <= c, the first
        factor is non-negative and a*D <= a*c = n, so the second factor is non-positive.
      * A factor pair gives n + s^2 = b^2 with b = (a + c)/2 and s = (c - a)/2
        (GK v5). The square search tries b-centers in order from the nearest-root
        successor. Every possible remaining factor pair has a center at or below
        (D + n/D)/2. The code uses floor(n/D) and an extra step of slack in its integer
        comparison before returning acchedya.

    `max_steps` counts outer trial-division and square-search steps. It does not cap every
    internal arithmetic operation, root-extraction step or prime-list extension.

    `use_root_stop`: also stop the trial once D passes the nearest root m. This is the
    square-root rule: if a <= b then a x a <= a x b = n, so a <= m. No verse states it;
    it is offered here as an explicit choice, off by default.
    """
    _whole("n", n, 2)
    t, m_rest = asakrd_bhaga(n, 2) if sama(n) else (0, n)
    if t:
        return Meet(n, n == 2, None if n == 2 else 2, 1, 0, "even (GK v2)")
    if pancaka_sthane(n):
        return Meet(n, n == 5, None if n == 5 else 5, 1, 0, "5 in the units place (GK v2)")
    m, r = vargamula(n)
    if r == 0:
        return Meet(n, False, m, 0, 0, "square (GK v4)")
    divisions, tried, i = 0, 0, 0
    b = m + 1
    if n == 3:
        return Meet(n, True, None, 0, 0, "no smaller acchedya than 3 to try")
    amount = b * b - n
    step = 2 * b + 1
    while True:
        if max_steps is not None and divisions + tried >= max_steps:
            return Meet(n, None, None, divisions, tried, f"unresolved: step budget {max_steps} used")
        # one trial division
        while _acchedya_at(i) in (2, 5):
            i += 1
        d = _acchedya_at(i)
        if d >= n:
            return Meet(n, True, None, divisions, tried, "trial reached n")
        if use_root_stop and d > m:
            return Meet(n, True, None, divisions, tried, "trial passed the root (square-root rule)")
        divisions += 1
        if divides(d, n):
            return Meet(n, False, d, divisions, tried, "trial division (GK v3-4)")
        i += 1
        D = _acchedya_at(i)
        # one square step
        tried += 1
        s, rest = vargamula(amount)
        if rest == 0 and b - s > 1:
            return Meet(n, False, b - s, divisions, tried, "square method (GK v5-8)")
        amount, step, b = amount + step, step + 2, b + 1
        # the meeting bound
        if b > bhagahara(D + bhagahara(n, D)[0], 2)[0] + 1:
            return Meet(n, True, None, divisions, tried, "searches met (derived bound)")


# ================================================================== source-led layer: decision and listing
@dataclass
class Outcome:
    n: int
    status: str                 # "neither" | "composite" | "acchedya" | "unresolved"
    factors: tuple | None       # (a, b) with a x b = n, a > 1, when composite
    steps: int                  # trial divisions + square steps
    how: str
    layer: str = "source-led"


def decide(n: int, max_steps: int | None = None) -> Outcome:
    """Source-led decision with explicit boundary, composite, acchedya or unresolved outcomes.

    GK v2: an even number, or one with 5 in the units place, is settled at once.
    GK v3-4 and v5-8: trial by acchedyas from 3 upward and the square method from the
    nearest root, run toward each other until the derived meeting bound (acchedya_meet).
    Inputs below 2 return "neither". If max_steps runs out first the answer is
    "unresolved" — never "acchedya". The stopping bound is derived, not text-attested.
    """
    _whole("n", n)
    if n < 2:
        return Outcome(n, "composite" if n > 1 else "neither", None, 0, "n < 2 is not acchedya")
    r = acchedya_meet(n, max_steps=max_steps)
    steps = r.divisions + r.big_tried
    if r.acchedya is None:
        return Outcome(n, "unresolved", None, steps, r.stopped_by)
    if r.acchedya:
        return Outcome(n, "acchedya", None, steps, r.stopped_by)
    other = bhagahara(n, r.factor)[0]
    return Outcome(n, "composite", (r.factor, other), steps, r.stopped_by)


def gk_v2_passes(n: int) -> bool:
    """GK v2 as a filter: not even and no 5 in the units place (2 and 5 themselves pass)."""
    if n in (2, 5):
        return True
    return not sama(n) and not pancaka_sthane(n)


def acchedyas_between(a: int, b: int, max_steps: int | None = None):
    """List acchedyas in [a, b] by the source-led layer.

    GK v2 discards 6 of every 10 numbers by their units digit; trial by 3 (the first
    named acchedya) then discards a further third, so 8 of every 30 reach the full
    search — the same survivors as a mod-30 wheel, reached by the text's own steps.
    Returns (acchedyas, unresolved).
    """
    _whole("a", a)
    _whole("b", b)
    found, open_ = [], []
    for n in range(max(a, 2), b + 1):
        if not gk_v2_passes(n):
            continue
        if n != 3 and divides(3, n):
            continue
        o = decide(n, max_steps)
        if o.status == "acchedya":
            found.append(n)
        elif o.status == "unresolved":
            open_.append(n)
    return found, open_


# ================================================================== Piṅgala — powers
def dvir_ardhe(base: int, e: int) -> int:
    """Chandaḥśāstra 8.28-31: halve the exponent and square ('ardhe … tad-guṇitam'),
    or take one away and multiply ('rūpe śūnyam … dviḥ'). Used here only to compute powers."""
    _whole("e", e)
    if e == 0:
        return 1
    half, odd = bhagahara(e, 2)
    if odd:
        return dvir_ardhe(base, e - 1) * base
    h = dvir_ardhe(base, half)
    return h * h
