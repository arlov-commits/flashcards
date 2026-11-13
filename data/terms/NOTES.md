# Artful terms deck — notes and audit trail

Leitner flashcards for the "artful terms" Xiu is building: fallacies, argument forms, writing moves (Waldron,
Cammarata), named laws and heuristics, biases. Built 2026-11-12. Batch 1 = the tools he reaches for most;
the remaining Working Lexicon classes follow as later batches.

## Files
- `data/terms/artful-terms-batch1.csv` — 95 rows, UTF-8 with BOM. Columns: id, class, term, gloss, form, use,
  example, source, notes, checked.
- `tools/terms_batch1_rows.py` — the source of the CSV. Draft rows first, then a FIX table of every correction
  from the two independent checks, applied as overrides so the original draft stays readable.
  Run: `python3 -I tools/terms_batch1_rows.py data/terms/artful-terms-batch1.csv`
- `tools/term_cards_pdf.py` — prints the cards. Run:
  `python3 -I tools/term_cards_pdf.py data/terms/artful-terms-batch1.csv out.pdf`

## Card design (decided)
- Size and front type copied from the MSOD Pali cards: 63.5 x 49 mm, US Letter landscape, 4 x 4, fronts
  column-first, backs mirrored, print duplex FLIP ON SHORT EDGE; DejaVu Serif, term italic 15 pt.
- Backs deliberately sparser than the (unfinalised) Pali deck-2 backs, per Xiu.
- Two cards per row (Xiu chose 2 directions):
  A "recall": term + class tag  ->  gloss / general form (italic) / "when:" use line.
  B "name it": a concrete example + cue tag  ->  the term.
  All A cards print first, then all B cards (sheets 1-6 A, 7-12 B), so they cut into two stacks.

## Provenance and checks
- Sources per row are in the `source` column: the Working Lexicon Claude doc
  (https://claude.ai/code/artifact/ee304ec1-1019-4464-a91e-5b2a8f0b1275), our chats (dated), William Waldron,
  Making Sense of Mind Only (2023; page numbers from Claude's reading of the PDF on 2026-10-20), and Nick
  Cammarata, "Neural Networks Are Already Clean" (https://already-clean.goodfire.com/).
- Glosses were written by Claude (Xiu: checked glosses acceptable, but double-checked). Two independent checks:
  - C1, accuracy/attribution. Web-verified: all nine Cammarata quotes (verbatim, essay URL above);
    Strathern 1997 wording of Goodhart's law (Cambridge, European Review); principle of charity
    Wilson 1959 / Quine / Davidson (philarchive JACCSA-2); Merton, Science 159 (1968); Crichton 2002
    "Why Speculate?". From memory only, NOT fetched: Korzybski, Simon 1956, Campbell, Conway 1968, Gall 1975,
    Parkinson 1955, Peter 1969, Hofstadter (GEB), Brandolini, Sagan, Hitchens, Hanlon, Hickam, Sutton, Hume.
  - C2, card fit: each example must instantiate its term and only that term within the deck; fallacy examples
    must be fallacious, not merely misaimed; no example may give the answer away.
  - 44 of 95 rows were corrected; the `checked` column says which check and why.
- Waldron page numbers were not re-checked by either critic. "Mother Theresa [sic]" is kept as printed in
  Waldron p. 38 as Claude read it; confirm against the book.

## Open items (provisional until Xiu decides)
- Batch order after batch 1 (Claude's proposal: Evidence and proof, Frame words, Medicine, then the rest).
- Whether "satisficing", "Pareto principle" etc. belong under "named law" or a separate "concept" tag.
- Not yet printed on a real printer: check sheet 1 alignment before printing all 12.

## 2026-11-13: first print = writing moves, named laws and biases only
- Xiu asked to print only the writing moves, named laws and biases first; the fallacies and reasoning forms go
  on a separate pass later.
- `data/terms/artful-terms-batch1a-moves-laws-biases.csv` = batch 1 filtered to class move, heuristic, bias and
  verdict (Pyrrhic and Procrustean came from the named-heuristics section, so they ride along): 61 rows, 122
  cards on 8 sheets (sheets 1-4 recall, 5-8 name-it; sheet 8 holds 10 cards). Rows unchanged from batch 1.
- Still to print: the 34 fallacy and reasoning rows (class fallacy, form) of artful-terms-batch1.csv.
