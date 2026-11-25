"""Every Sanskrit passage the blocks rely on, with its source and retrieval status.

status values
  "sanskrit"      Sanskrit text retrieved from the named source
  "sanskrit-frag" Sanskrit retrieved for part of the passage only
  "scan-reading"  a reading of a manuscript/edition scan, not yet collated
  "translation"   only a translation of the verse is available here
Text is stored exactly as retrieved (Devanagari or IAST); vtools normalises it.
"""

SRC = {
    "weber_sb": "Weber (ed.), Śatapatha-Brāhmaṇa, Mādhyandina, Berlin 1849; unaccented text from https://github.com/vishvAsa/vedAH_yajuH (CC BY 4.0)",
    "vishvasa_bu": "Bṛhadāraṇyaka Upaniṣad (Kāṇva), 3.9 Śākalya-brāhmaṇa, from https://github.com/vishvAsa/vedAH_yajuH (upstream dvaitavedanta.in)",
    "vishvasa_rv": "Ṛgveda (Śākala) 3.9.9, saṃhitā text from https://github.com/vishvAsa/vedAH_Rk",
    "sambasiva_ab": "Āryabhaṭīya with Nīlakaṇṭha's commentary, ed. K. Sāmbaśiva Śāstrī, Trivandrum 1930, via https://github.com/vishvAsa/jyotiSham",
    "rangacharya_gss": "Gaṇitasārasaṅgraha, ed. M. Raṅgācārya, Madras 1912, via https://github.com/vishvAsa/jyotiSham",
    "dvivedi_gk": "Gaṇita Kaumudī, ed. Padmākara Dvivedī, Part II, Benares 1942; OCR at https://archive.org/stream/in.ernet.dli.2015.326039/2015.326039.Ganita-Kaumudi_djvu.txt",
    "gretil_ss": "https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/html/sa_sUryasiddhAnta.htm",
    "gretil_ab": "https://zenodo.org/records/6466333/files/sa_AryabhaTa-AryabhaTIya-comm.txt (GRETIL)",
    "keller_ab": "https://halshs.archives-ouvertes.fr/halshs-01427248v1/file/HistoriographyKuttakaAKPresentation-24-10-2016.pdf",
    "wisdomlib_sb": "https://www.wisdomlib.org/hinduism/book/satapatha-brahmana-sanskrit/ (via search results and user-supplied dossier)",
    "dharmapedia_sb": "https://en.dharmapedia.net/wiki/Shatapatha_Brahmana",
    "eggeling_sb": "https://sacred-texts.com/hin/sbr/sbe43/sbe4362.htm (Sāyaṇa gloss in footnote)",
    "gk_blog": "https://shreevatsa.net/post/narayana-factoring/ (translation of GK ch. 11; scan image 005)",
    "dossier": "user-supplied dossier (Vedshala / sa.wikisource / Gita Press links)",
    "vedapath": "https://vedapath.app/en/narada-purana/purva-bhaga/dvitiya-pada/54/26",
    "indica": "https://www.indica.today/?p=14913",
    "vivekavani": "https://cdn.vivekavani.com/?p=22107",
    "wisdomlib_rv": "https://www.wisdomlib.org/hinduism/book/rig-veda-english-translation/d/doc831657.html",
    "wisdomlib_sb11": "https://www.wisdomlib.org/hinduism/book/satapatha-brahmana-sanskrit/d/doc1057138.html",
}

# ------------------------------------------------------------------ Śatapatha Brāhmaṇa 10.4.2 (complete)
# Weber's edition (1849), unaccented text, via vishvAsa/vedAH_yajuH (CC BY 4.0). All 31 verses.
SB_10_4_2_FULL = {
    1: 'संवत्सरो वै प्रजापतिः अग्निः । सोमो राजा चन्द्रमाः । स ह स्वयमेवात्मानं प्रोचे- यज्ञवचसे राजस्तंबायनाय । यावन्ति वाव मे ज्योतींषि- तावत्यो म इष्टका इति ॥ १ ॥',
    2: 'तस्य वा एतस्य संवत्सरस्य प्रजापतेः सप्त च शतानि विंशतिश्चाहोरात्राणि ज्योतींषि- ता इष्टकाः । षष्टिश्च त्रीणि च शतानि परिश्रितः । षष्टिश्च त्रीणि च शतानि यजुष्मत्यः । सो ऽयं संवत्सरः प्रजापतिः सर्वाणि भूतानि ससृजे- यच्च प्राणि, यच्चाप्राणम् । उभयान्देवमनुष्यान् । स सर्वाणि भूतानि सृष्ट्वा रिरिचानः- इव मेने । स मृत्योर्बिभयां चकार ॥ २ ॥',
    3: 'स हेक्षां चक्रे । कथं न्वहमिमानि सर्वाणि भूतानि पुनरात्मन्नावपेय । पुनरात्मन्दधीय । कथं न्वहमेवैषां सर्वेषां भूतानां पुनरात्मा स्यामिति ॥ ३ ॥',
    4: 'स द्वेधा ऽऽत्मानं व्यौहत्- षष्टिश्च त्रीणि च शतान्यन्यतरस्येष्टका अभवन् । एवमन्यतरस्य । स न व्याप्नोत् ॥ ४ ॥',
    5: 'त्रीनात्मनो ऽकुरुत । तिस्रस्तिस्रो ऽशीतय एकैकस्येष्टका अभवन् । स नैव व्याप्नोत् ॥ ५ ॥',
    6: 'चतुर आत्मनो ऽकुरुत- अशीतिशतेष्टकान् । स नैव व्याप्नोत् ॥ ६ ॥',
    7: 'पञ्चात्मनो ऽकुरुत । चतुश्चत्वारिंशं शतमेकैकस्येष्टका अभवन् । स नैव व्याप्नोत् ॥ ७ ॥',
    8: 'षडात्मनो ऽकुरुत- विंशतिशतेष्टकान् । स नैव व्याप्नोत् । न सप्तधा व्यभवत् ॥ ८ ॥',
    9: 'अष्टावात्मनो ऽकुरुत- नवतीष्टकान् । स नैव व्याप्नोत् ॥ ९ ॥',
    10: 'नवात्मनो ऽकुरुत- अशीतीष्टकान् । स नैव व्याप्नोत् ॥ १० ॥',
    11: 'दशात्मनो ऽकुरुत- द्वासप्ततीष्टकान् । स नैव व्याप्नोत् । नैकादशधा व्यभवत् ॥ ११ ॥',
    12: 'द्वादशात्मनो ऽकुरुत- षष्टीष्टकान् । स नैव व्याप्नोत् । न त्रयोदशधा व्यभवत् । न चतुर्दशधा ॥ १२ ॥',
    13: 'पञ्चदशात्मनो ऽकुरुत-- अष्टाचत्वारिंशदिष्टकान् । स नैव व्याप्नोत् ॥ १३ ॥',
    14: 'षोडशात्मनो ऽकुरुत- पञ्चचत्वारिंशदिष्टकान् । स नैव व्याप्नोत् । न सप्तदशधा व्यभवत् ॥ १४ ॥',
    15: 'अष्टादशात्मनो ऽकुरुत- चत्वारिंशदिष्टकान् । स नैव व्याप्नोत् । नैकान्निविंशतिधा व्यभवत् ॥ १५ ॥',
    16: 'विंशतिमात्मनो ऽकुरुत- षट्त्रिंशदिष्टकान् । स नैव व्याप्नोत् । नैकविंशतिधा व्यभवत् । न द्वाविंशतिधा । न त्रयोविंशतिधा ॥ १६ ॥',
    17: 'चतुर्विंशतिमात्मनो ऽकुरुत- त्रिंशदिष्टकान् । सो ऽत्रातिष्ठत- पञ्चदशे व्यूहे । तद् यत्पञ्चदशे व्यूहे ऽतिष्ठत- तस्मात्पञ्चदशापूर्यमाणस्य रूपाणि । पञ्चदशापक्षीयमाणस्य ॥ १७ ॥',
    18: 'अथ यच्चतुर्विंशतिमात्मनो ऽकुरुत- तस्माच्चतुर्विंशत्यर्धमासः संवत्सरः । स एतैश्चतुर्विंशत्या त्रिंशदिष्टकैरात्मभिर्न व्यभवत् । स पञ्चदशाह्नो रूपाण्यपश्यदात्मनस्तन्वो मुहूर्तान्- लोकम्पृणाः । पञ्चदशैव रात्रेः । तद् यन्मुहुः त्रायन्ते- तस्मान्मुहूर्ताः । अथ यत्क्षुद्राः सन्त इमाल्ँ लोकानापूरयन्ति- तस्माल्लोकम्पृणाः ॥ १८ ॥',
    19: 'एष वा इदं सर्वं पचति- अहोरात्रैः, अर्धमासैः, मासैः, ऋतुभिः, संवत्सरेण । तदमुना पक्वमयं पचति । पक्वस्य पक्तेति ह स्माह भारद्वाजो ऽग्निम् । अमुना हि पक्वमयं पचतीति ॥ १९ ॥',
    20: 'तानि सम्वत्सरे दश च सहस्राणि, अष्टौ च शतानि समपद्यन्त । सो ऽत्रातिष्ठत- दशसु च सहस्रेषु, अष्टासु च शतेषु ॥ २० ॥',
    21: 'अथ सर्वाणि भूतानि पर्यैक्षत् । स त्रय्यामेव विद्यायां सर्वाणि भूतान्यपश्यत् । अत्र हि सर्वेषां छन्दसामात्मा । सर्वेषां स्तोमानाम् । सर्वेषां प्राणानाम् । सर्वेषां देवानाम् । एतद्वा अस्त्येतद्ध्यमृतम् । यद्ध्यमृतं तद्ध्यस्ति । एतदु तद् यन्मर्त्यम् ॥ २१ ॥',
    22: 'स ऐक्षत प्रजापतिः । त्रय्यां वाव विद्यायां सर्वाणि भूतानि । हन्त त्रयीमेव विद्यामात्मानमभिसंस्करवा इति ॥ २२ ॥',
    23: 'स ऋचो व्यौहत्- द्वादश बृहतीसहस्राणि । एतावत्यो हर्चो याः प्रजापतिसृष्टाः । तास्त्रिंशत्तमे व्यूहे पङ्क्तिष्वतिष्ठन्त । ता यत्त्रिंशत्तमे व्यूहे ऽतिष्ठन्त । तस्मात्त्रिंशन्मासस्य रात्रयः । अथ यत्पङ्क्तिषु- तस्मात्पाङ्क्तः प्रजापतिः । ता अष्टाशतं शतानि पङ्क्तयो ऽभवन् ॥ २३ ॥',
    24: 'अथेतरौ वेदौ व्यौहत्- द्वादशैव बृहतीसहस्राणि । अष्टौ यजुषाम् । चत्वारि साम्नाम् । एतावद्धैतयोर्वेदयोर्यत्प्रजापतिसृष्टम् । तौ त्रिंशत्तमे व्यूहे पङ्क्तिष्वतिष्ठेताम् । तौ यत्त्रिंशत्तमे व्यूहे ऽतिष्ठेताम्- तस्मात्त्रिंशन्मासस्य रात्रयः । अथ यत्पङ्क्तिषु- तस्मात्पाङ्क्तः प्रजापतिः । ता अष्टाशतमेव शतानि पङ्क्तयो ऽभवन् ॥ २४ ॥',
    25: 'ते सर्वे त्रयो वेदाः दश च सहस्राण्यष्टौ च शतान्यशीतीनामभवन् । स मुहूर्तेन- मुहूर्तेनाशीतिमाप्नोत् । मुहूर्तेन मुहूर्तेनाशीतिः समपद्यत ॥ २५ ॥',
    26: 'स एषु त्रिषु लोकेषूखायां योनौ रेतोभूतमात्मानमसिञ्चत्- छन्दोमयम्, स्तोममयम्, प्राणमयम्, देवतामयम् । तस्यार्धमासे प्रथम आत्मा समस्क्रियत । दवीयसि परः । दवीयसि परः । सम्वत्सर एव सर्वः कृत्स्नः समस्क्रियत ॥ २६ ॥',
    27: 'तद् यत्परिश्रितमुपाधत्त- तद्रात्रिमुपाधत्त । तदनु पञ्चदश मुहूर्तान् । मुहूर्ताननु पञ्चदशाशीतीः । अथ यद्यजुष्मतीमुपाधत्त- तदहरुपाधत्त । तदनु पञ्चदश मुहूर्तान् । मुहूर्ताननु पञ्चदशाशीतीः । एवमेतां त्रयीं विद्यामात्मन्नावपत । आत्मन्नकुरुत । सो ऽत्रैव सर्वेषां भूतानामात्मा ऽभवत्- छन्दोमयः, स्तोममयः, प्राणमयः, देवतामयः । स एतन्मय एव भृत्वोर्ध्व उदक्रामत् । स यः स उदक्रामद्- एष स चन्द्रमाः ॥ २७ ॥',
    28: 'तस्यैषा प्रतिष्ठा य एष तपति, एतस्मादेवाध्यचीयत । एतस्मिन्नध्यचीयत । आत्मन एवैनं तन्निरमिमीत । आत्मनः प्राजनयत् ॥ २८ ॥',
    29: 'स यदग्निं चेष्यमाणो दीक्षते- यथैव तत्प्रजापतिरेषु त्रिषु लोकेषूखायां योनौ रेतोभूतमात्मानमसिञ्चत्- एवमेवैष एतदात्मानमुखायां योनौ रेतोभूतं सिञ्चति- छन्दोमयम्, स्तोममयम्, प्राणमयम्, देवतामयम् । तस्यार्द्धमासे प्रथम आत्मा संस्क्रियते, दवीयसि परः, दवीयसि परः । संवत्सर एव सर्वः कृत्स्नः संस्क्रियते ॥ २९ ॥',
    30: 'तद् यत्परिश्रितमुपधत्ते- तद्रात्रिमुपधत्ते । तदनु पञ्चदश मुहूर्तान् । मुहूर्ताननु पञ्चदशाशीतीः । अथ यद्यजुष्मतीमुपधत्ते- तदहरुपधत्ते । तदनु पञ्चदश मुहूर्तान् । मुहूर्ताननु पञ्चदशाशीतीः । एवमेतां त्रयीं विद्यामात्मन्नावपते, आत्मन् कुरुते । सो ऽत्रैव सर्वेषां भूतानामात्मा भवति- छन्दोमयः, स्तोममयः, प्राणमयः, देवतामयः । स एतन्मय एव भूत्वोर्ध्व उत्क्रामति ॥ ३० ॥',
    31: 'तस्यैषा प्रतिष्ठा- य एष तपति- एतस्माद्वेवाधिचीयते । एतस्मिन्नधिचीयते, आत्मन एवैनं तन्निर्मिमीते, आत्मनः प्रजनयति । स यदैवंविदस्माल्लोकात्प्रैति- अथैतमेवात्मानमभिसम्भवति- छन्दोमयम्, स्तोममयम्, प्राणमयम्, देवतामयम् । स एतन्मय एव भूत्वोर्ध्व उत्क्रामति- य एवं विद्वानेतत्कर्म कुरुते, यो वैतदेवं वेद ॥ ३१ ॥',
}
# the division series, with spans for checking: (surface span, base word / structure)
SB_10_4_2 = [
    dict(ref="ŚB 10.4.2.4", status="sanskrit", src="weber_sb", text=SB_10_4_2_FULL[4],
         bodies=('dvedhā', 'dvi'), bricks=('ṣaṣṭiśca trīṇi ca śatāny', 'ṣaṣṭi + tri * śata'), fails=[]),
    dict(ref="ŚB 10.4.2.5", status="sanskrit", src="weber_sb", text=SB_10_4_2_FULL[5],
         bodies=('trīn', 'tri'), bricks=("tisrastisro 'śītaya", 'tri * aśīti'), fails=[]),
    dict(ref="ŚB 10.4.2.6", status="sanskrit", src="weber_sb", text=SB_10_4_2_FULL[6],
         bodies=('catura', 'catur'), bricks=('aśītiśate', 'aśīti + śata'), fails=[]),
    dict(ref="ŚB 10.4.2.7", status="sanskrit", src="weber_sb", text=SB_10_4_2_FULL[7],
         bodies=('pañcā', 'pañca'), bricks=('catuścatvāriṃśaṃ śatam', 'catuścatvāriṃśat + śata'), fails=[]),
    dict(ref="ŚB 10.4.2.8", status="sanskrit", src="weber_sb", text=SB_10_4_2_FULL[8],
         bodies=('ṣaḍ', 'ṣaṭ'), bricks=('viṃśatiśate', 'viṃśati + śata'), fails=[('na saptadhā', 'sapta')]),
    dict(ref="ŚB 10.4.2.9", status="sanskrit", src="weber_sb", text=SB_10_4_2_FULL[9],
         bodies=('aṣṭā', 'aṣṭau'), bricks=('navatī', 'navati'), fails=[]),
    dict(ref="ŚB 10.4.2.10", status="sanskrit", src="weber_sb", text=SB_10_4_2_FULL[10],
         bodies=('navā', 'nava'), bricks=('aśītī', 'aśīti'), fails=[]),
    dict(ref="ŚB 10.4.2.11", status="sanskrit", src="weber_sb", text=SB_10_4_2_FULL[11],
         bodies=('daśā', 'daśa'), bricks=('dvāsaptatī', 'dvāsaptati'), fails=[('naikādaśadhā', 'ekādaśa')]),
    dict(ref="ŚB 10.4.2.12", status="sanskrit", src="weber_sb", text=SB_10_4_2_FULL[12],
         bodies=('dvādaśā', 'dvādaśa'), bricks=('ṣaṣṭī', 'ṣaṣṭi'), fails=[('na trayodaśadhā', 'trayodaśa'), ('na caturdaśadhā', 'caturdaśa')]),
    dict(ref="ŚB 10.4.2.13", status="sanskrit", src="weber_sb", text=SB_10_4_2_FULL[13],
         bodies=('pañcadaśā', 'pañcadaśa'), bricks=('aṣṭācatvāriṃśad', 'aṣṭācatvāriṃśat'), fails=[]),
    dict(ref="ŚB 10.4.2.14", status="sanskrit", src="weber_sb", text=SB_10_4_2_FULL[14],
         bodies=('ṣoḍaśā', 'ṣoḍaśa'), bricks=('pañcacatvāriṃśad', 'pañcacatvāriṃśat'), fails=[('na saptadaśadhā', 'saptadaśa')]),
    dict(ref="ŚB 10.4.2.15", status="sanskrit", src="weber_sb", text=SB_10_4_2_FULL[15],
         bodies=('aṣṭādaśā', 'aṣṭādaśa'), bricks=('catvāriṃśad', 'catvāriṃśat'), fails=[('naikānniviṃśatidhā', 'ekānnaviṃśati')], note='Weber reads ekānni-viṃśati (for the usual ekānna-); same number, 19.'),
    dict(ref="ŚB 10.4.2.16", status="sanskrit", src="weber_sb", text=SB_10_4_2_FULL[16],
         bodies=('viṃśatim', 'viṃśati'), bricks=('ṣaṭtriṃśad', 'ṣaṭtriṃśat'), fails=[('naikaviṃśatidhā', 'ekaviṃśati'), ('na dvāviṃśatidhā', 'dvāviṃśati'), ('na trayoviṃśatidhā', 'trayoviṃśati')]),
    dict(ref="ŚB 10.4.2.17", status="sanskrit", src="weber_sb", text=SB_10_4_2_FULL[17],
         bodies=('caturviṃśatim', 'caturviṃśati'), bricks=('triṃśad', 'triṃśat'), fails=[], note="No 'sa naiva vyāpnot' here: he stood (atiṣṭhata) in the fifteen-fold arrangement. The series ends."),
]
# ŚB 11.6.3.4-5 (Mādhyandina): Śākalya's question, the same dialogue as Bṛhadāraṇyaka 3.9.1-2
SB_11_6_3 = {4: 'स होवाच- कति देवा याज्ञवल्क्य ! इति, त्रयश्च त्री च शता त्रयश्च त्री च सहस्रेति, ओमिति होवाच । कत्येव देवा याज्ञवल्क्य ! इति त्रयस्त्रिँ शदिति, ओमिति होवाच । कत्येव देवा याज्ञवल्क्य ! इति, त्रय इति, ओमिति होवाच । कत्येव देवा याज्ञवल्क्य ! इति, द्वाविति, ओमिति होवाच । कत्येव देवा याज्ञवल्क्य ! इति, अध्यर्द्ध इति, ओमिति होवाच । कत्येव देवा याज्ञवल्क्य ! इति, एक इति, ओमिति होवाच । कतमे ते त्रयश्च त्री च शता त्रयश्च त्री च सहस्रेति ॥ ४ ॥',
             5: 'स होवाच- महिमान एवैषामेते, त्रयस्त्रिंशत्त्वेव देवा इति । कतमे ते त्रयस्त्रिंशदिति । अष्टौ वसवः, एकादश रुद्राः, द्वादशादित्याः, त एकत्रिंशत् । इंद्रश्चैव प्रजापतिश्च त्रयस्त्रिंशाविति ॥ ५ ॥'}

# ------------------------------------------------------------------ Āryabhaṭīya
ARYABHATIYA = [
    dict(ref="Āryabhaṭīya 2.4", status="sanskrit", src="gretil_ab", metre="arya",
         halves=["bhāgam haret avargāt nityam dviguṇena vargamūlena",
                 "vargāt varge śuddhe labdham sthānāntare mūlam"],
         role="vargamūla: square root by alternate (varga / avarga) places"),
    dict(ref="Āryabhaṭīya 2.32", status="sanskrit", src="keller_ab", metre="arya",
         halves=["adhikāgrabhāgahāraṃ chindyād ūnāgrabhāgahāreṇa",
                 "śeṣaparasparabhaktaṃ matiguṇam agrāntare kṣiptam"],
         role="mutual division of remainders (kuṭṭaka)"),
]
ARYABHATIYA.append(
    dict(ref="Āryabhaṭīya 2.33", status="sanskrit", src="sambasiva_ab", metre="arya",
         halves=["अधउपरिगुणितमन्त्ययुगूनाग्रच्छेदभाजिते शेषम्",
                 "अधिकाग्रच्छेदगुणं द्विच्छेदाग्रमधिकाग्रयुतम्"],
         role="rest of the kuṭṭaka (not used by the blocks)"))
# second witness for 2.4 and 2.32 (Sāmbaśiva Śāstrī 1930), as printed
ARYABHATIYA_WITNESS = {
    "Āryabhaṭīya 2.4": ["भागं हरेवर्गान्नित्यं द्विगुणेन वर्गमूलेन", "वर्गाद् वर्गे शुद्धे लब्धं स्थानान्तरे मूलम्"],
    "Āryabhaṭīya 2.32": ["अधिकाग्रभागहारं छिन्द्यादूनाग्रभागहारेण", "शेषपरस्परभक्तं मतिगुणमग्रान्तरे क्षिप्तम्"],
}
BHASKARA_I = [  # commentary on the kuṭṭaka examples, GRETIL text
    "bhāgahārabhājyāgrāṇām ekena apavartanacchedena apavartanam kṛtvā pūrvavat kuṭṭākāraḥ kriyate",
    "etābhyām apavartitabhāgahārābhyām apavartitāgrāntareṇa kuṭṭākāraḥ labdhaḥ",
    "etayoḥ chedāgrāntarāṇām anena 210389 apavartanam kṛtvā sthāpanā",
]

# ------------------------------------------------------------------ Gaṇita Kaumudī ch. 11
GK_11_3 = dict(ref="Gaṇita Kaumudī 11.3", status="ocr-reading", src="dvivedi_gk", metre="arya-family",
               text="न समो भाज्यः प्रथमस्तस्मिन् यदि पञ्चकः स्थाने ।\nअच्छेद्याः कल्प्यन्ते त्रिसप्तकैकादशादयश्छेदाः ॥",
               blog_reading="न समो भाज्यः प्रथमस्तस्मिन् यदि पञ्चकं स्थाने ।\nअच्छेद्याः कल्प्यन्ते त्रिसप्तैकादशादयश्छेदाः ॥")

# Gaṇita Kaumudī ch. 11 (bhāgādāna), edition numbering (Dvivedī 1942).
# The supplied OCR has 11 numbered entries, but v9 is incomplete and the readings have
# not been collated line-by-line against the page images. Do not cite this as a complete
# verified transcription.
# ocr      : the archive.org OCR line as transcribed by a fetch tool (not checked against the page image)
# reading  : our restoration of that line (spelling only; doubtful words marked in note)
# blog     : the verse label used earlier from the blog's scan-image numbers
GK_11 = [
    dict(v=1, blog="—", ocr="अथ गणंकानन्दकरं भागादानस्य कोतुकं वक्ष्ये । ज्ञाते यस्मिन् सपदि सामान्यो जायते गणकः ॥ १ ॥",
         reading=["अथ गणकानन्दकरं भागादानस्य कौतुकं वक्ष्ये", "ज्ञाते यस्मिन् सपदि सामान्यो जायते गणकः"],
         block=None, note="Half 2 is one mātrā short as restored: a word may be lost in the OCR."),
    dict(v=2, blog="v2", ocr="प्रसक्रद् विभजेद् द्वाभ्यां समराशिं यावदेति वैषम्यम् । सत्सु प्रथमस्थाने पञ्चसु भाग्ये च पञ्चभिश्छिन्यात् ॥२॥",
         reading=["असकृद् विभजेद् द्वाभ्यां समराशिं यावदेति वैषम्यम्", "सत्सु प्रथमस्थाने पञ्चसु भाज्ये च पञ्चभिश्छिन्द्यात्"],
         block="sama, pancaka_sthane, asakrd_bhaga", note="'satsu … pañcasu' kept as the OCR has it; it scans (gīti)."),
    dict(v=3, blog="v3", ocr="न समो भाञ्यः पथमः तस्मिन् यदि पञ्चकः स्थाने । घ्रच्छेव्याः कल्प्यन्ते | त्रिसप्तकेकादशादयश्छेदाः ॥ २ ॥",
         reading=["न समो भाज्यः प्रथमस्तस्मिन् यदि पञ्चकः स्थाने", "अच्छेद्याः कल्प्यन्ते त्रिसप्तकैकादशादयश्छेदाः"],
         block="gk_trial", note="OCR mislabels it ॥ २ ॥. Differs from the blog reading in pañcakaḥ and tri-saptaka-."),
    dict(v=4, blog="v4 + v5", ocr="यावच्ेदप्राभि- स्तावद् ह्रसाधनं क्रियते । भाज्यो वगेश्चेत् त- न्मूलं छेदो दह्विधा भवति ॥ ४ ॥",
         reading=["यावच्छेदप्राप्तिस्तावद्धरसाधनं क्रियते", "भाज्यो वर्गश्चेत् तन्मूलं छेदो द्विधा भवति"],
         block="gk_trial (continue), is_varga", note="'hara-sādhanam' restored from OCR 'ह्रसाधनं'."),
    dict(v=5, blog="v6", ocr="द्मपदपदस्तु भाज्यः कयेष्टक्त्या युतात् पदं भाज्यात् । पदयोः सय॒ुतिषियुती हारो परिकत्पितौ भाज्यो ॥ ५ ॥",
         reading=["अपदप्रदस्तु भाज्यः कयेष्टकृत्या युतात् पदं भाज्यात्", "पदयोः संयुतिवियुती हारौ परिकल्पितौ भाज्ये"],
         block="vargantara", note=""),
    dict(v=6, blog="v7 + v8", ocr="राश्योस्तु तयोः प्राग्वत् कुर्वीतच्छदशोधनं सुधिया । श्मपदप्रदस्य राशेः पदमासन्नं द्विसङ्कणं सेकम् ॥ £ ॥",
         reading=["राश्योस्तु तयोः प्राग्वत् कुर्वीतच्छेदशोधनं सुधिया", "अपदप्रदस्य राशेः पदमासन्नं द्विसङ्गुणं सैकम्"],
         block="bhagadana (recurse), vargantara (2m+1)", note=""),
    dict(v=7, blog="v8-9 + v10", ocr="मूलावशोषहीनं वगेश्चेत सेपकश्च कुतिसिद्ध्ये । वर्गो न भवेत् पूवा सन्नपदं दिगुणितं चरिसंयुक्तम् ॥५॥",
         reading=["मूलावशेषहीनं वर्गश्चेत् क्षेपकश्च कृतिसिद्ध्यै", "वर्गो न भवेत् पूर्वासन्नपदं द्विगुणितं त्रिसंयुक्तम्"],
         block="vargantara (2m+1−r, then 2m+3)", note="OCR mislabels it ॥५॥."),
    dict(v=8, blog="v10-11 + v12", ocr="्रादादयुत्तरव्द्धचा तावद् यावद् भवेद् वगेः । असमानां पृवेहताः परे पुरःस्थास्तथा चान्ये ॥ ८ ॥",
         reading=["आद्यं द्व्युत्तरवृद्ध्या तावद् यावद् भवेद् वर्गः", "असमानां पूर्वहताः परे पुरःस्थास्तथा चान्ये"],
         block="vargantara (+2 each step), sarva_hara", note="The opening word is badly damaged in the OCR; 'ādyaṃ dvyuttara-' is a guess that fits sense and metre."),
    dict(v=9, blog="v12 + v20", ocr="तुल्यानां पवनः परः प्रथक् तेऽन्यदहरनिघ्नाः ॥८५५॥",
         reading=None, block="sarva_hara, m_minus_x",
         note="Only one damaged half-line survives in the OCR. The rest of v9 (end of the all-divisors rule and the "
              "start of the 'nearest root less a chosen number' rule) is lost. Needs the page image."),
    dict(v=10, blog="v21", ocr="हारद्ता चेच्छुद्धयति तेनाऽवश्यं इतो भान्यः । न विशुद्धयति चेदिष्ठं स्वधिया परिकस्पयेदन्यत् ॥ १० ॥",
         reading=["हारहृता चेच्छुद्ध्यति तेनावश्यं हृतो भाज्यः", "न विशुद्ध्यति चेदिष्टं स्वधिया परिकल्पयेदन्यत्"],
         block="m_minus_x", note="Its subject ('the nearest root less a chosen number') was in the lost part of v9."),
    dict(v=11, blog="v23-24", ocr="इट तयुश्ययुणका- वशेषधातस्तथेष्टह्ृ्डेषम् । तुल्यं चेदिष्ट दूति- शेषेण स्यात् स्फुटाऽत्र हतिः ॥११॥",
         reading=["इष्टहृतगुण्यगुणकावशेषघातस्तथेष्टहृच्छेषम्", "तुल्यं चेदिष्टहृतिशेषेण स्यात् स्फुटात्र हतिः"],
         block="sesha_pariksa", note="Half 2 is one mātrā short as restored: a syllable may be lost in the OCR."),
]
GK_11_RULES = {  # translation only (blog, by scan image); verse numbering = image - 2
    "v2 (img 004)": "Repeatedly divide an even number by 2 until it becomes odd; if 5 is in the units place, divide by 5.",
    "v3 (img 005)": "Try the acchedyas 3, 7, 11, etc. as divisors.",
    "v4 (img 006)": "While you find divisors, keep finding divisors. [no stopping rule]",
    "v5 (img 007)": "If N is a square, its root is a factor, twice.",
    "v6 (img 008)": "A non-square added to some square becomes a square; sum and difference of the roots are factors.",
    "v7 (img 009)": "Of these numbers, as before, find factors.",
    "v8-9 (img 010-011)": "Nearest root m of N = m^2 + r: double it, add 1, subtract r; if a square, that is the number to add.",
    "v10-11 (img 012-013)": "If not, add 2m+3, then 2m+5 ... in arithmetic progression until a square is reached.",
    "v12 (img 014)": "All divisors: put previous products in front of each new divisor, and again separately.",
    "v20-21 (img 022-023)": "Nearest root minus a chosen number is a divisor [when it divides]; else choose differently.",
    "v23-24 (img 025-026)": "Check a product by remainders of both factors by a chosen number.",
}
GK_EXERCISES = {  # (blog images 015-027)
    "2048": 2048, "3125": 3125, "7250 (text) / 7520 (blog notes)": (7250, 7520), "10201": 10201,
    "1161": 1161, "1001": 1001, "4620": 4620, "3927": 3927, "120": 120, "231": 231,
    "check 29 x 17 = 493": (29, 17, 493),
}

# ------------------------------------------------------------------ Līlāvatī, Gaṇitasārasaṅgraha, Nārada P.
LILAVATI_DIV = dict(ref="Līlāvatī (division rule)", status="sanskrit", src="dossier", metre="upajati",
                    halves=["भाज्याद्धरः शुध्यति यद्गुणः स्यात् अन्त्यात् फलं तत् खलु भागहारे",
                            "समेन केनाप्यपवर्त्य हार- भाज्यौ भजेद्वा सति संभवे तु"])
LILAVATI_41 = dict(ref="Līlāvatī 41 (fraction division)", status="sanskrit-frag", src="dossier",
                   metre="vasantatilaka",
                   padas=["छेदं लवं च परिवर्त्य हरस्य शेषः", "कार्योऽथ भागहरणे गुणनविधिश्च"])
GSS_2_18_19 = dict(ref="Gaṇitasārasaṅgraha 2.18-19", status="sanskrit", src="rangacharya_gss", metre="arya",
                   halves=["विन्यस्य भाज्यमानं तस्याधस्स्थेन भागहारेण", "सदृशापवर्तविधिना भागं कृत्वा फलं प्रवदेत्",
                           "प्रतिलोमपथेन भजेद्भाज्यमधस्स्थेन भागहारेण", "सदृशापवर्तनविधिर्यद्यस्ति विधाय तमपि तयोः"],
                   note="Text of the 1912 edition. The dossier copy read सदृशपवर्त in 2.18 (one mātrā short); "
                        "the edition reads सदृशापवर्त, which scans. The edition notes that 2.18 is missing in manuscript P.")
NARADA_2_54_26 = dict(ref="Nārada Purāṇa Pūrva 2.54.26", status="sanskrit", src="vedapath", metre="anustubh",
                      halves=["छेदं चापि लवं विद्वन्परिवर्त्य हरस्य च", "शेषः कार्यो भागहारे कर्तव्यो गुणनाविधिः"])
PINGALA_8_28_31 = dict(ref="Chandaḥśāstra 8.28-31", status="sanskrit", src="indica", metre=None,
                       text="द्विरर्धे | रुपे शून्यम् | द्विः शून्ये | तावदर्धे तद्गुणितम्",
                       note="Source prints रुपे; standard reading रूपे.")

# ------------------------------------------------------------------ Sūrya Siddhānta 1.11-1.37 (GRETIL)
SS = {
    "1.11": ["prāṇādiH kathito mūrtas truṭyādyo +amūrtasaṃjñakaH/", "ṣaḍbhiH prāṇair vināḍī syāt tatṣaṣṭyā nāḍikā smṛtā//"],
    "1.12": ["nāḍīṣaṣṭyā tu nākṣatram ahorātraṃ prakīrtitam/", "tattriṃśatā bhaven māsaH sāvano +arkodayais tathā//"],
    "1.13": ["aindavas tithibhis tadvat saṃkrāntyā saura ucyate/", "māsair dvādaśabhir varṣaṃ divyaṃ tad aha ucyate//"],
    "1.14": ["surāsurāṇām anyonyam ahorātraṃ viparyayāt/", "tatṣaṣṭiH ṣaḍguṇā divyaṃ varṣam āsuram eva ca//"],
    "1.15": ["taddvādaśasahasrāṇi caturyugam udāhṛtam/", "sūryābdasaṃkhyayā dvitrisāgarair ayutāhataiH//"],
    "1.16": ["sandhyāsandhyāṃśasahitaṃ vijñeyaṃ taccaturyugam/", "kṛtādīnāṃ vyavastheyaṃ dharmapādavyavasthayā//"],
    "1.17": ["yugasya daśamo bhāgaś catustridvyekasaṅguṇaH/", "kramāt kṛtayugādīnāṃ ṣaṣṭhāṃśaH sandhyayoH svakaH//"],
    "1.18": ["yugānāṃ saptatiH saikā manvantaram ihocyate/", "kṛtābdasaṃkhyās tasyānte sandhiH prokto jalaplavaH//"],
    "1.19": ["sasandhayas te manavaH kalpe jñeyās caturdaśa/", "kṛtapramāṇaH kalpādau sandhiH pañcadaśaH smṛtaH//"],
    "1.20": ["ittham yugasahasreṇa bhūtasaṃhārakārakaH/", "kalpo brāhmam ahaH proktaṃ śarvarī tasya tāvatī//"],
    "1.21": ["paramāyuH śataṃ tasya tayāhorātrasaṃkhyayā/", "āyuṣo +ardhamitaṃ tasya śeṣakalpo +ayam ādimaH//"],
    "1.22": ["kalpād asmāc ca manavaH ṣaḍ vyatītāH sasandhayaH/", "vaivasvatasya ca manor yugānāṃ trighano gataH//"],
    "1.23": ["aṣṭāviṃśād yugād asmād yātam etat kṛtaṃ yugam/", "ataH kālaṃ prasaṃkhyāya saṃkhyām ekatra piṇḍayet//"],
    "1.24": ["graharkṣadevadaityādi sṛjato +asya carācaram/", "kṛtādrivedā divyābdāH śataghnā vedhaso gatāH//"],
    "1.25": ["paścād vrajanto +atijavān nakṣatraiH satataṃ grahāH/", "jīyamānās tu lambante tulyam eva svamārgagāH//"],
    "1.26": ["prāggatitvam atas teṣāṃ bhagaṇaiH pratyahaṃ gatiH/", "pariṇāhavaśād bhinnā tadvaśād bhāni bhuñjate//"],
    "1.27": ["śīghragas tāny athālpena kālena mahatālpagaH/", "teṣāṃ tu parivartena pauṣṇānte bhagaṇaH smṛtaH//"],
    "1.28": ["vikalānāṃ kalā ṣaṣṭyā tatṣaṣṭyā bhāga ucyate/", "tattriṃśatā bhaved rāśir bhagaṇo dvādaśaiva te//"],
    "1.29": ["yuge sūryajñaśukrāṇām khacatuṣkaradārṇavāH/", "kujārkiguruśīghrāṇāṃ bhagaṇāH pūrvayāyinām//"],
    "1.30": ["indo rasāgnitritrīṣusaptabhūdharamārgaṇāH/", "dasratryaṣṭarasāṅkākṣilocanāni kujasya tu//"],
    "1.31": ["budhaśīghrasya śūnyartukhādritryaṅkanagendavaH/", "bṛhaspateH khadasrākṣivedaṣaḍvahnayas tathā//"],
    "1.32": ["sitaśīghrasya ṣaṭsaptatriyamāśvikhabhūdharāH/", "śaner bhujaṅgaṣaṭpañcarasavedaniśākarāH//"],
    "1.33": ["candroccasyāgniśūnyāśvivasusarpārṇavā yuge/", "vāmaṃ pātasya vasvagniyamāśviśikhidasrakāH//"],
    "1.34": ["bhānām aṣṭākṣivasvadritridvidvyaṣṭaśarendavaH/", "bhodayā bhagaṇaiH svaiH svair ūnāH svasvodayā yuge//"],
    "1.35": ["bhavanti śaśino māsāH sūryendubhagaṇāntaram/", "ravimāsonitās te tu śeṣāH syur adhimāsakāH//"],
    "1.36": ["sāvahāhāni cāndrebhyo dyubhyaH projjhya tithikṣayāH/", "udayād udayaṃ bhānor bhūmisāvanavāsaraH//"],
    "1.37": ["vasudvyaṣṭādrirūpāṅkasaptādritithayo yuge/", "cāndrāH khāṣṭakhakhavyomakhāgnikhartuniśākarāH//"],
}
# GRETIL's own numeric annotations on these lines
SS_GRETIL_ANNOTATIONS = {
    ("1.30", 0): 57753336, ("1.30", 1): 2296832, ("1.31", 0): 17937060, ("1.31", 1): 364220,
    ("1.32", 0): 7022376, ("1.32", 1): 146568, ("1.33", 0): 488203, ("1.33", 1): 232238,
    ("1.34", 0): 1582237828, ("1.37", 0): 1577917828, ("1.37", 1): 1603000080,
}
# word-numeral compounds: (verse, half, compound as written, tokens; last token in its inflected surface form)
SS_NUMERALS = [
    ("1.15", 1, "dvitrisāgarair", ["dvi", "tri", "sāgarair"], "x ayuta"),
    ("1.24", 1, "kṛtādrivedā", ["kṛta", "adri", "vedā"], "x 100 (śataghnāḥ)"),
    ("1.29", 0, "khacatuṣkaradārṇavāH", ["kha", "catuṣka", "rada", "arṇavāH"], "Sun, Mercury, Venus"),
    ("1.30", 0, "rasāgnitritrīṣusaptabhūdharamārgaṇāH", ["rasa", "agni", "tri", "tri", "iṣu", "sapta", "bhūdhara", "mārgaṇāH"], "Moon"),
    ("1.30", 1, "dasratryaṣṭarasāṅkākṣilocanāni", ["dasra", "tri", "aṣṭa", "rasa", "aṅka", "akṣi", "locanāni"], "Mars"),
    ("1.31", 0, "śūnyartukhādritryaṅkanagendavaH", ["śūnya", "ṛtu", "kha", "adri", "tri", "aṅka", "naga", "indavaH"], "Mercury śīghra"),
    ("1.31", 1, "khadasrākṣivedaṣaḍvahnayas", ["kha", "dasra", "akṣi", "veda", "ṣaṭ", "vahnayas"], "Jupiter"),
    ("1.32", 0, "ṣaṭsaptatriyamāśvikhabhūdharāH", ["ṣaṭ", "sapta", "tri", "yama", "aśvi", "kha", "bhūdharāH"], "Venus śīghra"),
    ("1.32", 1, "bhujaṅgaṣaṭpañcarasavedaniśākarāH", ["bhujaṅga", "ṣaṭ", "pañca", "rasa", "veda", "niśākarāH"], "Saturn"),
    ("1.33", 0, "candroccasyāgniśūnyāśvivasusarpārṇavā", ["~candroccasya", "agni", "śūnya", "aśvi", "vasu", "sarpa", "arṇavā"], "Moon's apogee"),
    ("1.33", 1, "vasvagniyamāśviśikhidasrakāH", ["vasu", "agni", "yama", "aśvi", "śikhi", "dasrakāH"], "Moon's node (retrograde)"),
    ("1.34", 0, "aṣṭākṣivasvadritridvidvyaṣṭaśarendavaH", ["aṣṭa", "akṣi", "vasu", "adri", "tri", "dvi", "dvi", "aṣṭa", "śara", "indavaH"], "sidereal days"),
    ("1.37", 0, "vasudvyaṣṭādrirūpāṅkasaptādritithayo", ["vasu", "dvi", "aṣṭa", "adri", "rūpa", "aṅka", "sapta", "adri", "tithayo"], "civil days"),
    ("1.37", 1, "khāṣṭakhakhavyomakhāgnikhartuniśākarāH", ["kha", "aṣṭa", "kha", "kha", "vyoma", "kha", "agni", "kha", "ṛtu", "niśākarāH"], "lunar days"),
]

# ------------------------------------------------------------------ yuga verses (Devanagari, dossier)
BHAGAVATA_3_11 = dict(ref="Bhāgavata 3.11.18-19", status="sanskrit", src="dossier", metre="anustubh",
                      halves=["कृतं त्रेता द्वापरं च कलिश्चेति चतुर्युगम्", "दिव्यैर्द्वादशभिर्वर्षैः सावधानं निरूपितम्",
                              "चत्वारि त्रीणि द्वे चैकं कृतादिषु यथाक्रमम्", "सङ्ख्यातानि सहस्राणि द्विगुणानि शतानि च"])
VISNU_1_3 = dict(ref="Viṣṇu Purāṇa 1.3.11-15", status="sanskrit", src="dossier", metre="anustubh",
                 halves=["दिव्यैर्वर्षसहस्रैस्तु कृतत्रेतादिसंज्ञितम्", "चतुर्युगं द्वादशभिस्तद्विभागं निबोध मे",
                         "चत्वारि त्रीणि द्वे चैकं कृतादिषु यथाक्रमम्", "दिव्याब्दानां सहस्राणि युगेष्वाहुः पुराविदः",
                         "तत्प्रमाणैः शतैः सन्ध्या पूर्वा तत्राभिधीयते", "सन्ध्यांशश्चैव तत्तुल्यो युगस्यानन्तरो हि सः",
                         "सन्ध्यासन्ध्यांशयोरन्तर्यः कालो मुनिसत्तम", "युगाख्यः स तु विज्ञेयः कृतत्रेतादिसंज्ञितः",
                         "कृतं त्रेता द्वापरश्च कलिश्चैव चतुर्युगम्", "प्रोच्यते तत्सहस्रं च ब्रह्मणो दिवसं मुने"])
MANU_1_68_72 = dict(ref="Manusmṛti 1.68-72", status="sanskrit", src="dossier (source link missing)", metre="anustubh",
                    halves=["ब्राह्मस्य तु क्षपाहस्य यत्प्रमाणं समासतः", "एकैकशो युगानां तु क्रमशस्तन्निबोधत",
                            "चत्वार्याहुः सहस्राणि वर्षाणां तत्कृतं युगम्", "तस्य तावत्शती सन्ध्या सन्ध्यांशश्च तथाविधः",
                            "इतरेषु ससन्ध्येषु ससन्ध्यांशेषु च त्रिषु", "एकापायेन वर्तन्ते सहस्राणि शतानि च",
                            "यदेतत्परिसंख्यातमादावेव चतुर्युगम्", "एतद्द्वादशसाहस्रं देवानां युगमुच्यते",
                            "दैविकानां युगानां तु सहस्रं परिसंख्यया", "ब्राह्ममेकमहर्ज्ञेयं तावतीं रात्रिमेव च"],
                    note="'तावत्शती' should be the sandhi form 'तावच्छती'.")

# ------------------------------------------------------------------ Vedic number lists (Devanagari, dossier)
TS_7_2 = {
    "7.2.11": "एकस्मै स्वाहा द्वाभ्याग् स्वाहा त्रिभ्यः स्वाहा चतुर्भ्यः स्वाहा पञ्चभ्यः स्वाहा षड्भ्यः स्वाहा सप्तभ्यः स्वाहाष्टाभ्यः स्वाहा नवभ्यः स्वाहा दशभ्यः स्वाहैकादशभ्यः स्वाहा द्वादशभ्यः स्वाहा त्रयोदशभ्यः स्वाहा चतुर्दशभ्यः स्वाहा पञ्चदशभ्यः स्वाहा षोडशभ्यः स्वाहा सप्तदशभ्यः स्वाहाष्टादशभ्यः स्वाहैकान्नविंशत्यै स्वाहा नवविंशत्यै स्वाहैकान्नचत्वारिंशते स्वाहा नवचत्वारिंशते स्वाहैकान्नषष्ट्यै स्वाहा नवषष्ट्यै स्वाहैकान्नाशीत्यै स्वाहा नवाशीत्यै स्वाहैकान्नशताय स्वाहा शताय स्वाहा द्वाभ्यां शताभ्याग् स्वाहा सर्वस्मै स्वाहा॥",
    "7.2.12": "एकस्मै स्वाहा त्रिभ्यः स्वाहा पञ्चभ्यः स्वाहा सप्तभ्यः स्वाहा नवभ्यः स्वाहैकादशभ्यः स्वाहा त्रयोदशभ्यः स्वाहा पञ्चदशभ्यः स्वाहा सप्तदशभ्यः स्वाहैकान्नविंशत्यै स्वाहा नवविंशत्यै स्वाहैकान्नचत्वारिंशते स्वाहा नवचत्वारिंशते स्वाहैकान्नषष्ट्यै स्वाहा नवषष्ट्यै स्वाहैकान्नाशीत्यै स्वाहा नवाशीत्यै स्वाहैकान्नशताय स्वाहा शताय स्वाहा सर्वस्मै स्वाहा॥",
    "7.2.13": "द्वाभ्याग् स्वाहा चतुर्भ्यः स्वाहा षड्भ्यः स्वाहा अष्टाभ्यः स्वाहा दशभ्यः स्वाहा द्वादशभ्यः स्वाहा चतुर्दशभ्यः स्वाहा षोडशभ्यः स्वाहा अष्टादशभ्यः स्वाहा विंशत्यै स्वाहा अष्टानवत्यै स्वाहा शताय स्वाहा सर्वस्मै स्वाहा॥",
    "7.2.14": "त्रिभ्यः स्वाहा पञ्चभ्यः स्वाहा सप्तभ्यः स्वाहा नवभ्यः स्वाहैकादशभ्यः स्वाहा त्रयोदशभ्यः स्वाहा पञ्चदशभ्यः स्वाहा सप्तदशभ्यः स्वाहैकान्नविंशत्यै स्वाहा नवविंशत्यै स्वाहैकान्नचत्वारिंशते स्वाहा नवचत्वारिंशते स्वाहैकान्नषष्ट्यै स्वाहा नवषष्ट्यै स्वाहैकान्नाशीत्यै स्वाहा नवाशीत्यै स्वाहैकान्नशताय स्वाहा शताय स्वाहा सर्वस्मै स्वाहा॥",
    "7.2.15": "चतुर्भ्यः स्वाहा अष्टाभ्यः स्वाहा द्वादशभ्यः स्वाहा षोडशभ्यः स्वाहा विंशत्यै स्वाहा षण्णवत्यै स्वाहा शताय स्वाहा सर्वस्मै स्वाहा॥",
    "7.2.16": "पञ्चभ्यः स्वाहा दशभ्यः स्वाहा पञ्चदशभ्यः स्वाहा विंशत्यै स्वाहा पञ्चनवत्यै स्वाहा शताय स्वाहा सर्वस्मै स्वाहा॥",
    "7.2.17": "दशभ्यः स्वाहा विंशत्यै स्वाहा त्रिंशते स्वाहा चत्वारिंशते स्वाहा पञ्चाशते स्वाहा षष्ट्यै स्वाहा सप्तत्यै स्वाहाशीत्यै स्वाहा नवत्यै स्वाहा शताय स्वाहा सर्वस्मै स्वाहा॥",
    "7.2.18": "विंशत्यै स्वाहा चत्वारिंशते स्वाहा षष्ट्यै स्वाहा अश्यीत्यै स्वाहा शताय स्वाहा सर्वस्मै स्वाहा॥",
    "7.2.19": "पञ्चाशते स्वाहा शताय स्वाहा द्वाभ्यां शताभ्याग् स्वाहा त्रिभ्यः शतेभ्यः स्वाहा चतुर्भ्यः शतेभ्यः स्वाहा पञ्चभ्यः शतेभ्यः स्वाहा षड्भ्यः शतेभ्यः स्वाहा सप्तभ्यः शतेभ्यः स्वाहा अष्टाभ्यः शतेभ्यः स्वाहा नवभ्यः शतेभ्यः स्वाहा सहस्राय स्वाहा सर्वस्मै स्वाहा॥",
    "7.2.20": "शताय स्वाहा सहस्राय स्वाहा अयुताय स्वाहा नियुताय स्वाहा प्रयुताय स्वाहा अर्बुदाय स्वाहा न्यर्बुदाय स्वाहा समुद्राय स्वाहा मध्याय स्वाहा अन्ताय स्वाहा परार्धाय स्वाहा उषसे स्वाहा व्युष्ट्यै स्वाहा उदेष्यते स्वाहा उद्यते स्वाहा उदिताय स्वाहा सुवर्गाय स्वाहा लोकाय स्वाहा सर्वस्मै स्वाहा॥",
}
VS = {
    "17.2": "इ॒मा मे॑ऽअग्न॒ऽइष्ट॑का धे॒नवः॑ स॒न्त्वेका॑ च॒ दश॑ च॒ दश॑ च श॒तं च॑ श॒तं च॑ स॒हस्रं॑ च स॒हस्रं॑ चा॒युतं॑ चा॒युतं॑ च नि॒युतं॑ च नि॒युतं॑ च प्र॒युतं॒ चार्बु॑दं च॒ न्यर्बुदं च समु॒द्रश्च॒ मध्यं॒ चान्त॑श्च परा॒र्द्धश्चै॒ता मे॑ऽअग्न॒ऽइष्ट॑का धे॒नवः॑ सन्त्व॒मु॒त्रा॒मुष्मिँ॑ल्लो॒के॥",
    "18.24": "एका च मे तिस्रश्च मे तिस्रश्च मे पञ्च च मे पञ्च च मे सप्त च मे सप्त च मे नव च मे नव च मे एकादश च मे एकादश च मे त्रयोदश च मे त्रयोदश च मे पञ्चदश च मे पञ्चदश च मे सप्तदश च मे सप्तदश च मे नवदश च मे नवदश च मे एकविंशतिश्च मे एकविंशतिश्च मे त्रयोविंशतिश्च मे त्रयोविंशतिश्च मे पञ्चविंशतिश्च मे पञ्चविंशतिश्च मे सप्तविंशतिश्च मे सप्तविंशतिश्च मे नवविंशतिश्च मे नवविंशतिश्च मे एकत्रिंशच्च मे एकत्रिंशच्च मे त्रयस्त्रिंशच्च मे यज्ञेन कल्पन्ताम्॥",
    "18.25": "चतस्रश्च मेऽष्टौ च मेऽष्टौ च मे द्वादश च मे द्वादश च मे षोडश च मे षोडश च मे विंशतिश्च मे विंशतिश्च मे चतुर्विंशतिश्च मे चतुर्विंशतिश्च मेऽष्टाविंशतिश्च मेऽष्टाविंशतिश्च मे द्वात्रिंशच्च मे द्वात्रिंशच्च मे षट्त्रिंशच्च मे षट्त्रिंशच्च मे चत्वारिंशच्च मे चत्वारिंशच्च मे चतुश्चत्वारिंशच्च मे चतुश्चत्वारिंशच्च मेऽष्टाचत्वारिंशच्च मे यज्ञेन कल्पन्ताम्॥",
}

# ------------------------------------------------------------------ counting passages
BU_3_9_1 = dict(ref="Bṛhadāraṇyaka 3.9.1-2", status="sanskrit", src="vishvasa_bu",
                text='अथ हैनं विदग्धः शाकल्यः पप्रच्छ कति देवा याज्ञवल्क्येति स हैतयैव निविदा प्रतिपेदे यावन्तो वैश्वदेवस्य निविद्युच्यन्ते त्रयश्च त्री च शता त्रयश्च त्री च सहस्रेत्योमिति होवाच कत्येव देवा याज्ञवल्क्येति त्रयस्त्रिंशदित्योमिति होवाच कत्येव देवा याज्ञवल्क्येति षडित्योमिति होवाच कत्येव देवा याज्ञवल्क्येति त्रय इत्योमिति होवाच कत्येव देवा याज्ञवल्क्येति द्वावित्योमिति होवाच कत्येव देवा याज्ञवल्क्येत्यध्यर्ध इत्योमिति होवाच कत्येव देवा याज्ञवल्येत्येक इत्योमिति होवाच कतमे ते त्रयश्च त्री च शता त्रयश्च त्री च सहस्रेति ॥ १ ॥',
                text2='स होवाच महिमान एवैषामेते त्रयस्त्रिंशत्त्वेव देवा इति कतमे ते त्रयस्त्रिंशदित्यष्टौ वसव एकादश रुद्रा द्वादशादित्यास्त एकत्रिंशदिन्द्रश्चैव प्रजापतिश्च त्रयस्त्रिंशा इति ॥ २ ॥',
                note="Source prints याज्ञवल्येति once for याज्ञवल्क्येति. ŚB 11.6.3.4 (Mādhyandina) has the same dialogue "
                     "without the answer 'six' (षट्).",
                answers=[("त्रयश्च त्री च शता", "traya + tri * śata"), ("त्रयश्च त्री च सहस्र", "traya + tri * sahasra"),
                         ("त्रयस्त्रिंशत्", "trayastriṃśat"), ("षट्", "ṣaṭ"), ("त्रयः", "trayaḥ"),
                         ("द्वौ", "dvau"), ("अध्यर्धः", "adhyardha"), ("एकः", "ekaḥ")])
RV_3_9_9 = dict(ref="Ṛgveda 3.9.9", status="sanskrit", src="vishvasa_rv",
                text="त्रीणि शता त्री सहस्राण्यग्निं त्रिंशच्च देवा नव चासपर्यन् ।\nऔक्षन्घृतैरस्तृणन्बर्हिरस्मा आदिद्धोतारं न्यसादयन्त ॥",
                accented="त्रीणि॑ श॒ता त्री स॒हस्रा॑ण्य॒ग्निं त्रिं॒शच्च॑ दे॒वा नव॑ चासपर्यन् ।\nऔक्ष॑न्घृ॒तैरस्तृ॑णन्ब॒र्हिर॑स्मा॒ आदिद्धोता॑रं॒ न्य॑सादयन्त ॥",
                metre="triṣṭubh", deity="Agni", rishi="Gāthina Viśvāmitra",
                count="tri * śata + tri * sahasra + triṃśat + nava")
