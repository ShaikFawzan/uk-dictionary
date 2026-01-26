import json, os, sys
from pathlib import Path

# ---------- CONFIG: map your input files to paradigm IDs ----------
INPUTS = [
    # ───────────── ДІЄСЛОВА ─────────────
    {"path": "data/дієслова 1 дієвідміна особове доконаний вид нерефлексивне.json",
     "pos": "VERB", "paradigm_id": "uk-verb-1st-perf-nonrefl"},

    {"path": "data/дієслова 1 дієвідміна особове недоконаний вид нерефлексивне.json",
     "pos": "VERB", "paradigm_id": "uk-verb-1st-imperf-nonrefl"},

    {"path": "data/дієслова 1 дієвідміна особове доконаний вид рефлексивне.json",
     "pos": "VERB", "paradigm_id": "uk-verb-1st-perf-refl"},

    {"path": "data/дієслова 2 дієвідміна особове недоконаний вид нерефлексивне.json",
     "pos": "VERB", "paradigm_id": "uk-verb-2nd-imperf-nonrefl"},

    {"path": "data/дієслова 2 дієвідміна особове недоконаний вид рефлексивне.json",
     "pos": "VERB", "paradigm_id": "uk-verb-2nd-imperf-refl"},

    {"path": "data/дієслова 2 дієвідміна особове доконаний вид рефлексивне.json",
     "pos": "VERB", "paradigm_id": "uk-verb-2nd-perf-refl"},

    {"path": "data/дієслова 2 дієвідміна особове доконаний вид нерефлексивне.json",
     "pos": "VERB", "paradigm_id": "uk-verb-2nd-perf-nonrefl"},

    # ───────────── ІМЕННИКИ ─────────────
    {"path": "data/іменники 1 відміна м'яка група.json",
     "pos": "NOUN", "paradigm_id": "uk-noun-1st-soft"},

    {"path": "data/іменники 1 відміна тверда група.json",
     "pos": "NOUN", "paradigm_id": "uk-noun-1st-hard"},

    {"path": "data/іменники 1 відміна мішана.json",
     "pos": "NOUN", "paradigm_id": "uk-noun-1st-mixed"},

    {"path": "data/іменники 2 відміна м'яка група.json",
     "pos": "NOUN", "paradigm_id": "uk-noun-2nd-soft"},

    {"path": "data/іменники 2 відміна тверда група.json",
     "pos": "NOUN", "paradigm_id": "uk-noun-2nd-hard"},

    {"path": "data/іменники 2 відміна мішана група.json",
     "pos": "NOUN", "paradigm_id": "uk-noun-2nd-mixed"},

    {"path": "data/іменники 3 відміна.json",
     "pos": "NOUN", "paradigm_id": "uk-noun-3rd"},

    {"path": "data/іменники 4 відміна.json",
     "pos": "NOUN", "paradigm_id": "uk-noun-4th"},

    {"path": "data/іменники множина.json",
     "pos": "NOUN", "paradigm_id": "uk-noun-plurale"},  # plural-only set

    # ───────────── ПРИКМЕТНИКИ ─────────────
    {"path": "data/прикметники м'яка група.json",
     "pos": "ADJ", "paradigm_id": "uk-adj-soft"},

    {"path": "data/прикметники тверда група.json",
     "pos": "ADJ", "paradigm_id": "uk-adj-hard"},

    # ───────────── ДІЄПРИКМЕТНИКИ ─────────────
    {"path": "data/дієприкметники.json",
     "pos": "PARTICIPLE", "paradigm_id": "uk-participle-long"},

    # # ───────────── SYNONYMS (if structure differs, keep separate or tag) ─────────────
    # {"path": "data/синоніми_іменники_м'якої_групи.json",
    #  "pos": "NOUN", "paradigm_id": "uk-noun-1st-soft",}  # or handle in a separate synonyms pipeline
]


# ---------- SLOT MAPS (keep these consistent per paradigm) ----------

# 2nd conjugation — IMPERFECTIVE, non-reflexive
VERB_2_IMPERF_NONREFL = [
    ("INF",      {"pos":"VERB","aspect":"imperf","mood":"inf"}),
    (None,       None),  # skip — technical placeholder

    ("IMP_2SG",  {"pos":"VERB","aspect":"imperf","mood":"imp","person":2,"number":"sg"}),
    ("IMP_1PL",  {"pos":"VERB","aspect":"imperf","mood":"imp","person":1,"number":"pl"}),
    ("IMP_1PL",  {"pos":"VERB","aspect":"imperf","mood":"imp","person":1,"number":"pl","alt":True}),
    ("IMP_2PL",  {"pos":"VERB","aspect":"imperf","mood":"imp","person":2,"number":"pl"}),

    ("PRES_1SG", {"pos":"VERB","aspect":"imperf","tense":"pres","person":1,"number":"sg"}),
    ("PRES_2SG", {"pos":"VERB","aspect":"imperf","tense":"pres","person":2,"number":"sg"}),
    ("PRES_3SG", {"pos":"VERB","aspect":"imperf","tense":"pres","person":3,"number":"sg"}),
    ("PRES_1PL", {"pos":"VERB","aspect":"imperf","tense":"pres","person":1,"number":"pl"}),
    ("PRES_1PL", {"pos":"VERB","aspect":"imperf","tense":"pres","person":1,"number":"pl","alt":True}),
    ("PRES_2PL", {"pos":"VERB","aspect":"imperf","tense":"pres","person":2,"number":"pl"}),
    ("PRES_3PL", {"pos":"VERB","aspect":"imperf","tense":"pres","person":3,"number":"pl"}),

    ("FUT_1SG",  {"pos":"VERB","aspect":"imperf","tense":"fut","person":1,"number":"sg","type":"synthetic"}),
    ("FUT_2SG",  {"pos":"VERB","aspect":"imperf","tense":"fut","person":2,"number":"sg","type":"synthetic"}),
    ("FUT_3SG",  {"pos":"VERB","aspect":"imperf","tense":"fut","person":3,"number":"sg","type":"synthetic"}),
    ("FUT_1PL",  {"pos":"VERB","aspect":"imperf","tense":"fut","person":1,"number":"pl","type":"synthetic"}),
    ("FUT_1PL",  {"pos":"VERB","aspect":"imperf","tense":"fut","person":1,"number":"pl","type":"synthetic","alt":True}),
    ("FUT_2PL",  {"pos":"VERB","aspect":"imperf","tense":"fut","person":2,"number":"pl","type":"synthetic"}),
    ("FUT_3PL",  {"pos":"VERB","aspect":"imperf","tense":"fut","person":3,"number":"pl","type":"synthetic"}),

    ("PAST_M",   {"pos":"VERB","aspect":"imperf","tense":"past","gender":"m","number":"sg"}),
    ("PAST_F",   {"pos":"VERB","aspect":"imperf","tense":"past","gender":"f","number":"sg"}),
    ("PAST_N",   {"pos":"VERB","aspect":"imperf","tense":"past","gender":"n","number":"sg"}),
    ("PAST_PL",  {"pos":"VERB","aspect":"imperf","tense":"past","number":"pl"}),
]

# 2nd conjugation — IMPERFECTIVE, reflexive (-ся/-сь)
VERB_2_IMPERF_REFL = [
    ("INF",      {"pos":"VERB","aspect":"imperf","reflexive":True,"mood":"inf"}),
    (None,       None),  # placeholder

    ("IMP_2SG",  {"pos":"VERB","aspect":"imperf","reflexive":True,"mood":"imp","person":2,"number":"sg"}),
    ("IMP_1PL",  {"pos":"VERB","aspect":"imperf","reflexive":True,"mood":"imp","person":1,"number":"pl"}),
    ("IMP_1PL",  {"pos":"VERB","aspect":"imperf","reflexive":True,"mood":"imp","person":1,"number":"pl","alt":True}),
    ("IMP_2PL",  {"pos":"VERB","aspect":"imperf","reflexive":True,"mood":"imp","person":2,"number":"pl"}),

    ("PRES_1SG", {"pos":"VERB","aspect":"imperf","reflexive":True,"tense":"pres","person":1,"number":"sg"}),
    ("PRES_2SG", {"pos":"VERB","aspect":"imperf","reflexive":True,"tense":"pres","person":2,"number":"sg"}),
    ("PRES_3SG", {"pos":"VERB","aspect":"imperf","reflexive":True,"tense":"pres","person":3,"number":"sg"}),
    ("PRES_1PL", {"pos":"VERB","aspect":"imperf","reflexive":True,"tense":"pres","person":1,"number":"pl"}),
    ("PRES_1PL", {"pos":"VERB","aspect":"imperf","reflexive":True,"tense":"pres","person":1,"number":"pl","alt":True}),
    ("PRES_2PL", {"pos":"VERB","aspect":"imperf","reflexive":True,"tense":"pres","person":2,"number":"pl"}),
    ("PRES_3PL", {"pos":"VERB","aspect":"imperf","reflexive":True,"tense":"pres","person":3,"number":"pl"}),

    ("FUT_1SG",  {"pos":"VERB","aspect":"imperf","reflexive":True,"tense":"fut","person":1,"number":"sg","type":"synthetic"}),
    ("FUT_2SG",  {"pos":"VERB","aspect":"imperf","reflexive":True,"tense":"fut","person":2,"number":"sg","type":"synthetic"}),
    ("FUT_3SG",  {"pos":"VERB","aspect":"imperf","reflexive":True,"tense":"fut","person":3,"number":"sg","type":"synthetic"}),
    ("FUT_1PL",  {"pos":"VERB","aspect":"imperf","reflexive":True,"tense":"fut","person":1,"number":"pl","type":"synthetic"}),
    ("FUT_1PL",  {"pos":"VERB","aspect":"imperf","reflexive":True,"tense":"fut","person":1,"number":"pl","type":"synthetic","alt":True}),
    ("FUT_2PL",  {"pos":"VERB","aspect":"imperf","reflexive":True,"tense":"fut","person":2,"number":"pl","type":"synthetic"}),
    ("FUT_3PL",  {"pos":"VERB","aspect":"imperf","reflexive":True,"tense":"fut","person":3,"number":"pl","type":"synthetic"}),

    ("PAST_M",   {"pos":"VERB","aspect":"imperf","reflexive":True,"tense":"past","gender":"m","number":"sg"}),
    ("PAST_F",   {"pos":"VERB","aspect":"imperf","reflexive":True,"tense":"past","gender":"f","number":"sg"}),
    ("PAST_N",   {"pos":"VERB","aspect":"imperf","reflexive":True,"tense":"past","gender":"n","number":"sg"}),
    ("PAST_PL",  {"pos":"VERB","aspect":"imperf","reflexive":True,"tense":"past","number":"pl"}),
]

# 2nd conjugation — PERFECTIVE, non-reflexive
VERB_2_PERF_NONREFL = [
    ("INF",      {"pos":"VERB","aspect":"perf","mood":"inf"}),
    (None,       None),  # placeholder in your data → skip
    ("IMP_2SG",  {"pos":"VERB","aspect":"perf","mood":"imp","person":2,"number":"sg"}),
    ("IMP_1PL",  {"pos":"VERB","aspect":"perf","mood":"imp","person":1,"number":"pl"}),
    ("IMP_1PL",  {"pos":"VERB","aspect":"perf","mood":"imp","person":1,"number":"pl","alt":True}),
    ("IMP_2PL",  {"pos":"VERB","aspect":"perf","mood":"imp","person":2,"number":"pl"}),

    # Note: perfective "present" forms are morphologically present but semantically future.
    ("PRES_1SG", {"pos":"VERB","aspect":"perf","tense":"pres","person":1,"number":"sg"}),
    ("PRES_2SG", {"pos":"VERB","aspect":"perf","tense":"pres","person":2,"number":"sg"}),
    ("PRES_3SG", {"pos":"VERB","aspect":"perf","tense":"pres","person":3,"number":"sg"}),
    ("PRES_1PL", {"pos":"VERB","aspect":"perf","tense":"pres","person":1,"number":"pl"}),
    ("PRES_1PL", {"pos":"VERB","aspect":"perf","tense":"pres","person":1,"number":"pl","alt":True}),
    ("PRES_2PL", {"pos":"VERB","aspect":"perf","tense":"pres","person":2,"number":"pl"}),
    ("PRES_3PL", {"pos":"VERB","aspect":"perf","tense":"pres","person":3,"number":"pl"}),

    ("FUT_1SG",  {"pos":"VERB","aspect":"perf","tense":"fut","person":1,"number":"sg","type":"synthetic"}),
    ("FUT_2SG",  {"pos":"VERB","aspect":"perf","tense":"fut","person":2,"number":"sg","type":"synthetic"}),
    ("FUT_3SG_REMOVE_IF_DUP", {"pos":"VERB","aspect":"perf","tense":"fut","person":3,"number":"sg","type":"synthetic"}),  # keep if present in your data
    ("FUT_1PL",  {"pos":"VERB","aspect":"perf","tense":"fut","person":1,"number":"pl","type":"synthetic"}),
    ("FUT_1PL",  {"pos":"VERB","aspect":"perf","tense":"fut","person":1,"number":"pl","type":"synthetic","alt":True}),
    ("FUT_2PL",  {"pos":"VERB","aspect":"perf","tense":"fut","person":2,"number":"pl","type":"synthetic"}),
    ("FUT_3PL",  {"pos":"VERB","aspect":"perf","tense":"fut","person":3,"number":"pl","type":"synthetic"}),

    ("PAST_M",   {"pos":"VERB","aspect":"perf","tense":"past","gender":"m","number":"sg"}),
    ("PAST_F",   {"pos":"VERB","aspect":"perf","tense":"past","gender":"f","number":"sg"}),
    ("PAST_N",   {"pos":"VERB","aspect":"perf","tense":"past","gender":"n","number":"sg"}),
    ("PAST_PL",  {"pos":"VERB","aspect":"perf","tense":"past","number":"pl"}),
]

# 2nd conjugation — PERFECTIVE, reflexive (-ся/-сь)
VERB_2_PERF_REFL = [
    ("INF",      {"pos":"VERB","aspect":"perf","reflexive":True,"mood":"inf"}),
    (None,       None),
    ("IMP_2SG",  {"pos":"VERB","aspect":"perf","reflexive":True,"mood":"imp","person":2,"number":"sg"}),
    ("IMP_1PL",  {"pos":"VERB","aspect":"perf","reflexive":True,"mood":"imp","person":1,"number":"pl"}),
    ("IMP_1PL",  {"pos":"VERB","aspect":"perf","reflexive":True,"mood":"imp","person":1,"number":"pl","alt":True}),
    ("IMP_2PL",  {"pos":"VERB","aspect":"perf","reflexive":True,"mood":"imp","person":2,"number":"pl"}),

    ("PRES_1SG", {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"pres","person":1,"number":"sg"}),
    ("PRES_2SG", {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"pres","person":2,"number":"sg"}),
    ("PRES_3SG", {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"pres","person":3,"number":"sg"}),
    ("PRES_1PL", {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"pres","person":1,"number":"pl"}),
    ("PRES_1PL", {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"pres","person":1,"number":"pl","alt":True}),
    ("PRES_2PL", {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"pres","person":2,"number":"pl"}),
    ("PRES_3PL", {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"pres","person":3,"number":"pl"}),

    ("FUT_1SG",  {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"fut","person":1,"number":"sg","type":"synthetic"}),
    ("FUT_2SG",  {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"fut","person":2,"number":"sg","type":"synthetic"}),
    ("FUT_3SG_REMOVE_IF_DUP", {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"fut","person":3,"number":"sg","type":"synthetic"}),
    ("FUT_1PL",  {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"fut","person":1,"number":"pl","type":"synthetic"}),
    ("FUT_1PL",  {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"fut","person":1,"number":"pl","type":"synthetic","alt":True}),
    ("FUT_2PL",  {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"fut","person":2,"number":"pl","type":"synthetic"}),
    ("FUT_3PL",  {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"fut","person":3,"number":"pl","type":"synthetic"}),

    ("PAST_M",   {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"past","gender":"m","number":"sg"}),
    ("PAST_F",   {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"past","gender":"f","number":"sg"}),
    ("PAST_N",   {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"past","gender":"n","number":"sg"}),
    ("PAST_PL",  {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"past","number":"pl"}),
]

############
# ІМЕННИКИ
############ 

NOUN_1_MIXED = [
    ("NOM_SG", {"pos":"NOUN","case":"nom","number":"sg"}), # називний одн.: "паша"
    ("GEN_SG", {"pos":"NOUN","case":"gen","number":"sg"}), # родовий: "паші"
    ("DAT_SG", {"pos":"NOUN","case":"dat","number":"sg"}), # давальний: "паші"
    ("ACC_SG", {"pos":"NOUN","case":"acc","number":"sg"}), # знахідний: "пашу"
    ("INS_SG", {"pos":"NOUN","case":"ins","number":"sg"}), # орудний: "пашею"
    ("LOC_SG", {"pos":"NOUN","case":"loc","number":"sg"}), # місцевий: "на Паші"
    ("VOC_SG", {"pos":"NOUN","case":"voc","number":"sg"}), # кличний: "Паше!"
]

NOUN_1_SOFT = [
    ("NOM_SG", {"pos":"NOUN","case":"nom","number":"sg"}),
    ("GEN_SG", {"pos":"NOUN","case":"gen","number":"sg"}),
    ("DAT_SG", {"pos":"NOUN","case":"dat","number":"sg"}),
    ("ACC_SG", {"pos":"NOUN","case":"acc","number":"sg"}),
    ("INS_SG", {"pos":"NOUN","case":"ins","number":"sg"}),
    ("LOC_SG", {"pos":"NOUN","case":"loc","number":"sg"}),
    ("VOC_SG", {"pos":"NOUN","case":"voc","number":"sg"}),
]

NOUN_1_HARD = [
    ("NOM_SG", {"pos":"NOUN","case":"nom","number":"sg"}),
    ("GEN_SG", {"pos":"NOUN","case":"gen","number":"sg"}),
    ("DAT_SG", {"pos":"NOUN","case":"dat","number":"sg"}),
    ("ACC_SG", {"pos":"NOUN","case":"acc","number":"sg"}),
    ("INS_SG", {"pos":"NOUN","case":"ins","number":"sg"}),
    ("LOC_SG", {"pos":"NOUN","case":"loc","number":"sg"}),
    ("VOC_SG", {"pos":"NOUN","case":"voc","number":"sg"}),
]

NOUN_2_SOFT = [
    ("NOM_SG", {"pos":"NOUN","case":"nom","number":"sg"}),
    ("GEN_SG", {"pos":"NOUN","case":"gen","number":"sg"}),
    ("DAT_SG", {"pos":"NOUN","case":"dat","number":"sg"}),
    ("ACC_SG", {"pos":"NOUN","case":"acc","number":"sg"}),
    ("INS_SG", {"pos":"NOUN","case":"ins","number":"sg"}),
    ("LOC_SG", {"pos":"NOUN","case":"loc","number":"sg"}),
    ("VOC_SG", {"pos":"NOUN","case":"voc","number":"sg"}),
]

# NOUN_2_HARD = [
#     ("NOM_SG", {"pos":"NOUN","case":"nom","number":"sg"}),
#     ("GEN_SG", {"pos":"NOUN","case":"gen","number":"sg"}),
#     ("DAT_SG", {"pos":"NOUN","case":"dat","number":"sg"}),
#     ("ACC_SG", {"pos":"NOUN","case":"acc","number":"sg"}),
#     ("INS_SG", {"pos":"NOUN","case":"ins","number":"sg"}),
#     ("LOC_SG", {"pos":"NOUN","case":"loc","number":"sg"}),
#     ("VOC_SG", {"pos":"NOUN","case":"voc","number":"sg"}),
# ]

NOUN_2_HARD = [
    # --- Однина ---
    ("NOM_SG", {"pos": "NOUN", "case": "nom", "number": "sg"}),                    # єнот
    ("GEN_SG", {"pos": "NOUN", "case": "gen", "number": "sg"}),                    # єнота
    ("DAT_SG", {"pos": "NOUN", "case": "dat", "number": "sg"}),                    # єнотові
    ("DAT_SG", {"pos": "NOUN", "case": "dat", "number": "sg", "alt": True}),       # єноту
    ("ACC_SG", {"pos": "NOUN", "case": "acc", "number": "sg"}),                    # єнота
    ("INS_SG", {"pos": "NOUN", "case": "ins", "number": "sg"}),                    # єнотом
    ("LOC_SG", {"pos": "NOUN", "case": "loc", "number": "sg"}),                    # на єнотові
    ("LOC_SG", {"pos": "NOUN", "case": "loc", "number": "sg", "alt": True}),       # на єноті
    ("DAT_SG", {"pos": "NOUN", "case": "dat", "number": "sg", "alt": True}),       # 
    ("VOC_SG", {"pos": "NOUN", "case": "voc", "number": "sg"}),                    # єноте

    # --- Множина ---
    ("NOM_PL", {"pos": "NOUN", "case": "nom", "number": "pl"}),                    # єноти
    ("GEN_PL", {"pos": "NOUN", "case": "gen", "number": "pl"}),                    # єнотів
    ("DAT_PL", {"pos": "NOUN", "case": "dat", "number": "pl"}),                    # єнотам
    ("DAT_PL", {"pos": "NOUN", "case": "dat", "number": "pl", "alt": True}),       # 
    ("ACC_PL", {"pos": "NOUN", "case": "acc", "number": "pl"}),                    # єнотів
    ("VOC_PL", {"pos": "NOUN", "case": "voc", "number": "pl"}),                    # єноти
    ("LOC_PL", {"pos": "NOUN", "case": "loc", "number": "pl"}),                    # на єнотах
    ("NOM_PL", {"pos": "NOUN", "case": "nom", "number": "pl", "alt": True}),       # 
]


NOUN_2_MIXED = [
    ("NOM_SG", {"pos":"NOUN","case":"nom","number":"sg"}),
    ("GEN_SG", {"pos":"NOUN","case":"gen","number":"sg"}),
    ("DAT_SG", {"pos":"NOUN","case":"dat","number":"sg"}),
    ("ACC_SG", {"pos":"NOUN","case":"acc","number":"sg"}),
    ("INS_SG", {"pos":"NOUN","case":"ins","number":"sg"}),
    ("LOC_SG", {"pos":"NOUN","case":"loc","number":"sg"}),
    ("VOC_SG", {"pos":"NOUN","case":"voc","number":"sg"}),
]

NOUN_3RD = [
    ("NOM_SG", {"pos":"NOUN","case":"nom","number":"sg"}),
    ("GEN_SG", {"pos":"NOUN","case":"gen","number":"sg"}),
    ("DAT_SG", {"pos":"NOUN","case":"dat","number":"sg"}),
    ("ACC_SG", {"pos":"NOUN","case":"acc","number":"sg"}),
    ("INS_SG", {"pos":"NOUN","case":"ins","number":"sg"}),
    ("LOC_SG", {"pos":"NOUN","case":"loc","number":"sg"}),
    ("VOC_SG", {"pos":"NOUN","case":"voc","number":"sg"}),
]

NOUN_4TH = [
    ("NOM_SG", {"pos":"NOUN","case":"nom","number":"sg"}),
    ("GEN_SG", {"pos":"NOUN","case":"gen","number":"sg"}),
    ("DAT_SG", {"pos":"NOUN","case":"dat","number":"sg"}),
    ("ACC_SG", {"pos":"NOUN","case":"acc","number":"sg"}),
    ("INS_SG", {"pos":"NOUN","case":"ins","number":"sg"}),
    ("LOC_SG", {"pos":"NOUN","case":"loc","number":"sg"}),
    ("VOC_SG", {"pos":"NOUN","case":"voc","number":"sg"}),
]

NOUN_PLURALE = [
    ("NOM_PL", {"pos":"NOUN","case":"nom","number":"pl"}),
    ("GEN_PL", {"pos":"NOUN","case":"gen","number":"pl"}),
    ("DAT_PL", {"pos":"NOUN","case":"dat","number":"pl"}),
    ("ACC_PL", {"pos":"NOUN","case":"acc","number":"pl"}),
    ("INS_PL", {"pos":"NOUN","case":"ins","number":"pl"}),
    ("LOC_PL", {"pos":"NOUN","case":"loc","number":"pl"}),
    ("VOC_PL", {"pos":"NOUN","case":"voc","number":"pl"}),
]

############
# ПРИКМЕТНИКИ
############ 

ADJ_LONG = [
    ("NOM_M_SG", {"pos":"ADJ","case":"nom","gender":"m","number":"sg"}),
    ("GEN_M_SG", {"pos":"ADJ","case":"gen","gender":"m","number":"sg"}),
    ("DAT_M_SG", {"pos":"ADJ","case":"dat","gender":"m","number":"sg"}),
    ("ACC_M_SG", {"pos":"ADJ","case":"acc","gender":"m","number":"sg"}),
    ("INS_M_SG", {"pos":"ADJ","case":"ins","gender":"m","number":"sg"}),
    ("LOC_M_SG", {"pos":"ADJ","case":"loc","gender":"m","number":"sg"}),

    ("NOM_F_SG", {"pos":"ADJ","case":"nom","gender":"f","number":"sg"}),
    ("GEN_F_SG", {"pos":"ADJ","case":"gen","gender":"f","number":"sg"}),
    ("DAT_F_SG", {"pos":"ADJ","case":"dat","gender":"f","number":"sg"}),
    ("ACC_F_SG", {"pos":"ADJ","case":"acc","gender":"f","number":"sg"}),
    ("INS_F_SG", {"pos":"ADJ","case":"ins","gender":"f","number":"sg"}),
    ("LOC_F_SG", {"pos":"ADJ","case":"loc","gender":"f","number":"sg"}),

    ("NOM_N_SG", {"pos":"ADJ","case":"nom","gender":"n","number":"sg"}),
    ("GEN_N_SG", {"pos":"ADJ","case":"gen","gender":"n","number":"sg"}),
]

############
# ДІЄПРИКМЕТНИКИ
############ 

PARTICIPLE_LONG = [
    # MASC SING
    ("PART_NOM_M_SG", {"pos": "PARTICIPLE", "verbform": "part",
                       "gender": "m", "number": "sg", "case": "nom"}),
    ("PART_GEN_M_SG", {"pos": "PARTICIPLE", "verbform": "part",
                       "gender": "m", "number": "sg", "case": "gen"}),
    ("PART_DAT_M_SG", {"pos": "PARTICIPLE", "verbform": "part",
                       "gender": "m", "number": "sg", "case": "dat"}),
    ("PART_ACC_M_SG", {"pos": "PARTICIPLE", "verbform": "part",
                       "gender": "m", "number": "sg", "case": "acc"}),
    ("PART_INS_M_SG", {"pos": "PARTICIPLE", "verbform": "part",
                       "gender": "m", "number": "sg", "case": "ins"}),
    ("PART_LOC_M_SG", {"pos": "PARTICIPLE", "verbform": "part",
                       "gender": "m", "number": "sg", "case": "loc"}),
    ("PART_VOC_M_SG", {"pos": "PARTICIPLE", "verbform": "part",
                       "gender": "m", "number": "sg", "case": "voc"}),

    # FEM SING
    ("PART_NOM_F_SG", {"pos": "PARTICIPLE", "verbform": "part",
                       "gender": "f", "number": "sg", "case": "nom"}),
    ("PART_GEN_F_SG", {"pos": "PARTICIPLE", "verbform": "part",
                       "gender": "f", "number": "sg", "case": "gen"}),
    ("PART_DAT_F_SG", {"pos": "PARTICIPLE", "verbform": "part",
                       "gender": "f", "number": "sg", "case": "dat"}),
    ("PART_ACC_F_SG", {"pos": "PARTICIPLE", "verbform": "part",
                       "gender": "f", "number": "sg", "case": "acc"}),
    ("PART_INS_F_SG", {"pos": "PARTICIPLE", "verbform": "part",
                       "gender": "f", "number": "sg", "case": "ins"}),
    ("PART_LOC_F_SG", {"pos": "PARTICIPLE", "verbform": "part",
                       "gender": "f", "number": "sg", "case": "loc"}),

    # NEUT SING
    ("PART_NOM_N_SG", {"pos": "PARTICIPLE", "verbform": "part",
                       "gender": "n", "number": "sg", "case": "nom"}),
    ("PART_GEN_N_SG", {"pos": "PARTICIPLE", "verbform": "part",
                       "gender": "n", "number": "sg", "case": "gen"}),
    ("PART_DAT_N_SG", {"pos": "PARTICIPLE", "verbform": "part",
                       "gender": "n", "number": "sg", "case": "dat"}),
    ("PART_ACC_N_SG", {"pos": "PARTICIPLE", "verbform": "part",
                       "gender": "n", "number": "sg", "case": "acc"}),
    ("PART_INS_N_SG", {"pos": "PARTICIPLE", "verbform": "part",
                       "gender": "n", "number": "sg", "case": "ins"}),
    ("PART_LOC_N_SG", {"pos": "PARTICIPLE", "verbform": "part",
                       "gender": "n", "number": "sg", "case": "loc"}),
    ("PART_VOC_N_SG", {"pos": "PARTICIPLE", "verbform": "part",
                       "gender": "n", "number": "sg", "case": "voc", "alt": True}),

    # PLURAL (no gender)
    ("PART_NOM_PL", {"pos": "PARTICIPLE", "verbform": "part",
                     "number": "pl", "case": "nom"}),
    ("PART_GEN_PL", {"pos": "PARTICIPLE", "verbform": "part",
                     "number": "pl", "case": "gen"}),
    ("PART_DAT_PL", {"pos": "PARTICIPLE", "verbform": "part",
                     "number": "pl", "case": "dat"}),
    ("PART_ACC_PL", {"pos": "PARTICIPLE", "verbform": "part",
                     "number": "pl", "case": "acc"}),
    ("PART_INS_PL", {"pos": "PARTICIPLE", "verbform": "part",
                     "number": "pl", "case": "ins"}),
    ("PART_LOC_PL", {"pos": "PARTICIPLE", "verbform": "part",
                     "number": "pl", "case": "loc"}),
]



# 1) I conjugation — IMPERFECTIVE, non-reflexive
VERB_1_IMPERF_NONREFL = [
    ("INF",      {"pos":"VERB","aspect":"imperf","mood":"inf"}),
    (None,       None),  # placeholder in your data → skip
    ("IMP_2SG",  {"pos":"VERB","aspect":"imperf","mood":"imp","person":2,"number":"sg"}),
    ("IMP_1PL",  {"pos":"VERB","aspect":"imperf","mood":"imp","person":1,"number":"pl"}),
    ("IMP_1PL",  {"pos":"VERB","aspect":"imperf","mood":"imp","person":1,"number":"pl","alt":True}),
    ("IMP_2PL",  {"pos":"VERB","aspect":"imperf","mood":"imp","person":2,"number":"pl"}),

    ("PRES_1SG", {"pos":"VERB","aspect":"imperf","tense":"pres","person":1,"number":"sg"}),
    ("PRES_2SG", {"pos":"VERB","aspect":"imperf","tense":"pres","person":2,"number":"sg"}),
    ("PRES_3SG", {"pos":"VERB","aspect":"imperf","tense":"pres","person":3,"number":"sg"}),
    ("PRES_1PL", {"pos":"VERB","aspect":"imperf","tense":"pres","person":1,"number":"pl"}),
    ("PRES_1PL", {"pos":"VERB","aspect":"imperf","tense":"pres","person":1,"number":"pl","alt":True}),
    ("PRES_2PL", {"pos":"VERB","aspect":"imperf","tense":"pres","person":2,"number":"pl"}),
    ("PRES_3PL", {"pos":"VERB","aspect":"imperf","tense":"pres","person":3,"number":"pl"}),

    ("FUT_1SG",  {"pos":"VERB","aspect":"imperf","tense":"fut","person":1,"number":"sg","type":"synthetic"}),
    ("FUT_2SG",  {"pos":"VERB","aspect":"imperf","tense":"fut","person":2,"number":"sg","type":"synthetic"}),
    ("FUT_3SG",  {"pos":"VERB","aspect":"imperf","tense":"fut","person":3,"number":"sg","type":"synthetic"}),
    ("FUT_1PL",  {"pos":"VERB","aspect":"imperf","tense":"fut","person":1,"number":"pl","type":"synthetic"}),
    ("FUT_1PL",  {"pos":"VERB","aspect":"imperf","tense":"fut","person":1,"number":"pl","type":"synthetic","alt":True}),
    ("FUT_2PL",  {"pos":"VERB","aspect":"imperf","tense":"fut","person":2,"number":"pl","type":"synthetic"}),
    ("FUT_3PL",  {"pos":"VERB","aspect":"imperf","tense":"fut","person":3,"number":"pl","type":"synthetic"}),

    ("PAST_M",   {"pos":"VERB","aspect":"imperf","tense":"past","gender":"m","number":"sg"}),
    ("PAST_F",   {"pos":"VERB","aspect":"imperf","tense":"past","gender":"f","number":"sg"}),
    ("PAST_N",   {"pos":"VERB","aspect":"imperf","tense":"past","gender":"n","number":"sg"}),
    ("PAST_PL",  {"pos":"VERB","aspect":"imperf","tense":"past","number":"pl"}),
]

# 2) I conjugation — PERFECTIVE, non-reflexive
# Note: Perfective “present” forms are used as simple future semantically,
# but we keep labels as PRES_* to match your file’s order; aspect="perf" clarifies it.
VERB_1_PERF_NONREFL = [
    ("INF",      {"pos":"VERB","aspect":"perf","mood":"inf"}),
    (None,       None),
    ("IMP_2SG",  {"pos":"VERB","aspect":"perf","mood":"imp","person":2,"number":"sg"}),
    ("IMP_1PL",  {"pos":"VERB","aspect":"perf","mood":"imp","person":1,"number":"pl"}),
    ("IMP_1PL",  {"pos":"VERB","aspect":"perf","mood":"imp","person":1,"number":"pl","alt":True}),
    ("IMP_2PL",  {"pos":"VERB","aspect":"perf","mood":"imp","person":2,"number":"pl"}),

    ("PRES_1SG", {"pos":"VERB","aspect":"perf","tense":"pres","person":1,"number":"sg"}),
    ("PRES_2SG", {"pos":"VERB","aspect":"perf","tense":"pres","person":2,"number":"sg"}),
    ("PRES_3SG", {"pos":"VERB","aspect":"perf","tense":"pres","person":3,"number":"sg"}),
    ("PRES_1PL", {"pos":"VERB","aspect":"perf","tense":"pres","person":1,"number":"pl"}),
    ("PRES_1PL", {"pos":"VERB","aspect":"perf","tense":"pres","person":1,"number":"pl","alt":True}),
    ("PRES_2PL", {"pos":"VERB","aspect":"perf","tense":"pres","person":2,"number":"pl"}),
    ("PRES_3PL", {"pos":"VERB","aspect":"perf","tense":"pres","person":3,"number":"pl"}),

    ("FUT_1SG",  {"pos":"VERB","aspect":"perf","tense":"fut","person":1,"number":"sg","type":"synthetic"}),
    ("FUT_2SG",  {"pos":"VERB","aspect":"perf","tense":"fut","person":2,"number":"sg","type":"synthetic"}),
    ("FUT_3SG",  {"pos":"VERB","aspect":"perf","tense":"fut","person":3,"number":"sg","type":"synthetic"}),
    ("FUT_1PL",  {"pos":"VERB","aspect":"perf","tense":"fut","person":1,"number":"pl","type":"synthetic"}),
    ("FUT_1PL",  {"pos":"VERB","aspect":"perf","tense":"fut","person":1,"number":"pl","type":"synthetic","alt":True}),
    ("FUT_2PL",  {"pos":"VERB","aspect":"perf","tense":"fut","person":2,"number":"pl","type":"synthetic"}),
    ("FUT_3PL",  {"pos":"VERB","aspect":"perf","tense":"fut","person":3,"number":"pl","type":"synthetic"}),

    ("PAST_M",   {"pos":"VERB","aspect":"perf","tense":"past","gender":"m","number":"sg"}),
    ("PAST_F",   {"pos":"VERB","aspect":"perf","tense":"past","gender":"f","number":"sg"}),
    ("PAST_N",   {"pos":"VERB","aspect":"perf","tense":"past","gender":"n","number":"sg"}),
    ("PAST_PL",  {"pos":"VERB","aspect":"perf","tense":"past","number":"pl"}),
]

# 3) I conjugation — PERFECTIVE, reflexive (-ся/-сь)
# Same slots as above, but we flag reflexive=True in features.
# Your generator can append "ся/сь" if suffix doesn’t already include it.
VERB_1_PERF_REFL = [
    ("INF",      {"pos":"VERB","aspect":"perf","reflexive":True,"mood":"inf"}),
    (None,       None),
    ("IMP_2SG",  {"pos":"VERB","aspect":"perf","reflexive":True,"mood":"imp","person":2,"number":"sg"}),
    ("IMP_1PL",  {"pos":"VERB","aspect":"perf","reflexive":True,"mood":"imp","person":1,"number":"pl"}),
    ("IMP_1PL",  {"pos":"VERB","aspect":"perf","reflexive":True,"mood":"imp","person":1,"number":"pl","alt":True}),
    ("IMP_2PL",  {"pos":"VERB","aspect":"perf","reflexive":True,"mood":"imp","person":2,"number":"pl"}),

    ("PRES_1SG", {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"pres","person":1,"number":"sg"}),
    ("PRES_2SG", {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"pres","person":2,"number":"sg"}),
    ("PRES_3SG", {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"pres","person":3,"number":"sg"}),
    ("PRES_1PL", {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"pres","person":1,"number":"pl"}),
    ("PRES_1PL", {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"pres","person":1,"number":"pl","alt":True}),
    ("PRES_2PL", {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"pres","person":2,"number":"pl"}),
    ("PRES_3PL", {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"pres","person":3,"number":"pl"}),

    ("FUT_1SG",  {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"fut","person":1,"number":"sg","type":"synthetic"}),
    ("FUT_2SG",  {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"fut","person":2,"number":"sg","type":"synthetic"}),
    ("FUT_3SG",  {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"fut","person":3,"number":"sg","type":"synthetic"}),
    ("FUT_1PL",  {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"fut","person":1,"number":"pl","type":"synthetic"}),
    ("FUT_1PL",  {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"fut","person":1,"number":"pl","type":"synthetic","alt":True}),
    ("FUT_2PL",  {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"fut","person":2,"number":"pl","type":"synthetic"}),
    ("FUT_3PL",  {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"fut","person":3,"number":"pl","type":"synthetic"}),

    ("PAST_M",   {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"past","gender":"m","number":"sg"}),
    ("PAST_F",   {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"past","gender":"f","number":"sg"}),
    ("PAST_N",   {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"past","gender":"n","number":"sg"}),
    ("PAST_PL",  {"pos":"VERB","aspect":"perf","reflexive":True,"tense":"past","number":"pl"}),
]


PARADIGM = {
    "uk-verb-1st-perf-refl":      VERB_1_PERF_REFL,
    "uk-verb-1st-perf-nonrefl":   VERB_1_PERF_NONREFL,
    "uk-verb-1st-imperf-nonrefl": VERB_1_IMPERF_NONREFL,

    "uk-verb-2nd-perf-refl":      VERB_2_PERF_REFL,
    "uk-verb-2nd-perf-nonrefl":   VERB_2_PERF_NONREFL,
    "uk-verb-2nd-imperf-nonrefl": VERB_2_IMPERF_NONREFL,
    "uk-verb-2nd-imperf-refl":    VERB_2_IMPERF_REFL,
    
    "uk-noun-1st-soft":           NOUN_1_SOFT,
    "uk-noun-1st-hard":           NOUN_1_HARD,
    "uk-noun-1st-mixed":          NOUN_1_MIXED,
    "uk-noun-2nd-soft":           NOUN_2_SOFT,
    "uk-noun-2nd-mixed":          NOUN_2_MIXED,
    "uk-noun-2nd-hard":           NOUN_2_HARD,
    "uk-noun-3rd":                NOUN_3RD,
    "uk-noun-4th":                NOUN_4TH,
    "uk-noun-plurale":            NOUN_PLURALE,

    "uk-adj-soft":                ADJ_LONG,
    "uk-adj-hard":                ADJ_LONG,

    "uk-participle-long":         PARTICIPLE_LONG,
}

# ---------- helpers ----------
def norm_id(s: str) -> str:
    return s.lower()

def apply_stem_rules(stem: str, suffix: str) -> str:
    # Hook for alternations if you need (e.g., d + "жу" → still OK because suffix already "жу").
    return stem

def build_forms(doc: dict) -> list[dict]:
    pid = doc["paradigm_id"]
    slots = PARADIGM.get(pid)
    if not slots:
        return []
    stem = doc["lemma"]
    out = []
    for i, suf in enumerate(doc.get("endings", [])):
        if not suf or suf == "0":
            continue
        if i >= len(slots):
            break
        slot_name, feats = slots[i]
        if not slot_name:
            continue  # skip technical/unused slot
        surface = apply_stem_rules(stem, suf) + suf
        out.append({
            "form": surface,
            "slot": slot_name,
            "features": {**({"pos": doc["pos"]} if doc.get("pos") else {}), **feats}
        })
    return out

def load_json(path: str):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def main():
    base = Path(__file__).parent
    out_docs = []

    for entry in INPUTS:
        path = base / entry["path"]
        pos = entry["pos"]
        pid = entry["paradigm_id"]
        arr = load_json(str(path))
        for it in arr:
            lemma = it["lemma"]
            endings = it.get("end", [])

            if not endings:
                continue

            doc = {
                "_id": norm_id(lemma),
                "lemma": lemma,
                "pos": pos,
                "paradigm_id": pid,
                "endings": endings,
                "forms": [],         # fill below
                "sources": [os.path.basename(path)]
            }
            doc["forms"] = build_forms(doc)
            out_docs.append(doc)

    # ensure result/ exists
    (base / "result").mkdir(exist_ok=True)
    out_path = base / "result" / "lemmas_new.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out_docs, f, ensure_ascii=False, indent=2)
    print(f"Written {len(out_docs)} lemmas → {out_path}")

if __name__ == "__main__":
    main()
