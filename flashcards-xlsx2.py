from fpdf import FPDF
import os
import pandas as pd


# ============================================================
# USER CONFIGURATION
# ============================================================

EXCEL_PATH = r"C:\Users\arteu\Documents\DRBU\Chinese Flashcards - Liturgy\lexicon.xlsx"

FONT_CHINESE = r"C:\Users\arteu\Documents\Fonts\Chinese\chinesefonts\NotoSerifSC-Regular.ttf"
FONT_PINYIN = r"C:\Windows\Fonts\msyh.ttc"

OUTPUT_DIR = r"C:\Users\arteu\Sandbox\OUTPUTS"

FILTER_INCLUDE = 1 #  1 or "all"
TAG_COLUMN = "eng_tag"    #eng_tag or ch_tag

FILTER_TAGS = (
    "heart_sutra", 
    "incense_praise", 
    "three_refuges", 
    "puxian_exhortation", 
    "merit_transfer"
    )

OUTPUT_FILENAME_A = os.path.join(OUTPUT_DIR, "5_flash_a.pdf")
OUTPUT_FILENAME_B = os.path.join(OUTPUT_DIR, "5_flash_b.pdf")

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ------------------------------------------------------------
# FILTER_TAGS
#
# Controls which liturgy sections are included.
#
# Accepts:
#
#   "all"
#       include every text in spreadsheet
#
#   "香讚"
#       include only that Chinese tag
#
#   ("香讚","心經")
#       include multiple Chinese tags
#
#   ("incense_praise","heart_sutra")
#       if TAG_COLUMN="eng_tag"
#
# ------------------------------------------------------------






# ============================================================
# LOAD DATA
# ============================================================

def load_excel_data():

    df = pd.read_excel(EXCEL_PATH)

    if FILTER_INCLUDE != "all":
        df = df[df["include"] == FILTER_INCLUDE]

    if FILTER_TAGS != "all":

        if isinstance(FILTER_TAGS, str):
            tags = [FILTER_TAGS]
        else:
            tags = list(FILTER_TAGS)

        df = df[df[TAG_COLUMN].isin(tags)]

    raw_data = []

    for _, row in df.iterrows():

        chinese = str(row["chinese"]).strip()
        pinyin = str(row["pinyin"]).strip()
        english = str(row["english_def"]).strip()
        ch_tag = str(row["ch_tag"]).strip()

        multichar = row.get("multichar", False)

        if isinstance(multichar, str):
            multichar = multichar.lower() == "true"

        raw_data.append((chinese, pinyin, english, multichar, ch_tag))

    return raw_data


raw_data = load_excel_data()


# ============================================================
# PDF CLASS
# ============================================================

class FlashcardPDF(FPDF):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_auto_page_break(False)

        self.margin_x = 7.62
        self.margin_y = 7.62

        self.w_card = (279.4 - (2 * self.margin_x)) / 4
        self.h_card = (215.9 - (2 * self.margin_y)) / 4


    def draw_grid_cell(self, x, y):
        self.set_draw_color(200, 200, 200)
        self.rect(x, y, self.w_card, self.h_card)


    def draw_source_tag(self, x, y, tag):

        self.set_text_color(120, 120, 120)

        self.set_font("ChineseChar", size=8)

        self.set_xy(x + self.w_card - 18, y + self.h_card - 6)

        self.cell(16, 4, tag, align="R")

        self.set_text_color(0, 0, 0)


    # ========================================================
    # VERSION A
    # Front: Chinese + Pinyin
    # Back: English
    # ========================================================

    def create_version_A(self):

        for i in range(0, len(raw_data), 16):

            chunk = raw_data[i:i+16]

            # ---------------- FRONT ----------------

            self.add_page()

            for idx, (char, pinyin, eng, is_compound, ch_tag) in enumerate(chunk):

                col = idx % 4
                row = idx // 4

                x = self.margin_x + col * self.w_card
                y = self.margin_y + row * self.h_card

                self.draw_grid_cell(x, y)

                font_size = 28
                if len(char) >= 5:
                    font_size = 20
                elif len(char) >= 3:
                    font_size = 24

                self.set_font("ChineseChar", size=font_size)

                # optical vertical centering
                char_y = y + (self.h_card / 2) - 12
                self.set_xy(x, char_y)

                self.cell(self.w_card, 10, char, align="C")

                style = "B" if is_compound else ""

                self.set_font("ChinesePinyin", style=style, size=14)

                self.set_xy(x, char_y + 16)

                self.cell(self.w_card, 10, pinyin, align="C")


            # ---------------- BACK ----------------

            self.add_page()

            for idx, (char, pinyin, eng, is_compound, ch_tag) in enumerate(chunk):

                col = 3 - (idx % 4)
                row = idx // 4

                x = self.margin_x + col * self.w_card
                y = self.margin_y + row * self.h_card

                self.draw_grid_cell(x, y)

                self.set_font("Helvetica", size=11)

                self.set_xy(x + 2, y + (self.h_card / 2) - 3)

                self.multi_cell(self.w_card - 4, 5, eng, align="C")

                self.draw_source_tag(x, y, ch_tag)


    # ========================================================
    # VERSION B
    # Front: Chinese
    # Back: Pinyin + English
    # ========================================================

    def create_version_B(self):

        for i in range(0, len(raw_data), 16):

            chunk = raw_data[i:i+16]

            # ---------------- FRONT ----------------

            self.add_page()

            for idx, (char, pinyin, eng, is_compound, ch_tag) in enumerate(chunk):

                col = idx % 4
                row = idx // 4

                x = self.margin_x + col * self.w_card
                y = self.margin_y + row * self.h_card

                self.draw_grid_cell(x, y)

                font_size = 32
                if len(char) >= 5:
                    font_size = 22
                elif len(char) >= 3:
                    font_size = 26

                self.set_font("ChineseChar", size=font_size)

                char_y = y + (self.h_card / 2) - 5

                self.set_xy(x, char_y)

                self.cell(self.w_card, 10, char, align="C")


            # ---------------- BACK ----------------

            self.add_page()

            for idx, (char, pinyin, eng, is_compound, ch_tag) in enumerate(chunk):

                col = 3 - (idx % 4)
                row = idx // 4

                x = self.margin_x + col * self.w_card
                y = self.margin_y + row * self.h_card

                self.draw_grid_cell(x, y)

                style = "B" if is_compound else ""

                pinyin_size = 14 if len(pinyin) < 18 else 11

                self.set_font("ChinesePinyin", style=style, size=pinyin_size)

                self.set_xy(x, y + 12)

                self.cell(self.w_card, 10, pinyin, align="C")

                line_y = y + 25
                padding = 10

                self.line(x + padding, line_y, x + self.w_card - padding, line_y)

                self.set_font("Helvetica", size=11)

                self.set_xy(x + 2, line_y + 4)

                self.multi_cell(self.w_card - 4, 5, eng, align="C")

                self.draw_source_tag(x, y, ch_tag)


# ============================================================
# RUN SCRIPT
# ============================================================

pdf_a = FlashcardPDF(orientation="L", unit="mm", format="Letter")

pdf_a.add_font("ChineseChar", fname=FONT_CHINESE)
pdf_a.add_font("ChineseChar", style="B", fname=FONT_CHINESE)

pdf_a.add_font("ChinesePinyin", fname=FONT_PINYIN)
pdf_a.add_font("ChinesePinyin", style="B", fname=FONT_PINYIN)

pdf_a.create_version_A()
pdf_a.output(OUTPUT_FILENAME_A)

print("Generated:", OUTPUT_FILENAME_A)


pdf_b = FlashcardPDF(orientation="L", unit="mm", format="Letter")

pdf_b.add_font("ChineseChar", fname=FONT_CHINESE)
pdf_b.add_font("ChineseChar", style="B", fname=FONT_CHINESE)

pdf_b.add_font("ChinesePinyin", fname=FONT_PINYIN)
pdf_b.add_font("ChinesePinyin", style="B", fname=FONT_PINYIN)

pdf_b.create_version_B()
pdf_b.output(OUTPUT_FILENAME_B)

print("Generated:", OUTPUT_FILENAME_B)