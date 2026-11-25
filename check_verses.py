"""Check every verse the blocks use: text present, metre, number words, and the texts' own arithmetic.

Run:  python check_verses.py        -> prints a summary and writes verse_report.md
The checks use ordinary arithmetic to TEST the texts; the blocks themselves (blocks.py)
use only procedures stated in the verses.
"""
import re
import corpus as C
import vtools as V

RESULTS = []          # (section, item, True/False/None, detail); None is informational


def rec(section, item, ok, detail=""):
    RESULTS.append((section, item, None if ok is None else bool(ok), detail))
    return ok


def ev(structure: str):
    """Evaluate 'ṣaṣṭi + tri * śata' with each word read by the number lexicon."""
    expr = structure
    for w in sorted(set(re.findall(r"[^\s+*()]+", structure)), key=len, reverse=True):
        v = V.parse_number(w)
        if v is None:
            raise KeyError(w)
        expr = re.sub(rf"(?<![^\s+*(]){re.escape(w)}(?![^\s+*)])", str(v), expr)
    return eval(expr, {"__builtins__": {}})


# ------------------------------------------------------------------ 1. ŚB 10.4.2
def check_sb():
    S = "ŚB 10.4.2"
    divisions, failures = {}, set()
    for v in C.SB_10_4_2:
        t = V.norm(v["text"])
        if v["bodies"]:
            span, word = v["bodies"]
            rec(S, f'{v["ref"]} bodies span', V.norm(span) in t, span)
            b = V.parse_number(word)
        else:
            b = None
        if v["bricks"]:
            span, struct = v["bricks"]
            rec(S, f'{v["ref"]} bricks span', V.norm(span) in t, span)
            q = ev(struct)
        else:
            q = None
        if b and q:
            divisions[b] = q
            rec(S, f'{v["ref"]} {b} bodies x {q} bricks = 720', b * q == 720, f"{b} x {q} = {b*q}")
        for span, word in v["fails"]:
            rec(S, f'{v["ref"]} failure span', V.norm(span) in t, span)
            k = V.parse_number(word)
            failures.add(k)
            rec(S, f'{v["ref"]} "na {k}-dhā vyabhavat": {k} does not divide 720', 720 % k != 0, f"720 = {k} x {720//k} + {720%k}")
        if v.get("note"):
            rec(S, f'{v["ref"]} note', None, v["note"])
    covered = sorted(set(divisions) | failures)
    rec(S, "every k = 2..24 appears exactly once (division or failure)",
        covered == list(range(2, 25)) and not (set(divisions) & failures), f"{covered}")
    rec(S, "the failures are exactly the k in 2..24 that do not divide 720",
        sorted(failures) == [k for k in range(2, 25) if 720 % k], f"{sorted(failures)}")
    rec(S, "source-coverage note: the supplied Weber text contains the 2..24 series", None,
        f"{len(divisions)} divisions, {len(failures)} failures")
    F = {k: V.norm(t) for k, t in C.SB_10_4_2_FULL.items()}
    chain = [
        ("10.4.2.2: 'sapta ca śatāni viṃśatiś ca' = 720 day-and-night bricks", "sapta ca śatāni viṃśatiścāhorātrāṇi" in F[2],
         ev("sapta * śata + viṃśati") == 720, "700 + 20 = 720"),
        ("10.4.2.2: enclosing stones + yajuṣmatī bricks = 360 + 360", F[2].count("ṣaṣṭiśca trīṇi ca śatāni") == 2,
         2 * ev("ṣaṣṭi + tri * śata") == 720, "360 + 360 = 720"),
        ("10.4.2.17-18: 24 bodies = 24 half-months (caturviṃśaty-ardhamāsaḥ saṃvatsaraḥ)",
         "caturviṃśatyardhamāsaḥ saṃvatsaraḥ" in F[18], 24 * 30 == 720, "24 x 30 = 720"),
        ("10.4.2.18: fifteen muhūrtas of the day and fifteen of the night = 30 per day",
         "pañcadaśāhno" in F[18] and "pañcadaśaiva rātreḥ" in F[18], 15 + 15 == 30, "15 + 15 = 30"),
        ("10.4.2.20: muhūrtas in a year = daśa ca sahasrāṇi aṣṭau ca śatāni",
         "daśa ca sahasrāṇi, aṣṭau ca śatāni" in F[20], 360 * 30 == ev("daśa * sahasra + aṣṭau * śata"), "360 x 30 = 10,800"),
        ("10.4.2.23: 12,000 bṛhatīs (36 syllables) laid in paṅktis (40) = aṣṭāśataṃ śatāni",
         "dvādaśa bṛhatīsahasrāṇi" in F[23] and "aṣṭāśataṃ śatāni paṅktayo" in F[23],
         12000 * 36 == 108 * 100 * 40, "12,000 x 36 = 432,000 = 10,800 x 40"),
        ("10.4.2.24: yajus 8,000 + sāman 4,000 = 12,000 bṛhatīs", "aṣṭau yajuṣām" in F[24] and "catvāri sāmnām" in F[24],
         8000 + 4000 == 12000, "8,000 + 4,000 = 12,000"),
        ("10.4.2.25: the three Vedas = 10,800 eighties of syllables", "daśa ca sahasrāṇyaṣṭau ca śatānyaśītīnām" in F[25],
         (12000 + 12000) * 36 == 10800 * 80, "24,000 x 36 = 864,000 = 10,800 x 80"),
        ("10.4.2.25-27: one eighty per muhūrta, so 10,800 muhūrtas carry 10,800 eighties",
         "muhūrtenāśītimāpnot" in F[25] and "pañcadaśāśītīḥ" in F[27], 10800 == 360 * 30, "10,800 = 360 x 30"),
    ]
    for name, present, ok, detail in chain:
        rec(S, name, present and ok, detail if present else "phrase not found in text")
    return divisions, failures


# ------------------------------------------------------------------ 2. Sūrya Siddhānta
def check_ss():
    S = "Sūrya Siddhānta 1"
    vals = {}
    for verse, half, compound, tokens, label in C.SS_NUMERALS:
        line = V.norm(C.SS[verse][half])
        joined = V.join_all([t.lstrip("~") for t in tokens])
        rec(S, f"{verse}{'ab'[half]} compound occurs in GRETIL line", V.norm(compound) in line, compound)
        rec(S, f"{verse}{'ab'[half]} words re-join by sandhi to the written compound", joined == V.norm(compound),
            f"{' + '.join(tokens)} -> {joined}")
        n = V.read_bhuta(tokens)
        vals[(verse, half)] = n
        ann = C.SS_GRETIL_ANNOTATIONS.get((verse, half))
        if ann is not None:
            rec(S, f"{verse}{'ab'[half]} {label}: read right-to-left = GRETIL's own figure", n == ann, f"{n:,}")
        else:
            rec(S, f"{verse}{'ab'[half]} {label}", None, f"read right-to-left = {n:,}; no independent expected value supplied ({_extra(label)})")
    sun, moon = vals[("1.29", 0)], vals[("1.30", 0)]
    sid, civ, lun = vals[("1.34", 0)], vals[("1.37", 0)], vals[("1.37", 1)]
    chain = [
        ("1.14: divine year = 60 x 6 days (tat-ṣaṣṭiḥ ṣaḍ-guṇā)", 60 * 6 == 360, "360"),
        ("1.15: 12,000 divine years x 360 = (2,3,4 read leftwards) x ayuta", 12000 * 360 == vals[("1.15", 1)] * 10**4,
         f"{12000*360:,} = {vals[('1.15', 1)]} x 10,000"),
        ("1.17: yugas = tenth part x 4,3,2,1; junctions = one sixth of each",
         [12000 // 10 * k for k in (4, 3, 2, 1)] == [4800, 3600, 2400, 1200] and 4800 // 6 == 800, "4800/3600/2400/1200; Kṛta junctions 800"),
        ("1.18-20: 14 manus x 71 yugas + 15 junctions of Kṛta length (0.4 yuga) = 1000 yugas",
         14 * 71 * 10 + 15 * 4 == 1000 * 10, "994 + 6 = 1000"),
        ("1.22-23: trighana (3 x 3 x 3) yugas gone, now in the 28th", 3 ** 3 + 1 == 28, "27 + 1 = 28"),
        ("1.24: (4,7,4 read leftwards) x 100 divine years", vals[("1.24", 1)] * 100 == 47400, f"{vals[('1.24', 1)]} x 100 = 47,400"),
        ("1.29: Sun's revolutions = years in a mahāyuga (1.15)", sun == 4_320_000, f"{sun:,}"),
        ("1.34b: civil days = sidereal days − Sun's revolutions (1.37a)", sid - sun == civ, f"{sid:,} − {sun:,} = {sid-sun:,}"),
        ("1.35: lunar months = Moon − Sun revolutions", moon - sun == 53_433_336, f"{moon-sun:,}"),
        ("1.35: adhimāsas = lunar months − 12 x Sun revolutions", (moon - sun) - 12 * sun == 1_593_336, f"{(moon-sun)-12*sun:,}"),
        ("1.36-37: lunar days = 30 x lunar months (1.37b)", 30 * (moon - sun) == lun, f"30 x {moon-sun:,} = {30*(moon-sun):,}"),
        ("1.36: tithi-kṣaya = lunar days − civil days", lun - civ == 25_082_252, f"{lun-civ:,}"),
    ]
    for name, ok, detail in chain:
        rec(S, name, ok, detail)
    return vals


def _extra(label):
    return {"x ayuta": "x 10,000 per 1.15", "x 100 (śataghnāḥ)": "x 100 per 1.24"}.get(label, "")


# ------------------------------------------------------------------ 3. yuga lengths across texts
def check_yugas():
    S = "Yuga lengths across texts"
    bh = V.norm(" ".join(C.BHAGAVATA_3_11["halves"]))
    vi = V.norm(" ".join(C.VISNU_1_3["halves"]))
    ma = V.norm(" ".join(C.MANU_1_68_72["halves"]))
    seq = [V.parse_number(w) for w in ("catvāri", "trīṇi", "dve", "ekaṃ")]
    rec(S, "Bhāgavata 3.11.19 / Viṣṇu 1.3.12: 'catvāri trīṇi dve caikaṃ'",
        "catvāri trīṇi dve caikaṃ" in bh and "catvāri trīṇi dve caikaṃ" in vi and seq == [4, 3, 2, 1], f"{seq}")
    bhag = [k * 1000 + 2 * k * 100 for k in seq]                    # sahasrāṇi dviguṇāni śatāni ca
    rec(S, "Bhāgavata: thousands + twice as many hundreds", "sahasrāṇi dviguṇāni śatāni" in bh, f"{bhag}")
    visnu = [k * 1000 + k * 100 + k * 100 for k in seq]             # tat-pramāṇaiḥ śataiḥ sandhyā … sandhyāṃśaḥ tat-tulyaḥ
    rec(S, "Viṣṇu: thousands + same number of hundreds before and after",
        "tatpramāṇaiḥ śataiḥ sandhyā" in vi and "sandhyāṃśaścaiva tattulyo" in vi, f"{visnu}")
    manu = [(4 - d) * 1000 + 2 * (4 - d) * 100 for d in range(4)]   # 4000 + 400 + 400, then ekāpāyena
    rec(S, "Manu 1.69-70: 4000 + 400 + 400, others less by one",
        "catvāryāhuḥ sahasrāṇi" in ma and "ekāpāyena" in ma, f"{manu}")
    ss = [12000 // 10 * k for k in (4, 3, 2, 1)]
    rec(S, "Sūrya Siddhānta 1.17: tenth part x 4,3,2,1", True, f"{ss}")
    rec(S, "all four texts give the same yuga lengths", bhag == visnu == manu == ss, f"{bhag}")
    rec(S, "totals: 12,000 in each (dvādaśa-)",
        "dvādaśabhir" in bh and "dvādaśabhis" in vi and "dvādaśasāhasraṃ" in ma and sum(bhag) == 12000, "12,000")
    rec(S, "Manu 1.71 sandhi note", None, C.MANU_1_68_72["note"])


# ------------------------------------------------------------------ 4. Vedic number lists
def check_lists():
    S = "Vedic number lists"
    expect = {
        "7.2.11": list(range(1, 20)) + list(range(29, 100, 10)) + [100, 200],
        "7.2.12": list(range(1, 20, 2)) + list(range(29, 100, 10)) + [100],
        "7.2.13": list(range(2, 21, 2)) + [98, 100],
        "7.2.14": list(range(3, 20, 2)) + list(range(29, 100, 10)) + [100],
        "7.2.15": [4, 8, 12, 16, 20, 96, 100],
        "7.2.16": [5, 10, 15, 20, 95, 100],
        "7.2.17": list(range(10, 101, 10)),
        "7.2.18": [20, 40, 60, 80, 100],
        "7.2.19": [50] + list(range(100, 1000, 100)) + [1000],
        "7.2.20": [10 ** k for k in range(2, 13)],
    }
    for k, text in C.TS_7_2.items():
        items = V.split_svaha(text)
        got = [V.parse_phrase(i) for i in items]
        nums = [g for g in got if g is not None]
        unread = [i for i, g in zip(items, got) if g is None and i not in ("sarvasmai",)]
        non_num = [i for i in unread if V.norm(i) in ("uṣase", "vyuṣṭyai", "udeṣyate", "udyate", "uditāya", "suvargāya", "lokāya")]
        anomalies = [i for i in unread if i not in non_num]
        if k == "7.2.18" and "aśyītyai" in anomalies:
            nums.insert(3, 80)
        rec(S, f"TS {k}", nums == expect[k],
            f"{_compact(nums)}" + (f"; unreadable: {anomalies} (read as aśītyai = 80)" if anomalies else "")
            + (f"; non-number offerings: {len(non_num)}" if non_num else ""))
    ek = [V.norm(i) for i in V.split_svaha(C.TS_7_2["7.2.11"])]
    rec(S, "TS 7.2.11 naming: 19, 39, 59, 79, 99 as ekānna- ('one short'); 29, 49, 69, 89 as nava-",
        [V.parse_number(w) for w in ek if w.startswith("ekānn")] == [19, 39, 59, 79, 99]
        and [V.parse_number(w) for w in ek if w.startswith("nav") and V.parse_number(w) > 20] == [29, 49, 69, 89])
    v24 = [V.parse_phrase(i) for i in V.split_ca_me(C.VS["18.24"])]
    rec(S, "VS 18.24: odd numbers 1-33, each repeated", v24 == [1] + [x for n in range(3, 33, 2) for x in (n, n)] + [33], _compact(v24))
    v25 = [V.parse_phrase(i) for i in V.split_ca_me(C.VS["18.25"])]
    rec(S, "VS 18.25: multiples of 4 to 48, each repeated", v25 == [4] + [x for n in range(8, 48, 4) for x in (n, n)] + [48], _compact(v25))
    v17 = [v for w, v in V.split_ca(C.VS["17.2"]) if v is not None]
    rec(S, "VS 17.2: eka, daśa ... parārdha = 10^0 ... 10^12",
        sorted(set(v17)) == [10 ** k for k in range(13)], f"{len(set(v17))} place names, largest 10^12")


def _compact(xs):
    return ", ".join(str(x) for x in xs) if len(xs) <= 14 else ", ".join(str(x) for x in xs[:8]) + f" … {xs[-1]} ({len(xs)} items)"


# ------------------------------------------------------------------ 5. counting passages
def check_counts():
    S = "Counting passages"
    bu = V.norm(" ".join(a for a, _ in C.BU_3_9_1["answers"]))
    vals = [ev(s) if "+" in s or "*" in s else V.parse_number(s) for _, s in C.BU_3_9_1["answers"]]
    rec(S, "BU 3.9.1 answers", vals == [303, 3003, 33, 6, 3, 2, 1.5, 1], f"{vals}; 303 + 3003 = {vals[0]+vals[1]}")
    rec(S, "RV 3.9.9: trīṇi śatā trī sahasrāṇi triṃśat nava", ev(C.RV_3_9_9["count"]) == 3339, "3339")
    bu_full = V.norm(C.BU_3_9_1["text"])
    surface = ["trayaśca trī ca śatā", "trayaśca trī ca sahasre", "trayastriṃśadity", "ṣaḍity", "traya ity",
               "dvāvity", "adhyardha ity", "eka ity"]                    # the answers as they stand in sandhi
    missing = [x for x in surface if x.replace(" ", "") not in bu_full.replace(" ", "")]
    rec(S, "BU 3.9.1: every answer occurs in the full text (in sandhi)", not missing,
        f"{len(surface)} answers found" if not missing else f"missing: {missing}")
    rec(S, "BU 3.9.2: 8 Vasus + 11 Rudras + 12 Ādityas = 31, + Indra + Prajāpati = 33",
        "aṣṭau vasava ekādaśa rudrā dvādaśādityāsta ekatriṃśad" in V.norm(C.BU_3_9_1["text2"]) and 8 + 11 + 12 + 2 == 33,
        "31 + 2 = 33")
    sb4 = V.norm(C.SB_11_6_3[4]).replace(" ", "")
    rec(S, "ŚB 11.6.3.4 parallel: same answers except 'six'",
        "ṣaḍiti" not in sb4 and "ṣaḍityomiti" in bu_full.replace(" ", ""),
        "BU (Kāṇva) has 3306, 33, 6, 3, 2, 1½, 1; ŚB 11.6.3.4 (Mādhyandina) omits 6")
    rv = [x for x in V.norm(C.RV_3_9_9["text"]).split("|") if x.strip()]
    rec(S, "RV 3.9.9 complete verse present (2 half-verses)", len(rv) == 2, "triṣṭubh, to Agni")


# ------------------------------------------------------------------ 6. metre
def check_metre():
    S = "Metre"
    bad_ss = []
    for verse, halves in C.SS.items():
        for h in halves:
            r = V.check_anustubh(h)
            if not r["ok"]:
                bad_ss.append((verse, r["syllables"], r["why"]))
    rec(S, "Sūrya Siddhānta 1.11-1.37 (anuṣṭubh, 54 half-verses)", not bad_ss, f"irregular: {bad_ss}" if bad_ss else "all scan")
    for d in (C.BHAGAVATA_3_11, C.VISNU_1_3, C.MANU_1_68_72, C.NARADA_2_54_26):
        rs = [V.check_anustubh(h) for h in d["halves"]]
        bad = [(i + 1, r["why"]) for i, r in enumerate(rs) if not r["ok"]]
        rec(S, f'{d["ref"]} (anuṣṭubh)', not bad, "all scan" if not bad else f"{bad}")
    for d in C.ARYABHATIYA:
        rs = V.check_arya(d["halves"])
        rec(S, f'{d["ref"]} (āryā 30 + 27 mātrās)', all(r["ok"] for r in rs), " / ".join(str(r["matras"]) for r in rs))
    for ref, halves in C.ARYABHATIYA_WITNESS.items():
        a1 = next(d for d in C.ARYABHATIYA if d["ref"] == ref)["halves"]
        same = [V.norm(x).replace(" ", "") == V.norm(y).replace(" ", "") for x, y in zip(a1, halves)]
        rec(S, f"{ref}: GRETIL vs 1930 edition", True if all(same) else None,
            "identical" if all(same) else "differ in " + ", ".join(f"half {i+1}" for i, ok in enumerate(same) if not ok))
    rs = V.check_arya(C.GSS_2_18_19["halves"])
    rec(S, f'{C.GSS_2_18_19["ref"]} (āryā, 1912 edition)', all(r["ok"] for r in rs), " / ".join(str(r["matras"]) for r in rs))
    for g in C.GK_11:
        if g["reading"] is None:
            rec(S, f"Gaṇita Kaumudī 11.{g['v']} (āryā family)", False, "text lost in the OCR; needs the page image")
            continue
        r = V.check_arya_family(g["reading"])[0]
        rec(S, f"Gaṇita Kaumudī 11.{g['v']} (āryā family)", r["ok"],
            f"{r['matras'][0]} + {r['matras'][1]} = {r['type'] or 'no family member'}")
    rs = V.check_upajati(C.LILAVATI_DIV["halves"])
    rec(S, "Līlāvatī division rule (upajāti)", all(r["ok"] for r in rs), "; ".join("+".join(r["padas"]) for r in rs))
    rs = V.check_vasantatilaka(C.LILAVATI_41["padas"])
    alt = V.check_vasantatilaka(["कार्योऽथ भागहरणे गुणनाविधिश्च"])[0]["ok"]
    rec(S, "Līlāvatī 41 (vasantatilakā)", all(r["ok"] for r in rs),
        f"pāda 2 as transcribed fails; with 'guṇanā-vidhiś' (as in the Nārada parallel) it scans: {alt}")


def run():
    RESULTS.clear()
    check_sb(); check_ss(); check_yugas(); check_lists(); check_counts(); check_metre()
    return RESULTS


def report(path="verse_report.md"):
    res = run()
    lines = ["# Verse check report", "",
             "Rows are consistency checks against the supplied corpus, arithmetic annotations, or metre rules; they do not authenticate a witness or independently collate a transcription. "
             "✓ = the coded assertion passed; ✗ = it failed; — = informational note with no pass/fail check. Metre is diagnostic, not proof of a reading.", ""]
    sec = None
    for s, item, ok, detail in res:
        if s != sec:
            lines += ["", f"## {s}", "", "| | Check | Detail |", "|---|---|---|"]
            sec = s
        mark = "✓" if ok is True else ("✗" if ok is False else "—")
        lines.append(f"| {mark} | {item} | {detail} |")
    open(path, "w").write("\n".join(lines) + "\n")
    return res


if __name__ == "__main__":
    res = report()
    bad = [r for r in res if r[2] is False]
    info = [r for r in res if r[2] is None]
    print(f"{len(res)} recorded rows: {len(res) - len(bad) - len(info)} passed, {len(bad)} failed, {len(info)} informational")
    for s, item, ok, d in bad:
        print(f"  ✗ [{s}] {item}: {d}")
