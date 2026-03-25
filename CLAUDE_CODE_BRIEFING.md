# Claude Code Briefing: Buddhist Liturgy Flashcard App v1.0

## WHAT TO BUILD

A single-page web app hosted on GitHub Pages where Buddhist students select liturgical vocabulary sets, customize flashcard appearance, preview cards, and download printable PDFs or Anki CSVs. No backend, no database, no accounts. Everything runs in the browser.

**Read `FLASHCARD_APP_SPEC.md` for the full project context.** This briefing is the build instructions.

---

## STEP 1: CREATE THE GITHUB REPO

```bash
# Create new repo called "flashcards" under arlov-commits
# Enable GitHub Pages on the main branch, root folder
```

Repo structure:
```
/
  index.html              ← The entire app (single file, inline CSS/JS)
  manifest.json           ← Registry of available card sets (app config — stays JSON)
  /data
    /chinese
      incense-praise.csv
      heart-sutra.csv
      amitabha-praise.csv
      three-refuges.csv
      puxian-exhortation.csv
      merit-transfer.csv
  sample-template.csv     ← For custom uploads
  README.md
  FLASHCARD_APP_SPEC.md   ← Full project spec (for future reference)
```

**I have already converted the Excel data to JSON. The manifest.json and all 6 JSON files are provided. Commit them as-is.**

---

## STEP 2: DATA FORMAT

### CRITICAL DESIGN PRINCIPLE: Language-Agnostic Architecture

The app must NOT hardcode field names like "chinese", "pinyin", "english". It must read field metadata from the manifest and data files dynamically. This is because:
- Pali data will have different fields (pali, romanized, english_1, english_2, english_3)
- Future traditions could have entirely different structures
- The app should handle ANY set of fields as long as the manifest describes them

### manifest.json
```json
{
  "traditions": {
    "chinese": {
      "display_name": "Chinese Liturgy",
      "available": true,
      "fields": [
        { "key": "chinese", "label": "Chinese", "type": "target_lang", "font_category": "chinese" },
        { "key": "pinyin", "label": "Pinyin", "type": "romanization", "font_category": "english" },
        { "key": "english", "label": "English", "type": "translation", "font_category": "english" }
      ],
      "default_front": ["chinese", "pinyin"],
      "default_back": ["english"],
      "tag_field": "ch_tag",
      "sets": {
        "incense_praise": {
          "file": "data/chinese/incense-praise.json",
          "display_tag": "香讚",
          "eng_name": "Incense Praise",
          "total_cards": 40,
          "active_cards": 40
        }
      }
    },
    "pali": {
      "display_name": "Pāli Liturgy",
      "available": false,
      "fields": [],
      "sets": {}
    }
  }
}
```

The `fields` array tells the app what columns exist and how to categorize them. The `default_front` and `default_back` arrays tell the app which fields go where by default, but the user can rearrange them. The `font_category` tells the app which font picker applies to that field.

### Each card set is a CSV file (e.g., incense-praise.csv)
```csv
include,chinese,pinyin,english_def,multichar,ch_tag,eng_tag
1,香,xiāng,incense; fragrance,False,香讚,incense_praise
1,香讚,xiāng zàn,incense praise,True,香讚,incense_praise
```

**CSV encoding: UTF-8 with BOM** (utf-8-sig) so Excel opens Chinese characters correctly.

The app loads these CSVs using **PapaParse** with `header: true`. No JSON data files — CSV is the canonical format for card data. This means:
- What's in the repo is the same format students upload
- Art can edit card data directly in Excel and commit CSVs
- No conversion step between editing and deploying
- The manifest.json (app config) remains JSON — only card data is CSV
```

### How the app uses this:
- `include`: Default checkbox state per card. **NOT a filter.** All cards are loaded and shown. Cards with `include=0` are unchecked by default but visible — the student can re-enable them. Cards with `include=1` are checked by default but the student can uncheck them. Think of it as "recommended for most students" vs "optional/basic."
- `multichar`: A styling hint. When true, pinyin/romanization renders bold in the PDF. The app reads this flag generically — it doesn't need to know what "multichar" means linguistically.
- The actual content fields (`chinese`, `pinyin`, `english_def`) are read dynamically based on the manifest's `fields` array. The app iterates over the fields, not over hardcoded column names.
- **Note:** PapaParse will read `include` as a string ("1"/"0") and `multichar` as a string ("True"/"False"). Coerce these on load: `include = row.include === "1"` and `multichar = row.multichar === "True"`.

---

## STEP 3: BUILD THE APP (index.html)

### Tech Stack (all loaded from CDNs, no build step)
- **jsPDF** — PDF generation in-browser (https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.2/jspdf.umd.min.js)
- **JSZip** — ZIP bundling for PDF + preferences export (https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js)
- **PapaParse** — CSV parsing for user uploads and Anki export (https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js)
- **Google Fonts** — Chinese + English fonts via CDN
- No frameworks. No React. No build tools. Plain HTML/CSS/JS.

### UI Flow (step by step)

**Screen 1 — Landing / Category Selection**
- Clean, parchment-toned aesthetic (similar to claude.ai's warm beige, NOT stark white)
- Title: "Buddhist Liturgy Flashcards" (or similar)
- Brief intro text explaining what the app does (2-3 sentences)
- Category buttons: "Chinese Liturgy" (active), "Pāli Liturgy" (grayed out / coming soon)
- Link to documentation / how-to-use guide (can be a collapsible section)
- Mobile-friendly from the start

**Screen 2 — Set Selection**
- Shows available card sets loaded from manifest.json
- Each set displayed as a card/tile: English name, Chinese name (ch_tag), card count
- Checkboxes — user can select ONE or MULTIPLE sets
- Show total card count updating as sets are checked/unchecked
- "Next" button proceeds to customization

**Screen 3 — Customization**
- **Card content mapping (driven by manifest `fields` array, NOT hardcoded):**
  - "Front side" — multi-select checkboxes from available fields (default from manifest's `default_front`)
  - "Back side" — multi-select checkboxes from remaining fields (default from manifest's `default_back`)
  - For Chinese, the defaults result in: Front = Chinese + Pinyin, Back = English (Version A)
  - User can switch to: Front = Chinese only, Back = Pinyin + English (Version B)
  - When Pali is added later, its fields auto-populate from the manifest — no code changes needed
- **Font selection (driven by manifest `font_category` per field):**
  - One font picker per unique font_category in the selected tradition's fields
  - For Chinese tradition: "Chinese font" picker + "English/Pinyin font" picker
  - Chinese fonts: Noto Sans SC, Noto Serif SC (default), Ma Shan Zheng, Long Cang, ZCOOL XiaoWei, Liu Jian Mao Cao
  - English fonts: Lora, DM Sans, Crimson Text (default), Caveat, Spectral, Patrick Hand
- **Layout:**
  - Grid: 4×4 (default) | 4×5 (future — can be grayed out for v1.0)
- **Card list:**
  - Scrollable list of all cards in the selected sets
  - Each card shows all content fields (read dynamically from the data, not hardcoded as "Chinese | Pinyin | English")
  - Checkbox to include/exclude individual cards
  - Cards where `include=0` in the data are unchecked by default but visible — student can re-enable
  - Cards where `include=1` are checked by default — student can uncheck
  - Search/filter box to find specific cards (searches across all fields)
  - "Select All" / "Deselect All" buttons
  - Show count: "X of Y cards selected"
- **Summary:** "This will generate X cards across Y pages (double-sided)"

**Screen 4 — Preview & Download**
- In-browser preview of the first few cards (front and back) using selected fonts
- Preview doesn't need to be pixel-perfect PDF — just a visual representation
- Download buttons:
  - "Download PDF (Version A: Chinese+Pinyin front)" — generates and downloads
  - "Download PDF (Version B: Chinese-only front)" — generates and downloads
  - "Download Anki CSV" — tab-separated, front/back based on selected mapping
  - "Download All (ZIP)" — both PDFs + Anki CSV + preferences.json
- Loading indicator during PDF generation ("Preparing fonts... Generating cards...")

### PDF Generation (CRITICAL — must match Python layout)

Port the logic from `flashcards-xlsx2.py` to jsPDF. Key specs:

```
Orientation: Landscape
Paper: US Letter (279.4mm × 215.9mm)
Margins: 7.62mm all sides
Grid: 4 columns × 4 rows = 16 cards per page
Card width: (279.4 - 2×7.62) / 4 ≈ 66.04mm
Card height: (215.9 - 2×7.62) / 4 ≈ 50.17mm
Grid lines: light gray (#C8C8C8) rectangles
```

**Version A (Chinese + Pinyin front, English back):**
- FRONT: Chinese centered in card (28pt default, 24pt for 3+ chars, 20pt for 5+ chars)
- FRONT: Pinyin below Chinese (14pt, BOLD if multichar=true)
- BACK: English centered (11pt, word-wrap within card)
- BACK: ch_tag in gray 8pt, bottom-right corner
- BACK: Columns MIRRORED (col 0↔3, 1↔2) for double-sided printing

**Version B (Chinese-only front, Pinyin + English back):**
- FRONT: Chinese centered (32pt default, 26pt for 3+, 22pt for 5+)
- BACK: Pinyin centered near top (14pt or 11pt if long string, BOLD if multichar)
- BACK: Horizontal line separator across card (with padding)
- BACK: English below line (11pt, word-wrap)
- BACK: ch_tag in gray 8pt, bottom-right
- BACK: Columns MIRRORED

**Font embedding in PDF:**
- Chinese: Use selected Google Font. Load the .ttf via fetch, register with jsPDF.addFont()
- For v1.0, it's acceptable to start with Noto Serif SC as the only embedded Chinese font if font switching in PDF is too complex. The font picker can still work for the preview.
- English: Use the selected Google Font, same approach
- Pinyin with tone marks (ā, é, ǐ, etc.): Must render correctly — test this

**Anki CSV export:**
- Tab-separated values
- First column: front content (based on user's field mapping)
- Second column: back content
- Third column: tags (the eng_tag)
- No header row (Anki convention)

### localStorage

Save to localStorage on every meaningful user action:
```json
{
  "selectedSets": ["heart_sutra", "incense_praise"],
  "frontMode": "chinese_pinyin",
  "chineseFont": "Noto Serif SC",
  "englishFont": "Crimson Text",
  "excludedCards": ["heart_sutra:42", "incense_praise:3"],
  "gridLayout": "4x4"
}
```

On page load, restore from localStorage if present.

### URL Permalink

Encode the current state into the URL hash:
```
#sets=heart_sutra,incense_praise&front=chinese_pinyin&cfont=noto-serif&efont=crimson&exclude=hs42,ip3
```

For large states, compress with base64:
```
#s=eyJzZXRzIjpbImhlYXJ0X3N1dHJhIl0sImZyb250Ij...
```

On page load, URL hash takes priority over localStorage.

### Custom File Upload

- Accept .csv and .xlsx files
- Validate that the file has at least 2 columns (something for front, something for back). No specific column names required — the app will let the user map whatever columns exist to front/back
- If the file has columns matching known field names (chinese, pinyin, english, pali, romanized, etc.), auto-detect and pre-fill the mapping
- Provide sample-template.csv for download showing the Chinese format as an example
- Uploaded data is processed identically to built-in sets — same customization, preview, and export
- File never leaves the browser

---

## STEP 4: STYLING

- **Parchment/warm aesthetic** — NOT stark white. Think claude.ai's warm beige tones.
- Background: warm off-white (#f5f0eb or similar)
- Text: warm dark brown/black
- Accents: muted gold or deep red (Buddhist aesthetic)
- Clean, readable, calming
- Mobile-responsive (students will use this on phones)
- No heavy frameworks — just well-written CSS
- Smooth transitions between screens (doesn't need to be a SPA — can be show/hide sections)

---

## STEP 5: DEPLOY

1. Commit all files to the `main` branch
2. Enable GitHub Pages: Settings → Pages → Source: main branch, / (root)
3. Live URL will be: `https://arlov-commits.github.io/flashcards/`
4. Test on mobile and desktop

---

## WHAT TO DEFER (NOT in v1.0)

- Pali liturgy support (Phase 2)
- 4×5 grid layout option (Phase 2)
- Custom font upload (decided against — curated list only)
- User accounts / cloud sync (maybe never)
- Documentation/how-to page (can be a simple collapsible section for now)

---

## FILES PROVIDED

You should have these files to commit directly:

1. `manifest.json` — the card set registry (JSON — this is app config, not card data)
2. `data/chinese/incense-praise.csv` — 40 cards
3. `data/chinese/heart-sutra.csv` — 104 cards (90 active)
4. `data/chinese/amitabha-praise.csv` — 105 cards (102 active)
5. `data/chinese/three-refuges.csv` — 61 cards (30 active)
6. `data/chinese/puxian-exhortation.csv` — 49 cards (36 active)
7. `data/chinese/merit-transfer.csv` — 61 cards (44 active)
8. `FLASHCARD_APP_SPEC.md` — full project spec for reference
9. `flashcards-xlsx2.py` — original Python PDF script for reference (keep in repo for PDF layout porting, don't deploy to site)

All CSVs are UTF-8 with BOM encoding. Chinese characters and pinyin diacritics are verified intact.

---

## SUMMARY

Build a single `index.html` that:
1. Loads card sets from JSON files in the repo
2. Lets students pick sets, customize fonts, deselect known cards
3. Shows a preview
4. Generates pixel-accurate printable PDFs (matching the Python layout) in-browser
5. Exports Anki CSVs
6. Saves/restores preferences via localStorage, URL hash, and JSON file export
7. Runs forever on GitHub Pages with zero maintenance
