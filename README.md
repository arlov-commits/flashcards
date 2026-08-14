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

Legacy files use `chinese,pinyin,english_def,ch_tag,eng_tag` and keep
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
| `shared_by`   | `shared_by` — other terms/sections it appears in |

## Anki export

The **To Anki (.apkg)** button on the Customize & Download screen turns the
current card selection into an Anki deck. The libraries it needs (~1.5 MB of
WASM) are fetched on the first click only, so the page and the PDF path stay
fast for anyone who never uses it.

| Anki field  | Card CSV column |
| ----------- | --------------- |
| `Chinese`   | `chinese`       |
| `Pinyin`    | `pinyin`        |
| `English`   | `english_def`   |
| `Shared_by` | `shared_by`     |

Each note is tagged with its `eng_tag`, so decks stay filterable by source text
inside Anki. Rows with an empty `chinese` are skipped and every field is
trimmed, so legacy CSVs with stray leading spaces export cleanly.

Deck names are flat, never nested — re-nest with `::` inside Anki if you want
that. A single set gets its Chinese title too (`Heart Sutra 心經`); a mixed
selection joins the set names with ` & `, fitting whole names into 60
characters and reporting the rest (`Heart Sutra & Amitabha Sutra +18 more`).
The name is only a default: it appears in an editable field before download.

Anki itself imposes **no** maximum deck name length — its normaliser
([`rslib/src/decks/name.rs`](https://github.com/ankitects/anki/blob/main/rslib/src/decks/name.rs))
only strips invalid characters and trims whitespace. The 60 in
`ANKI_DECK_NAME_MAX` is ours, borrowed from AnkiWeb's shared-deck title limit,
to keep names readable in the deck list.

### Card template

The note type's front, back, and CSS live in `templates/anki-1.2-type-a.txt`
and are compiled into `index.html` verbatim. **Edit that file and re-copy the
three sections** rather than editing the strings in `index.html`, so the two
cannot drift apart.

The back of the card carries:

- a 📖 Pleco link and a 📕 [HanziCraft](https://hanzicraft.com) link, pinned to
  the bottom corners. The Pleco link is built per platform by the card's own
  script: Android gets the `intent://` wrapper (with a `browser_fallback_url`
  to pleco.com), iOS gets `plecoapi://x-callback-url/df?hw=…&sec=dict`, and
  desktop gets a note saying Pleco is mobile-only rather than a dead link. On
  iOS nothing reports whether a custom scheme resolved, so the card assumes
  Pleco is missing if the page is still on screen 1.5 s later and offers an App
  Store link;
- a **Shared by** accordion, collapsed by default, toggled by click or by
  pressing <kbd>J</kbd>. Only some CSVs carry `shared_by`; the
  `{{#Shared_by}}` conditional drops the whole block on notes without it, so
  there is no stray expander to click.

That back template contains its own `<script>`. Inside `index.html` its closing
tag must stay written as `<\/script>`, or it ends the page's own inline script
instead of the Anki card's.

Two constants must never change once shipped:

- the note type id (`ANKI_MODEL_ID` in `index.html`) — a fresh id per export
  would create a duplicate note type in the user's collection every time and
  stop styling edits from propagating;
- the GUID recipe, `ankiHash([chinese, eng_tag])` — hashing term and source
  section only means a corrected deck **updates in place** on re-import rather
  than duplicating every note.

### Licensing

The Anki export vendors [genanki-js](https://github.com/infinyte7/genanki-js)
at `vendor/genanki.js`, which is **AGPL-3.0** (itself derived from
[mkanki](https://github.com/nornagon/mkanki), AGPL-3.0, and
[genanki](https://github.com/kerrickstaley/genanki), MIT; it bundles
[js-sha256](https://github.com/emn178/js-sha256), MIT). Shipping it inside this
page makes the app a combined work under the AGPL-3.0. The repo is public, so
the obligation is met — but the app cannot later become closed-source.

## The Customize & Download screen

The download section is Anki-first: the **To Anki (.apkg)** button and deck
name come immediately after the card table. Everything else lives behind
**Download Data**, which offers the card data (CSV, XLSX, JSON, Google Sheets)
and the printable flashcard PDFs (4×4, 4×5, 5×5) as two groups of the same
menu.

The menu only *chooses* a format — it never downloads. Picking one names the
format and reveals a download button; picking a PDF grid additionally reveals
the print-only controls (the page-count pill and the card design gear) so the
page count is visible before committing. Nothing leaves the browser until the
download button is pressed, and the whole block resets on the next visit to
the screen.

A persistent site nav (**Home · Instructions · Methodology · Feedback · Quiz**)
sits above every screen, outside the screen containers, and highlights the
current one. It never wraps to a second row: the buttons tighten through
breakpoints at 700px, 420px and 340px, and a test measures `scrollWidth`
against `clientWidth` at seven real device widths from 320px up to confirm
nothing is clipped.

## Card identity: Chinese + Pinyin

**One card is one (Chinese, Pinyin) pair**, everywhere — `cardKey()`. 行 *xíng*
and 行 *háng* are two cards; knowing one does not mark the other. This governs
the known list, the card-list de-duplication in `loadCards()`, and the quiz
queue alike.

Known-list entries are `{ch, py, ts, deck}`. Entries written before this carried
no `py`; `getKnownIndex()` treats those as matching **any** reading of that
character, so no existing progress was invalidated. `removeFromKnown(mode, ch)`
without a reading clears every reading of the character (and any legacy entry);
passing a reading removes just that card.

`loadCards()` keeps the **first** row for each (Chinese, Pinyin) in manifest
order. This replaced a gloss-subset comparison that also weighed the English
column — over the full corpus it keeps 2,498 cards where the old rule kept
3,555, because 637 term+reading pairs are glossed differently in different
liturgies and only the first is now shown.

## The Quiz screen

A rolling self-test over the global card index (`#/quiz`), with no scheduling —
the page says so and points at the Anki export. **There is no start or end:**
`openQuiz()` restores the last settings from `quiz_prefs` (defaulting to New /
Type A) and deals a queue immediately; any setting change calls
`regenerateQuiz()`, which rebuilds the queue while keeping the score and
history.

Three settings: pool (New / Known), type (A / B), and a deck **dropdown**
defaulting to **Random** — every deck shuffled together — whose menu is a
checkbox tree mirroring the landing page's categories and sets, with whole
categories selectable. The card count beside it is the de-duplicated queue
length, recomputed on every toggle, so a term in five liturgies is counted and
asked once.

**The geometry is fixed on purpose.** `.qcard` has a set height and
`.quiz-controls` a set min-height, because revealing an answer roughly doubles
the card's content: if the box grew, the buttons would slide out from under the
pointer and the page would jump on every card. Long answers scroll inside the
card instead. A regression test asserts card height, card top, button top,
page height and scroll position are all identical across reveal, across the
next card, and across twenty cards in a row.

The card shows its deck name top-left, the 📖 Pleco and 📕 HanziCraft links in
the same two corners as the Anki note (same glyphs, same 0.4 opacity, same
per-platform behaviour), and nothing else. No prompt, no score line, no
keyboard legend — the known counter is the only running feedback.

Controls, centred beneath: **← Back** (slate) · **✗ Missed it** (red) · **✓ Got
it | + known** (green, one split control) · **Skip →** (slate).

The card mirrors the Anki note type — same palette (`#fdf6e3` on `#47321d`),
fonts and sizes, and the same collapsed **Shared by** expander.

The two pools differ in consequence, which is the whole point of the screen:

| Pool | Got it | Missed it | Manual |
| ---- | ------ | --------- | ------ |
| **New** | nothing | nothing | **+ Add to known**, which toggles back off |
| **Known** | nothing | `removeFromKnown()` — the term returns to your next deck | — |

**Skip** advances without scoring. **Back** returns to the previous card and
undoes what leaving it did, including re-adding a card the Known pool removed.

### Marking cards as known

**Building an Anki deck is what records progress.** `exportToAnki()` calls
`markExportedAsKnown()` after the download, adding every exported card to the
known list for the current mode, attributed to the set it came from, then
refreshes the table. Printing a PDF and downloading card data deliberately do
**not** touch the known list — this moved off `generatePDF()` when the app
became Anki-first.

### Study modes

Only **Type A** and **Type B** are offered. Mode `C` (custom field mapping)
still exists in `setStudyMode()` and `effectiveKnownMode()` so old state cannot
break the screen, but no button selects it.

Both modes present the cards in liturgy order. They differ only in what the
front of the card shows.

> **Removed:** a `frequency` column once re-ordered Type B. It was never
> finished — only 4 of 21 CSVs ever carried it, its counts were per-liturgy
> rather than corpus-wide, and the sort ran ascending. The column has been
> dropped from the CSVs and every code path, alias, and doc reference to it is
> gone. Do not reintroduce it as an ordering input without re-deriving the
> counts across the whole corpus first.

## Feedback board

A public board for bug reports and feature requests at `#/feedback`, posted
under a per-device alias — an adjective and a noun, e.g. *Still Ziggurat*,
*Alabaster Compass*, *Murmuring Pagoda* — derived from an id in `localStorage`.
73 adjectives (qualities, textures, colours) × 74 nouns from Buddhist, Sufi,
yogic, Babylonian/Sumerian and wider mystical vocabulary: 5,402 combinations.

The nouns are **objects, creatures, places and states only**. Terms a tradition
venerates are deliberately excluded — the Three Jewels (`Sangha` was removed),
awakening itself (`Bodhi`), and the names of gods in any of these pantheons —
so an alias reads as an image and never as a claim about the person holding it.
Implements like `Vajra` and architecture like `Stupa` and `Ziggurat` are in. Authors can edit and delete
their own posts; anyone can reply, one level deep. Deletes are soft, so replies
survive the post they answer.

**The board needs a backend to actually be public.** This app is a static page,
so `FEEDBACK_ENDPOINT` / `FEEDBACK_READ_ENDPOINT` / `FEEDBACK_API_KEY` at the
top of the feedback section in `index.html` are where you point it at one. Run
[`feedback-schema.sql`](feedback-schema.sql) against a Supabase project, paste
the three values in, and the same board serves every visitor. Until then the
page runs against `localStorage` and **says so in a banner** rather than
implying a post has been shared.

Two identifiers, deliberately distinct:

| Field | Visible | Purpose |
| ----- | ------- | ------- |
| `author_key` | yes | "same person" marker, drives the *you* badge |
| `edit_token` | **no** — the read view omits it | proves authorship for edit/delete |

Edits and deletes filter on `edit_token`, which the public view never returns,
so reading a post tells you nothing about how to change it. This is a soft
guard, not authentication; it is proportionate to a feedback board, and the
schema notes what to do if that stops being true.

## URLs

Every screen has a shareable URL:

| URL | Screen |
| --- | ------ |
| `#/` | Set browser |
| `#/cards/all` | Customize, everything selected |
| `#/cards/evening-ceremony` | Customize, one whole section |
| `#/cards/heart_sutra+gc_repent` | Customize, specific sets |
| `#/known/a`, `#/known/b` | Known-cards viewer |
| `#/quiz` | Quiz |
| `#/instructions` | Instructions |
| `#/methodology` | Methodology |
| `#/feedback` | Feedback board |

Selections stay readable and resolvable, so a pasted link rebuilds the same
selection.
