# term_cards_pdf.py
# Version 1.1 (tags: reasoning / named law / bias / evaluative word added after the independent checks)
# Prints double-sided Leitner cards for the "artful terms" deck (fallacies, argument forms, writing moves, heuristics).
# Each CSV row gives two cards:
#   A  "recall":   front = term (italic 15 pt, as the MSOD Pali deck) + class tag;  back = gloss / form / use
#   B  "name it":  front = a concrete example + cue tag ("name the fallacy");       back = the term (italic 15 pt)
# All A cards come first, then all B cards, so each can be cut and boxed as its own stack.
# Geometry kept from the MSOD Pali cards (63.5 x 49 mm, US Letter landscape, 4 x 4 per sheet, fronts laid out
# column-first, back columns mirrored). Print double-sided, FLIP ON SHORT EDGE. Black and white; greys only for
# the tag, the secondary back lines and the cut guides.
# Usage: python3 -I term_cards_pdf.py <cards.csv> <out.pdf>
import csv, sys
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

src, dst = sys.argv[1], sys.argv[2]
CARD_W, CARD_H = 2.5 * 25.4, 49.0
PAGE_W, PAGE_H = [v / mm for v in landscape(letter)]
COLS, ROWS = 4, 4
X0, Y0 = (PAGE_W - COLS * CARD_W) / 2, (PAGE_H - ROWS * CARD_H) / 2
PAD = 4.0          # inner margin, mm
TAG_SIZE = 6.0     # class / cue tag, pt
FD = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("R", FD + "DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("I", FD + "DejaVuSerif-Italic.ttf"))

TAG = {"fallacy": "fallacy", "form": "reasoning", "move": "writing move", "heuristic": "named law",
       "bias": "bias", "verdict": "evaluative word"}
CUE = {"fallacy": "name the fallacy", "form": "name it", "move": "name the move", "heuristic": "name the law",
       "bias": "name the bias", "verdict": "name the word"}

rows = list(csv.DictReader(open(src, encoding="utf-8-sig")))
box_w = (CARD_W - 2 * PAD) * mm
box_h = (CARD_H - 2 * PAD - 3.0) * mm      # leave room for the tag line


def wrap(text, font, size, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if pdfmetrics.stringWidth(t, font, size) <= width or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def block(paras, scale):
    """paras: [(text, font, size, gray, gap_before_pt)] -> laid-out lines and total height (pt)."""
    out, h = [], 0.0
    for i, (text, font, size, gray, gap) in enumerate(paras):
        s = size * scale
        if i:
            h += gap * scale
        for ln in wrap(text, font, s, box_w):
            out.append((ln, font, s, gray, h))
            h += s * 1.25
    return out, h


def fit(paras, floor=0.55):
    scale = 1.0
    while True:
        lines, h = block(paras, scale)
        if h <= box_h or scale <= floor:
            return lines, h
        scale -= 0.03


def draw_card(c, x, y, paras, tag=None):
    c.setStrokeGray(0.78); c.setLineWidth(0.2)
    c.rect(x * mm, y * mm, CARD_W * mm, CARD_H * mm)
    lines, h = fit(paras)
    top = y * mm + (CARD_H * mm + h) / 2 + 1.0 * mm   # vertically centred, nudged up off the tag
    for ln, font, s, gray, off in lines:
        c.setFillGray(gray); c.setFont(font, s)
        c.drawCentredString((x + CARD_W / 2) * mm, top - off - s, ln)
    if tag:
        c.setFillGray(0.55); c.setFont("R", TAG_SIZE)
        c.drawRightString((x + CARD_W - 2.0) * mm, (y + 2.0) * mm, tag)
    c.setFillGray(0)


def cell_xy(i):
    col, row = divmod(i, ROWS)                 # column-first, as the MSOD fronts
    return X0 + col * CARD_W, PAGE_H - Y0 - (row + 1) * CARD_H, col, row


def faces(r, kind):
    term = r["term"].strip()
    if kind == "A":
        front = [(term, "I", 15, 0, 0)]
        back = [(r["gloss"].strip(), "R", 10.5, 0, 0)]
        if r["form"].strip():
            back.append((r["form"].strip(), "I", 9, 0.25, 5))
        if r["use"].strip():
            back.append(("when: " + r["use"].strip(), "R", 8, 0.45, 5))
        return front, TAG[r["class"]], back
    return [(r["example"].strip(), "R", 11, 0, 0)], CUE[r["class"]], [(term, "I", 15, 0, 0)]


cards = [(r, "A") for r in rows] + [(r, "B") for r in rows]
c = canvas.Canvas(dst, pagesize=landscape(letter))
c.setTitle("Artful terms: Leitner cards")
per = COLS * ROWS
for p in range(0, len(cards), per):
    sheet = cards[p:p + per]
    for i, (r, k) in enumerate(sheet):           # fronts
        x, y, _, _ = cell_xy(i)
        front, tag, _ = faces(r, k)
        draw_card(c, x, y, front, tag)
    c.showPage()
    for i, (r, k) in enumerate(sheet):           # backs, columns mirrored for short-edge flip
        _, y, col, _ = cell_xy(i)
        x = X0 + (COLS - 1 - col) * CARD_W
        _, _, back = faces(r, k)
        draw_card(c, x, y, back)
    c.showPage()
c.save()
print(f"{len(cards)} cards on {(len(cards) + per - 1) // per} sheets -> {dst}")
