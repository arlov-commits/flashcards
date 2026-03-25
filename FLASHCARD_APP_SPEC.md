# Buddhist Liturgy Flashcard App — Project Specification

**Last updated:** March 24, 2026  
**Status:** Planning / Scoping  
**Live URL (future):** `arlov-commits.github.io/flashcards` (or similar)

---

## 1. Project Vision

A free, permanent web app where Buddhist students can generate printable flashcards for liturgical vocabulary. Designed to run forever on GitHub Pages with zero cost, zero maintenance, and zero human intervention.

### Design Principles
- **Zero-cost forever:** Hosted on GitHub Pages. No backend, no database, no recurring fees.
- **Portable:** Pure HTML/CSS/JS + JSON data. Can be moved to any hosting provider by copying files.
- **Future-proof:** If community support materializes, can move to a custom domain on shared hosting. If hosting goes away, falls back to GitHub Pages URL and everything still works.
- **Ordination-proof:** Must remain functional indefinitely without active maintenance or financial support.

---

## 2. Supported Languages / Traditions

### Phase 1: Chinese Liturgy
- Source: Chinese Buddhist liturgical texts (已有 canonical liturgy)
- ~10–20 chunks, varying from 2–3 pages to ~30 pages each
- Priority order: daily chanting → weekly/occasional → long texts
- Long texts (e.g., Shurangama Mantra) broken into sub-sections by how they're actually chanted

#### Completed Sections (6 in lexicon.xlsx, 342 active cards)
| Section | eng_tag | ch_tag | Active Cards |
|---------|---------|--------|------------|
| Amitabha Praise | amitabha_praise | 佛讚 | 102 |
| Heart Sutra | heart_sutra | 心經 | 90 |
| Merit Transfer | merit_transfer | 回向 | 44 |
| Incense Praise | incense_praise | 香讚 | 40 |
| Puxian Exhortation (Samantabhadra) | puxian_exhortation | 普賢 | 36 |
| Three Refuges | three_refuges | 三皈依 | 30 |

#### Planned Sections (not yet generated)
**Morning Chanting:**
- Shurangama Mantra (long — sub-sections needed)
- Medicine Buddha Mantra
- Ode to the Patriarch (?)

**Evening Chanting:**
- Amitabha Sutra
- Eighty-Eight Buddhas Repentance
- Incense Offering (Mengshan)
- Vow to be Reborn in the Pure Land

**Other:**
- Meal Offering
- Meal Blessing
- Great Compassion Repentance
- 100+ Pure Conduct Vows (Avatamsaka Ch. 11)
- Universal Door of Guanyin Bodhisattva Chapter

### Phase 2: Pali Liturgy (future)
- Source: Theravada chanting texts
- ~100 chunks, each ~2–3 pages
- Will require different data fields (Pali script, romanized Pali, English)
- May include 2–3 English translation sources (unlike Chinese which uses one canonical source)
- Romanization scheme TBD — consult with Pali monk community
- Diacritical marks (ā, ī, ū, ṃ, ṇ, etc.) must be handled correctly in data, fonts, and PDF output
- Additional Pali-friendly fonts needed in the curated font selection

---

## 3. Data Structure

### Chinese Cards — Actual Column Structure (from `lexicon.xlsx`)
| Column | Type | Description |
|--------|------|-------------|
| `include` | 0 or 1 | Whether card is active (0 = excluded, e.g., very basic characters like 一, 不, 是 that students already know) |
| `chinese` | text | Traditional Chinese character(s) |
| `pinyin` | text | Romanized pronunciation with tone marks |
| `english_def` | text | English definition PLUCKED from canonical translation (not reinvented) |
| `multichar` | True/False | Whether this is a compound term (binome, trinome, etc.) — rendered bold in pinyin on PDF |
| `ch_tag` | text | Chinese name of the liturgy section (e.g., 香讚, 心經, 佛讚) |
| `eng_tag` | text | English name of the liturgy section (e.g., incense_praise, heart_sutra, amitabha_praise) |

**Current database size:** 420 cards across 6 sections, 342 active (include=1), 78 excluded

### Current Tag Distribution (include=1 only)
| Section | eng_tag | ch_tag | Card Count |
|---------|---------|--------|------------|
| Amitabha Praise | amitabha_praise | 佛讚 | 102 |
| Heart Sutra | heart_sutra | 心經 | 90 |
| Merit Transfer | merit_transfer | 回向 | 44 |
| Incense Praise | incense_praise | 香讚 | 40 |
| Puxian Exhortation | puxian_exhortation | 普賢 | 36 |
| Three Refuges | three_refuges | 三皈依 | 30 |

### Grouping Logic (Chinese)
The `multichar` flag controls grouping. Rules from instructions:

**Characters that stand alone (multichar=False):**
- Characters with independent meaning (e.g., 香 xiāng = incense)
- Characters that are part of translated (non-phonetic) compounds can ALSO appear standalone AND as compounds (e.g., 普 pǔ = universal appears alone AND as 普賢 pǔxián = Universal Worthy)

**Characters that must be grouped (multichar=True):**
- Phonetic transliterations MUST stay together (e.g., 阿彌陀佛 = Amitabha Buddha, 舍利弗 = Shariputra) — individual syllables like 彌 mí are meaningless alone
- Binomes/trinomes that form meaningful units (e.g., 雲蓋 = cloud canopy, 觀自在 = Avalokiteshvara)

**What NOT to include:**
- Whole sentences or long phrases — too much for a flashcard
- Mantras (e.g., gate gate paragate...) — no point memorizing transliterations
- Full titles

**Key distinction:** Translated compounds (普賢 pǔxián) CAN be broken up because each character has meaning. Phonetic transliterations (舍利弗 shèlìfú) CANNOT — the individual characters have no relevant meaning.

### Source Liturgy Format (e.g., `Amita_Zan.xlsx`)
- Multi-column layout: each column = one character position
- Alternating rows: Chinese characters → pinyin → blank → English sentence → Chinese → pinyin → ...
- English translations span full lines (not word-by-word aligned)
- AI must "pluck out" individual English definitions from the full English sentence and pair them to Chinese/pinyin

### Pali Cards (Future — TBD)
| Column | Description |
|--------|-------------|
| Pali Script | Original Pali text |
| Romanized Pali | With proper diacriticals |
| English (Source 1) | Translation from first source |
| English (Source 2) | Translation from second source (optional) |
| English (Source 3) | Translation from third source (optional) |
| Source Tag | Identifies the chanting section |

---

## 4. Data Generation Pipeline

### Current Workflow (Chinese)
1. **Source material:** Canonical Chinese liturgy texts, already digitized in Excel from prior project
   - Format: Multi-column spreadsheet with one character per column
   - Alternating rows: Chinese → pinyin → blank → English sentence
   - Example source file: `Amita_Zan.xlsx` (Amitabha Praise — 70 rows, 8 columns)
2. **AI extraction:** Upload each section's Excel to Claude with detailed instructions to:
   - Extract every character/phrase
   - Generate pinyin
   - **PLUCK** English directly from the corresponding English line in the source (no reinvention/reinterpretation)
   - Apply grouping rules: standalone characters, binomes, transliterations kept whole
   - Exclude mantras, full sentences, long phrases, and full titles
   - Group output by character length (1, 2, 3+)
3. **Cross-check:** Compare Claude output against DeepSeek output on the same task
   - Known issue: DeepSeek struggles to follow instructions — includes oversized chunks (whole mantras, long sentences), forgets corrections mid-conversation
   - Claude handles instructions significantly better
4. **Manual verification:** Art reviews and catches errors that slip through
   - Common issues: wrong grouping decisions, English defs that don't match the source, transliterations incorrectly broken up
5. **Output:** Structured Excel (`lexicon.xlsx`) with 7 columns (include, chinese, pinyin, english_def, multichar, ch_tag, eng_tag)

### AI Prompt Instructions (from `instructions2.txt`)
Key rules given to the AI:
- English definitions must be PLUCKED from the source English line, not reinvented
- Phonetic transliterations (阿彌陀佛, 舍利弗) must stay as one unit — never break up
- Meaningless standalone syllables (須, 彌, 菩, 薩) must only appear in compounds
- Translated compounds (普賢) CAN be broken up AND also grouped
- Mantras should be excluded entirely
- No whole sentences or long phrases — must fit on a flashcard as a meaningful unit
- After initial output, Art may provide an alternate version to cross-reference for missed items
- The `multichar` flag is set based on whether the term is a compound

### Known Challenges
- English doesn't always cleanly map 1:1 to Chinese due to translation interpretation differences
- Grouping decisions require human judgment
- Verification step is partially manual and time-consuming
- *Art will document the detailed AI prompt approach and grouping rules separately*

### Future Workflow (Pali)
- Similar pipeline but targeting Pali → Romanized Pali → English
- Multiple English translation sources to reconcile
- Pipeline developed for Chinese should mostly transfer
- Volume is higher (~100 chunks) but each chunk is shorter

---

## 5. App Features

### Core Functionality
- [ ] Browse card sets by chapter/liturgy section (Source Tag)
- [ ] Choose what data field goes on front vs. back of card
- [ ] Preview cards in-browser before downloading
- [ ] Deselect individual cards the student already knows
- [ ] Language-agnostic field handling (app reads whatever columns exist in the dataset)

### Customization
- [ ] Font selection for front and back independently
- [ ] Curated font list (see Section 7 below)
- [ ] Card layout options:
  - **Current:** 4×4 grid on letter-size landscape (16 cards/page, double-sided)
  - **Future:** 4×5 grid option (20 cards/page) — slightly smaller cards but more per page
- [ ] Students can upload their own card data files (CSV/Excel) if in the correct format
  - App validates column structure against expected format
  - Sample template provided for download
  - File is processed entirely in-browser — never leaves the student's device

### Export Formats
- [ ] **Printable PDF:** 4×4 landscape grid, double-sided, matching Art's existing Python layout logic
  - Generated in-browser using jsPDF (no server needed)
  - Art's Python script to be ported to JavaScript
- [ ] **Anki-compatible CSV:** Simple TSV/CSV download with selected fields mapped to front/back
- [ ] **Preferences file:** Bundled in a ZIP with the PDF
  - Human-readable summary at top (set, fonts, card count, etc.)
  - Raw JSON for drag-and-drop restore
  - Permalink URL at bottom (see Section 6)

### Progress / Preferences
- [ ] **localStorage:** Day-to-day persistence in the student's browser
  - Remembers which cards marked as "known"
  - Remembers customization preferences (fonts, layout, field mapping)
  - Tied to device/browser — not synced across devices
- [ ] **Export/Import JSON file:** Manual backup for device transfers
  - "Save Progress" → downloads small JSON file
  - "Load Progress" → drag-and-drop or file picker to restore
- [ ] **URL-encoded state (permalink):**
  - Entire preference state serialized into URL hash
  - Example: `site.com/#set=amitabha&front=chinese&back=pinyin&font=mashanzheng&exclude=12,47`
  - For large exclusion lists, state compressed via base64
  - Students can bookmark, share with classmates, or paste into notes
  - Included at bottom of preferences file in ZIP export

---

## 6. Permalink / URL State System

When a student configures their session, the app encodes the full state into the URL:
- Selected card set
- Front/back field mapping
- Font choices
- Excluded card IDs
- Any other preferences

This URL can be:
- Bookmarked for personal use
- Shared with classmates (they open the link and get the same configuration)
- Saved in the preferences text file (inside the ZIP download)
- Used as a lightweight "save state" that requires zero infrastructure

For large states (200+ excluded cards), base64 compression keeps the URL manageable.

---

## 7. Font Selection (Curated)

All fonts are open-licensed via Google Fonts. No hosting cost.

### Chinese Fonts
| Font | Style | Notes |
|------|-------|-------|
| Noto Sans SC | Clean modern sans-serif | Highly readable, good default |
| Noto Serif SC | Traditional Song/Ming style | Classic textbook feel |
| Ma Shan Zheng | Brush calligraphy | Temple inscription energy |
| Long Cang | Casual handwritten | Good for informal study |
| ZCOOL XiaoWei | Elegant semi-calligraphic | Nice middle ground |
| Liu Jian Mao Cao | Grass script / wild cursive | More artistic |

### English Fonts
| Font | Style |
|------|-------|
| Lora | Elegant serif |
| DM Sans | Clean modern sans |
| Crimson Text | Scholarly serif |
| Caveat | Handwritten casual |
| Spectral | Refined reading serif |
| Patrick Hand | Friendly handwriting |

### Pali Fonts (TBD — Phase 2)
- Must support full diacritical character set (ā, ī, ū, ṃ, ṇ, ṭ, ḍ, ṅ, ñ, ḷ)
- Candidates to be evaluated when Pali phase begins

### Font Loading Strategy
- Google Fonts CDN for web preview (auto-subsets to displayed characters)
- Full font files lazy-loaded only when "Generate PDF" is triggered
- Brief loading indicator ("Preparing fonts...") on first PDF generation

---

## 8. Technical Architecture

### Stack
- **Hosting:** GitHub Pages (free, permanent)
- **Frontend:** Single HTML file with inline CSS/JS (no build step, no framework)
- **Data:** JSON files in the GitHub repo (converted from Excel)
- **PDF generation:** jsPDF (in-browser)
- **CSV parsing (for user uploads):** PapaParse or SheetJS
- **ZIP bundling:** JSZip (for PDF + preferences export)
- **No backend. No database. No authentication. No server-side anything.**

### File Structure (in GitHub repo)
```
/flashcards
  index.html          ← The entire app
  /data
    /chinese
      heart-sutra.json
      incense-praise.json
      amitabha-praise.json
      ...
    /pali (future)
      morning-puja.json
      evening-puja.json
      ...
  /fonts (if self-hosting any)
  sample-template.csv  ← For custom uploads
  README.md
```

### Portability
- If moved to custom domain: copy the folder, done
- If moved to hosting with a backend: add database layer as enhancement, not dependency
- If hosting disappears: GitHub Pages URL still works
- All data is in the repo — versioned, backed up, permanent

---

## 9. Print Layout (from `flashcards-xlsx2.py`)

### Current Python Implementation Details
- **Library:** fpdf (Python)
- **Orientation:** Landscape
- **Paper:** US Letter (279.4mm × 215.9mm)
- **Margins:** 7.62mm on all sides
- **Grid:** 4×4 (16 cards per page)
- **Card size:** ~66mm wide × ~50mm tall (calculated from available space)
- **Grid lines:** Light gray (200, 200, 200) rectangles

### Two PDF Versions Generated

**Version A — Chinese + Pinyin on front, English on back:**
- Front: Chinese characters centered (font size scales: 28pt default, 24pt for 3+ chars, 20pt for 5+ chars)
- Front: Pinyin below Chinese (14pt, **bold if multichar**)
- Back: English centered (Helvetica 11pt, multi-cell for wrapping)
- Back: Source tag (ch_tag) in small gray text, bottom-right corner (8pt)
- Back columns MIRRORED (col 3→0, 2→1, etc.) for double-sided printing alignment

**Version B — Chinese only on front, Pinyin + English on back:**
- Front: Chinese characters centered (larger: 32pt default, 26pt for 3+, 22pt for 5+)
- Back: Pinyin at top (14pt or 11pt if long, **bold if multichar**)
- Back: Horizontal line separator
- Back: English below line (Helvetica 11pt, multi-cell)
- Back: Source tag bottom-right
- Back columns MIRRORED for double-sided printing

### Fonts Used (Python version)
- Chinese characters: Noto Serif SC Regular
- Pinyin: Microsoft YaHei (msyh.ttc)
- English: Helvetica (built-in)

### Key Implementation Notes for JS Port
- Column mirroring on back pages is critical for double-sided printing
- Font size scaling based on character count
- Multichar flag controls bold styling on pinyin
- Source tag rendered small and gray in corner — non-intrusive
- The `include` flag filters cards before generation
- Tags can be filtered individually or in combination
- The `FILTER_INCLUDE` and `FILTER_TAGS` config allows flexible subset generation

### Future: 4×5 Grid Option
- 20 cards per page
- Slightly smaller cards, more efficient for vocabulary drilling
- To be added as a layout option in the UI

---

## 10. Phases & Roadmap

### Phase 1: Chinese Launch (MVP)
- [ ] Convert first 3–5 Chinese datasets from Excel to JSON
- [ ] Build the app (single HTML file)
- [ ] Core features: browse sets, field mapping, font selection, preview, PDF export, Anki CSV export
- [ ] Deploy to GitHub Pages
- [ ] Students can start using it immediately

### Phase 2: Polish & Expand Chinese
- [ ] Add remaining Chinese datasets as they're verified
- [ ] Add custom file upload support
- [ ] Add localStorage progress tracking
- [ ] Add export/import preferences (JSON file + ZIP bundle)
- [ ] Add URL permalink state system
- [ ] Add 4×5 grid layout option

### Phase 3: Pali Expansion
- [ ] Consult with Pali monk community on romanization scheme
- [ ] Evaluate and add Pali-friendly fonts
- [ ] Adapt data pipeline for Pali (multiple English sources)
- [ ] Generate first Pali datasets
- [ ] Update app UI to handle Pali field structure
- [ ] Deploy Pali card sets

### Phase 4 (Optional): Community Hosting
- [ ] If community support exists: purchase domain, add to shared hosting
- [ ] Database-backed progress sync (Supabase or similar) as enhancement layer
- [ ] Automated database backups to external location
- [ ] Migration plan documented for hosting changes

---

## 11. Open Questions / TBD

- [ ] Exact priority order of Chinese liturgy sections for data generation
- [ ] Grouping rules documentation (Art refining separately)
- [ ] AI prompt template for data extraction (Art to document)
- [ ] Python print script details (Art to share)
- [ ] Pali romanization scheme preference (consult monk community)
- [ ] Pali font candidates (evaluate when Phase 3 begins)
- [ ] Whether any Chinese fonts need self-hosting vs. Google Fonts CDN

---

## 12. Related Projects (Same GitHub Account)

| Project | URL | Backend | Status |
|---------|-----|---------|--------|
| Team Scheduler | `arlov-commits.github.io/agroforest` | Supabase (free tier) | Live |
| Project 2 | TBD | TBD | TBD |
| Flashcard App | TBD | None (static) | Planning |

---

*This document is updated live during planning conversations. Last conversation: March 24, 2026.*
