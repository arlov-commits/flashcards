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

## 2026-11-14: pre-print verification of the moves / laws / biases print (61 rows, 122 cards)
- Card structure: `pairing_check.py` read the printed PDF by text position and confirmed all 122 faces are
  present, each front sits behind its mirrored back (short-edge duplex), every face matches its CSV row,
  nothing overflows a card, smallest type 8 pt. (Script kept in the session scratchpad, not the repo.)
- V1, Waldron: Xiu's PDF of Making Sense of Mind Only has no text layer, so pages 20-340 were OCR'd with
  tesseract and every quote searched; book pages read from the printed running heads. Confirmed: p. 14
  "depend upon mind", p. 26 transposed questions, p. 38 "Mother Theresa" (as printed), p. 39 "do not explain",
  p. 42 in-dependent, p. 55 basis/object, p. 56 vi- "division" and the refrigerator hum, p. 78 "undercut the very
  aim" / "We call this the Abhidharma Problematic", p. 79 psycho-logical space, p. 84 "what we will call the
  Abhidharma Problematic", p. 86 synchronically/diachronically, p. 97 "a metaphor (not a dharma)", p. 104
  "from deconstructing essences logically to showing how to stop imputing them psychologically", p. 116
  "explanatorily vacuous", pp. 40/128/317 "conceptual cul-de-sac", p. 160 remedially/causally/soteriologically
  (Waldron's paraphrase of the Samdhinirmocana), p. 216 trick birthday candles, p. 217 rubber hand, p. 231
  habits -> "the habitats we inhabit" and the skin-encapsulated boundary (the "habitats" idea builds on a
  William Paden quote on the same page), p. 241 "just another perception", p. 262 binding problem.
  Fixed: two quotes restored to exact wording (relocated boundary, inline gloss), one constructed example
  replaced by Waldron's own sentence (paired axes), page numbers corrected (contrastive compression,
  evaluative compound).
- V2, named laws: independent web check. Verified via source: Campbell (Eval. & Program Planning 2, 1979,
  citation), Conway (melconway.com, Datamation 1968), Zwicky/frequency illusion (Language Log), Crichton 2002,
  Brandolini 2013, Strathern 1997, Peter (Britannica), Hanlon (Quote Investigator), Hume Treatise 3.1.1.27
  (davidhume.org), Chesterton The Thing 1929 (chesterton.org), Streisand/Masnick (Techdirt), Overton
  (mackinac.org), Lindy (Ord, arXiv 2308.09045), satisficing (Palgrave; Simon 1956), zebras (Quote
  Investigator), curse of knowledge (Camerer et al. 1989, citation), Merton 1968 (PubMed). NOT verified from a
  primary source: Parkinson, Hickam (fetch blocked); Hitchens, Sutton, Sagan, Hofstadter, Gall, rubber duck,
  cobra effect (search snippets only); Korzybski, bikeshedding, yak shaving, Pareto, Buridan, Occam, lectio
  difficilior, survivorship, streetlight (general knowledge only). No false attribution was found.
  Fixed: 4 glosses tightened (Campbell, Peter, satisficing, Hanlon), 4 examples replaced (Hitchens, Gall,
  Sutton, Overton), 2 class tags (Gell-Mann -> bias, Buridan's ass -> new "paradox" tag).
- Every change is in FIX2 in tools/terms_batch1_rows.py; the `checked` column records it per row.
