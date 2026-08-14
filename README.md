# Chinese Buddhist Language Flashcards 中文佛教語言抽認卡

A single-file static web app (`index.html`) for browsing Chinese Buddhist
liturgical vocabulary, printing double-sided flashcard PDFs, and exporting
card data.

## Adding a new section or card set

Two steps — no code changes needed.

**1. Put the CSV in `data/chinese/<section-slug>/`**

The folder is the section title, lower-cased with spaces as hyphens:

| Section title        | Folder                        |
| -------------------- | ----------------------------- |
| `Afternoon Recitation` | `data/chinese/afternoon-recitation/` |
| `Repentance`         | `data/chinese/repentance/`    |

**2. Add one row to `flashcard_directory.csv`**

```csv
section,file,english,chinese
Afternoon Recitation,meal_mantra.csv,Mantra for the Meal,供養咒
```

| Column    | Meaning |
| --------- | ------- |
| `section` | Section title, typed by hand. Rows sharing a title group together. Also names the folder (above). |
| `file`    | CSV filename inside that folder. |
| `english` | English name shown for the set. |
| `chinese` | Chinese subtitle shown under it. |
| `folder`  | *Optional.* Only needed if the folder on disk differs from the section title — e.g. after renaming a section without moving files. Leave blank/absent otherwise. |

Sections appear in the order first seen; sets appear in row order.

> **Renaming a section?** Either rename the folder to match the new title, or
> add a `folder` column pointing at the existing folder. If the two disagree
> the files can't be found, and the app logs a clear error to the console and
> shows the set as `0 cards`.

## Card CSV format

Preferred header (new files):

```csv
Character,Pīnyīn,English,eng_tag,shared_by,ch_tag
```

Legacy files use `chinese,pinyin,english_def,ch_tag,eng_tag,frequency` and keep
working — column names are matched case-, accent-, and punctuation-insensitively
against an alias table in `index.html` (`CARD_FIELD_ALIASES`), then mapped onto
the canonical fields. To support another spelling, add one alias there.

| Canonical     | Accepted spellings include                      |
| ------------- | ----------------------------------------------- |
| `chinese`     | `Character`, `chinese`, `hanzi`, `term`         |
| `pinyin`      | `Pīnyīn`, `pinyin`, `romanization`              |
| `english_def` | `English`, `english_def`, `definition`, `meaning` |
| `ch_tag`      | `ch_tag` — Chinese name of the section          |
| `eng_tag`     | `eng_tag` — English key for the section         |
| `frequency`   | `frequency` — occurrence count, orders Type B   |
| `shared_by`   | `shared_by` — other terms/sections it appears in |

## URLs

Every screen has a shareable URL:

| URL | Screen |
| --- | ------ |
| `#/` | Set browser |
| `#/cards/all` | Customize, everything selected |
| `#/cards/evening-ceremony` | Customize, one whole section |
| `#/cards/heart_sutra+gc_repent` | Customize, specific sets |
| `#/known/a`, `#/known/b` | Known-cards viewer |

Selections stay readable and resolvable, so a pasted link rebuilds the same
selection.
