"""Tools for checking the verses: transliteration, syllable weight, metre, number words, sandhi.

Nothing here decides anything about primes; it only reads and checks the texts.
"""
import re
import unicodedata

# ------------------------------------------------------------------ Devanagari -> IAST
_CONS = {"क": "k", "ख": "kh", "ग": "g", "घ": "gh", "ङ": "ṅ", "च": "c", "छ": "ch", "ज": "j", "झ": "jh", "ञ": "ñ",
         "ट": "ṭ", "ठ": "ṭh", "ड": "ḍ", "ढ": "ḍh", "ण": "ṇ", "त": "t", "थ": "th", "द": "d", "ध": "dh", "न": "n",
         "प": "p", "फ": "ph", "ब": "b", "भ": "bh", "म": "m", "य": "y", "र": "r", "ल": "l", "ळ": "ḻ", "व": "v",
         "श": "ś", "ष": "ṣ", "स": "s", "ह": "h"}
_VOW = {"अ": "a", "आ": "ā", "इ": "i", "ई": "ī", "उ": "u", "ऊ": "ū", "ऋ": "ṛ", "ॠ": "ṝ", "ऌ": "ḷ",
        "ए": "e", "ऐ": "ai", "ओ": "o", "औ": "au"}
_MAT = {"ा": "ā", "ि": "i", "ी": "ī", "ु": "u", "ू": "ū", "ृ": "ṛ", "ॄ": "ṝ", "ॢ": "ḷ", "े": "e", "ै": "ai",
        "ो": "o", "ौ": "au"}
_OTHER = {"ं": "ṃ", "ः": "ḥ", "ँ": "ṃ", "ꣳ": "ṃ", "ऽ": "'", "।": "|", "॥": "||"}
_VIRAMA = "्"


def deva_to_iast(s: str) -> str:
    s = "".join(ch for ch in s if not (0x0951 <= ord(ch) <= 0x0954 or 0x1CD0 <= ord(ch) <= 0x1CFF
                                     or (0xA8E0 <= ord(ch) <= 0xA8FF and ch != "ꣳ") or ch in "‌‍"))
    out, i = [], 0
    while i < len(s):
        ch = s[i]
        if ch in _CONS:
            out.append(_CONS[ch])
            nxt = s[i + 1] if i + 1 < len(s) else ""
            if nxt in _MAT:
                out.append(_MAT[nxt])
                i += 1
            elif nxt == _VIRAMA:
                i += 1
            else:
                out.append("a")
        elif ch in _VOW:
            out.append(_VOW[ch])
        elif ch in _OTHER:
            out.append(_OTHER[ch])
        elif "०" <= ch <= "९":
            out.append(str(ord(ch) - ord("०")))
        else:
            out.append(ch)
        i += 1
    return "".join(out)


def norm(s: str) -> str:
    """Any retrieved text -> plain IAST: Devanagari converted, GRETIL H/+ fixed, accents removed."""
    if re.search(r"[ऀ-ॿ]", s):
        s = deva_to_iast(s)
    s = s.replace("H", "ḥ").replace("+", "'").replace("’", "'")
    s = s.replace("'a", "'")                            # GRETIL '+a': the a after avagraha is elided
    # drop Vedic accent marks written on IAST vowels (á, ā́, …) but keep ś, ṣ, ṛ etc.
    s, kept, base = unicodedata.normalize("NFD", s), [], ""
    for c in s:
        if unicodedata.combining(c):
            if c in "́̀" and base.lower() in "aeiou":
                continue
        else:
            base = c
        kept.append(c)
    s = unicodedata.normalize("NFC", "".join(kept))
    return s.lower().replace("ṁ", "ṃ")


# ------------------------------------------------------------------ syllable weight
_VOWELS = ["ai", "au", "ā", "ī", "ū", "ṝ", "ṛ", "ḷ", "a", "i", "u", "e", "o"]
_LONG = {"ai", "au", "ā", "ī", "ū", "ṝ", "e", "o"}
_CONSONANTS = ["kh", "gh", "ch", "jh", "ṭh", "ḍh", "th", "dh", "ph", "bh",
               "k", "g", "ṅ", "c", "j", "ñ", "ṭ", "ḍ", "ṇ", "t", "d", "n", "p", "b", "m",
               "y", "r", "l", "ḻ", "v", "ś", "ṣ", "s", "h"]


def phonemes(text: str):
    """IAST -> list of ('V', v) | ('C', c) | ('M', ṃ/ḥ); everything else dropped."""
    t, i, out = norm(text), 0, []
    while i < len(t):
        for v in _VOWELS:
            if t.startswith(v, i):
                out.append(("V", v)); i += len(v); break
        else:
            for c in _CONSONANTS:
                if t.startswith(c, i):
                    out.append(("C", c)); i += len(c); break
            else:
                if t[i] in "ṃḥ":
                    out.append(("M", t[i]))
                i += 1
    return out


def weights(text: str):
    """Syllable weights in order: 1 = laghu, 2 = guru (final syllable by its own nature)."""
    ph, w = phonemes(text), []
    for k, (kind, val) in enumerate(ph):
        if kind != "V":
            continue
        heavy = val in _LONG
        j, cons = k + 1, 0
        while j < len(ph) and ph[j][0] != "V":
            if ph[j][0] == "M":
                heavy = True
            else:
                cons += 1
            j += 1
        if j < len(ph) and cons >= 2:
            heavy = True
        if j == len(ph) and cons >= 1:          # closed final syllable
            heavy = True
        w.append(2 if heavy else 1)
    return w


def pattern(ws):
    return "".join("–" if x == 2 else "⏑" for x in ws)


# ------------------------------------------------------------------ metre checks
def check_anustubh(half: str):
    """One half-verse = 2 pādas of 8 syllables (pathyā rule; odd-pāda vipulās allowed)."""
    w = weights(half)
    res = {"syllables": len(w), "pattern": pattern(w)}
    if len(w) != 16:
        res.update(ok=False, why=f"{len(w)} syllables, expected 16")
        return res
    a, b = w[:8], w[8:]
    even_ok = b[4] == 1 and b[5] == 2 and b[6] == 1
    odd_pathya = a[4] == 1 and a[5] == 2 and a[6] == 2
    res.update(ok=even_ok, even_pada_cadence=even_ok,
               odd_pada="pathyā" if odd_pathya else "vipulā/irregular",
               why="" if even_ok else "even pāda: syllables 5-7 must be ⏑–⏑")
    return res


def check_arya(halves):
    """Āryā: first half 30 mātrās, second half 27 (the last syllable of each half counts as long)."""
    out = []
    for idx, h in enumerate(halves):
        w = weights(h)
        m = sum(w[:-1]) + 2 if w else 0
        need = 30 if idx % 2 == 0 else 27
        out.append({"half": idx + 1, "matras": m, "expected": need, "ok": m == need, "pattern": pattern(w)})
    return out


ARYA_FAMILY = {(30, 27): "āryā", (30, 30): "gīti", (27, 27): "upagīti", (27, 30): "udgīti", (32, 32): "āryāgīti"}


def check_arya_family(halves):
    """Name the member of the āryā family by the mātrā count of each half-verse pair.
    Only totals are checked, not the internal gaṇa rules."""
    rs = check_arya(halves)
    out = []
    for i in range(0, len(rs) - 1, 2):
        a, b = rs[i]["matras"], rs[i + 1]["matras"]
        name = ARYA_FAMILY.get((a, b))
        out.append({"verse": i // 2 + 1, "matras": (a, b), "type": name, "ok": name is not None,
                    "patterns": (rs[i]["pattern"], rs[i + 1]["pattern"])})
    return out


INDRAVAJRA = "––⏑––⏑⏑–⏑––"
UPENDRAVAJRA = "⏑–⏑––⏑⏑–⏑––"
VASANTATILAKA = "––⏑–⏑⏑⏑–⏑⏑–⏑––"


def _match(p, target):
    return len(p) == len(target) and p[:-1] == target[:-1]      # final syllable anceps


def check_upajati(halves):
    out = []
    for h in halves:
        p = pattern(weights(h))
        if len(p) != 22:
            out.append({"ok": False, "why": f"{len(p)} syllables, expected 22", "pattern": p})
            continue
        names = []
        for pada in (p[:11], p[11:]):
            names.append("indravajrā" if _match(pada, INDRAVAJRA) else
                         "upendravajrā" if _match(pada, UPENDRAVAJRA) else "irregular")
        out.append({"ok": "irregular" not in names, "padas": names, "pattern": p})
    return out


def check_vasantatilaka(padas):
    return [{"ok": _match(pattern(weights(p)), VASANTATILAKA), "pattern": pattern(weights(p))} for p in padas]


# ------------------------------------------------------------------ sandhi (compound-internal, as needed here)
def join(left: str, right: str) -> str:
    if not left:
        return right
    l, r = left[-1], right[0]
    if l in "aā" and r in "aā":
        return left[:-1] + "ā" + right[1:]
    if l in "aā" and r in "iī":
        return left[:-1] + "e" + right[1:]
    if l in "aā" and r in "uū":
        return left[:-1] + "o" + right[1:]
    if l in "aā" and r == "ṛ":
        return left[:-1] + "ar" + right[1:]
    if l in "iī" and r in "iī":
        return left[:-1] + "ī" + right[1:]
    if l in "iī" and r in "aāuūeo":
        return left[:-1] + "y" + right
    if l in "uū" and r in "aāiīeo":
        return left[:-1] + "v" + right
    if l == "ṭ" and r in "aāiīuūeogjḍdbvyrl":
        return left[:-1] + "ḍ" + right
    return left + right


def join_all(tokens):
    s = ""
    for t in tokens:
        s = join(s, norm(t))
    return s


# ------------------------------------------------------------------ bhūtasaṅkhyā (word-numerals)
BHUTA = {
    "kha": "0", "śūnya": "0", "vyoma": "0",
    "rūpa": "1", "indu": "1", "niśākara": "1",
    "dasra": "2", "akṣi": "2", "locana": "2", "yama": "2", "aśvi": "2", "dvi": "2",
    "agni": "3", "tri": "3", "vahni": "3", "śikhi": "3",
    "veda": "4", "sāgara": "4", "arṇava": "4", "kṛta": "4",
    "iṣu": "5", "śara": "5", "mārgaṇa": "5", "pañca": "5",
    "rasa": "6", "ṛtu": "6", "ṣaṭ": "6",
    "sapta": "7", "adri": "7", "naga": "7", "bhūdhara": "7",
    "aṣṭa": "8", "vasu": "8", "sarpa": "8", "bhujaṅga": "8",
    "aṅka": "9",
    "rada": "32", "tithi": "15",
}
_INFLECTED = {"sāgarair": "sāgara", "vedā": "veda", "arṇavāḥ": "arṇava", "arṇavā": "arṇava",
              "mārgaṇāḥ": "mārgaṇa", "locanāni": "locana", "indavaḥ": "indu", "vahnayas": "vahni",
              "bhūdharāḥ": "bhūdhara", "niśākarāḥ": "niśākara", "dasrakāḥ": "dasra", "tithayo": "tithi"}


def bhuta_value(token: str):
    t = norm(token)
    if t.startswith("~"):
        return None                                   # marked non-numeral word
    if t == "catuṣka":
        return "x4"
    t = _INFLECTED.get(t, t)
    if t not in BHUTA:
        raise KeyError(f"not a word-numeral in this lexicon: {token}")
    return BHUTA[t]


def read_bhuta(tokens):
    """aṅkānāṃ vāmato gatiḥ: the digits run leftwards, so read the words in reverse order."""
    vals = []
    for t in tokens:
        v = bhuta_value(t)
        if v is None:
            continue
        if v == "x4":
            vals[-1:] = vals[-1:] * 4                  # kha-catuṣka: four kha
        else:
            vals.append(v)
    return int("".join(reversed(vals)))


# ------------------------------------------------------------------ ordinary number words
_UNIT_STEMS = {1: ["eka", "ekā"], 2: ["dvi", "dva", "dvā", "dve", "dvau"], 3: ["tri", "trīṇi", "trīn", "tisraḥ", "tisras", "tisro", "trayaḥ", "trayas", "traya"],
               4: ["catur", "catura", "catvāri", "catasraḥ", "catasras"], 5: ["pañca"], 6: ["ṣaṭ", "ṣaḍ"],
               7: ["sapta"], 8: ["aṣṭa", "aṣṭā", "aṣṭau"], 9: ["nava"], 10: ["daśa"]}
_PREFIX = {1: ["eka"], 2: ["dvā", "dvi"], 3: ["trayo", "trayas", "trayaś", "tri"], 4: ["catur", "catuś", "catus"],
           5: ["pañca"], 6: ["ṣaṭ", "ṣaḍ", "ṣaṇ"], 7: ["sapta"], 8: ["aṣṭā", "aṣṭa"], 9: ["nava"]}
_DECADES = {20: ["viṃśati"], 30: ["triṃśat"], 40: ["catvāriṃśat"], 50: ["pañcāśat"], 60: ["ṣaṣṭi"],
            70: ["saptati"], 80: ["aśīti"], 90: ["navati"]}
_PLACES = {100: ["śata"], 1000: ["sahasra"], 10**4: ["ayuta"], 10**5: ["niyuta"], 10**6: ["prayuta"],
           10**7: ["arbuda"], 10**8: ["nyarbuda"], 10**9: ["samudra"], 10**10: ["madhya"],
           10**11: ["anta"], 10**12: ["parārdha", "parārddha"]}


def _build_stems():
    st = {}
    for v, forms in _UNIT_STEMS.items():
        for f in forms:
            st[f] = v
    teens = {11: "ekādaśa", 12: "dvādaśa", 13: "trayodaśa", 14: "caturdaśa", 15: "pañcadaśa", 16: "ṣoḍaśa",
             17: "saptadaśa", 18: "aṣṭādaśa", 19: "navadaśa"}
    for v, f in teens.items():
        st[f] = v
    for dec, dforms in _DECADES.items():
        for d in dforms:
            st[d] = dec
            for u, pforms in _PREFIX.items():
                for p in pforms:
                    st[join(p, d)] = dec + u
                    st[p + d] = dec + u
            for e in ("ekānna", "ekān na "):
                st[join(e, d)] = dec - 1
                st[e + d] = dec - 1
    st[join("ekānna", "śata")] = 99
    st["ṣaṇṇavati"] = 96
    st["adhyardha"] = 1.5
    for v, forms in _PLACES.items():
        for f in forms:
            st[f] = v
    return st


STEMS = _build_stems()
_ENDINGS = ["ābhyāṃ", "ābhyām", "ābhyāg", "bhyāṃ", "bhyām", "bhyāg", "bhyaḥ", "bhyas", "smai", "āya", "āni", "āṇi", "ebhyaḥ", "ā", "am", "aṃ",
            "aḥ", "ḥ", "ś", "s", "ṃ", "m", "e", "yai", "ayaḥ", "ayo", "ī", "īḥ", "iś", "iḥ", "dhā", ""]


def parse_number(word: str):
    """One inflected number word -> value, or None. Tries stem + known ending, with stem-final sandhi."""
    w = norm(word).strip(" '|,;")
    w = re.sub(r"[cd]$", "t", w)                      # ekatriṃśac / catvāriṃśad -> -t
    w = re.sub(r"ś$", "ḥ", w)                         # tisraś (before ca) -> tisraḥ
    if w in STEMS:
        return STEMS[w]
    for stem in sorted(STEMS, key=len, reverse=True):
        variants = {stem, stem[:-1]} if stem[-1] in "ai" else {stem}
        if stem.endswith("t"):
            variants |= {stem[:-1] + "c", stem[:-1] + "d"}
        for s in variants:
            if w.startswith(s) and w[len(s):] in _ENDINGS:
                if s == stem[:-1] and stem[-1] == "a" and not w[len(s):].startswith(("ā", "e", "ebh")):
                    continue
                return STEMS[stem]
    return None


def parse_phrase(phrase: str):
    """A list item of one or two words: '2', or '2 x 100' (dvābhyāṃ śatābhyām, tribhyaḥ śatebhyaḥ)."""
    words = norm(phrase).split()
    vals = [parse_number(w) for w in words]
    if len(words) == 1:
        return vals[0]
    if len(words) == 2 and all(v is not None for v in vals) and vals[1] in (100, 1000):
        return vals[0] * vals[1]
    return None


def split_svaha(text: str):
    """TS 7.2 lists: items separated by svāhā, with vowel sandhi across the boundary restored."""
    t = norm(text).replace("|", " ").strip()
    parts = re.split(r"svāh(?:ā|a)", t)
    items, carry = [], ""
    for k, p in enumerate(parts):
        p = p.strip()
        if k > 0 and parts[k - 1] is not None:
            raw = parts[k]
            if raw and not raw.startswith(" "):
                if raw.startswith("i"):            # svāhā + e… -> svāhai…
                    p = "e" + raw[1:].strip()
                elif raw[0] not in "aāiīuūeo":     # svāhā + a… -> svāhā…
                    p = "a" + raw.strip()
        if p:
            items.append(p)
    return items


def split_ca(text: str):
    """VS 17.2: number words joined by 'ca', with sandhi cāyutaṃ = ca ayutaṃ, samudraśca = samudraḥ ca."""
    t = norm(text).replace("|", " ")
    t = t.replace("santvekā", "santu ekā")             # u + e -> ve
    t = re.sub(r"\bcā", "ca a", t)
    t = re.sub(r"\bcai", "ca e", t)
    t = re.sub(r"śca(?=\s|$|i|e|a)", "ḥ ca ", t)
    t = re.sub(r"śca", "ḥ ca ", t)
    words = [w for w in t.split() if w != "ca"]
    return [(w, parse_number(w)) for w in words]


def split_ca_me(text: str):
    """VS 18.24-25 lists: items separated by 'ca me' (sandhi 'ma' before a vowel)."""
    t = norm(text).replace("|", " ")
    t = re.sub(r"yajñena kalpantām.*$", "", t)
    t = t.replace("'", " a")                           # me'ṣṭau -> me aṣṭau
    parts = re.split(r"\s*ca\s+m[ae]\s*|(?<=[śc])ca\s+m[ae]\s*", t)
    return [p.strip() for p in parts if p.strip()]
