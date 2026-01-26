# UK-DICTIONARY 📘🇺🇦
![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![NLP](https://img.shields.io/badge/Domain-NLP%20%2F%20Linguistics-brightgreen)
![Data](https://img.shields.io/badge/Format-JSON-orange)

**UK-DICTIONARY** is a paradigm-based morphological dictionary of the Ukrainian language, designed for programmatic use in NLP, bots, linguistic research, and language tools.

The project focuses on **explicit morphological paradigms** and **reproducible generation** of fully tagged word forms from compact, human-curated source data.

⚠️ **Early public release (v0.1).** The data and paradigms may contain errors. This release is published for transparency, reproducibility, and future iteration.

---

## Overview 🧠

This repository contains:
- paradigm-grouped source data (JSON)
- a morphology generator script
- a defined schema for lemmas and word forms

The generated dictionary output (e.g. `lemmas_new.json`) is intentionally **not included** in the repo because it can be very large (hundreds of MB) and can be deterministically recreated using the provided script.

---

## Features 🚀

- Lemma-centric dictionary design
- Explicit morphological paradigms (`paradigm_id`)
- Automatic generation of word forms for:
  - verbs (aspect, tense, person, mood, reflexivity)
  - nouns (declension, case, number)
  - adjectives
  - participles
- Rich grammatical feature tagging for every generated form
- JSON-first, database-friendly structure
- Fully reproducible output

---

## Getting Started 🛠️

Follow these steps to set up the project locally:  

### Prerequisites

- **Python 3.8+**  

### Generate the Dictionary

1. **Clone the repository:**  
    ```bash
    git clone https://github.com/raccoon-hero/uk-dictionary.git
    cd uk-dictionary
    ```

2. **Run the generator:**
    ```bash
    python forms_builder_new.py
    ```

3) **Output will be written to the `result/` directory.**

**Note:** the generated file can be large (hundreds of MB) and is therefore excluded from version control.

---

## Project Structure 📂

```plaintext
uk-dictionary/  
├─ data/                  # Source JSON files grouped by paradigms  
├─ docs/                  # Technical documentation  
├─ forms_builder_new.py   # Morphology generator script  
└─ README.md              # Project overview  
```

---

## Data Model 🧩

Each lemma is stored as a normalized document with fields like:
- `_id` — unique identifier (usually equals the lemma)
- `lemma` — base dictionary form
- `pos` — part of speech
- `paradigm_id` — morphological paradigm identifier
- `endings` — ordered list of endings corresponding to paradigm slots
- `forms` — generated word forms with grammatical features

`forms` is generated automatically and is not stored in the repository.

---

## Generation Logic ⚙️

Word forms are generated using a fixed paradigm slot order:

lemma (stem) + ordered endings → paradigm slots → grammatical features

Paradigm definitions and slot mappings are explicitly defined in `forms_builder_new.py`. The generation is deterministic: the same inputs produce the same output.

---

## Documentation 📄

See the `docs/` directory for technical documentation, including:
- schema design
- paradigm system
- grammatical feature taxonomy
- known data issues and limitations

---

## Known Limitations ⚠️

This project reflects the current state of the source data (v0.1). Known issues include:
- duplicated lemmas across some input files
- incorrect or inconsistent endings in certain noun groups
- absence of phonological alternation rules (stem changes)

These issues are documented and intentionally left unmodified in this version.
