import os
from typing import Optional
from io import BytesIO

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class PDFWriter:
    def __init__(
        self,
        font_name: str = "Courier-New-Bold",
        font_size: int = 8,
        left_margin: int = 10,
        top_margin: int = 25,
        right_margin: int = 10,
        bottom_margin: int = 25,
        line_leading: float = 1.4,
        page_width: float = 13.6 * 72 / 2.54
    ):
        self.font_name = font_name
        self.font_size = font_size
        self.left_margin = left_margin
        self.top_margin = top_margin
        self.right_margin = right_margin
        self.bottom_margin = bottom_margin
        self.line_leading = line_leading
        self.page_width = page_width

        if self.font_name not in pdfmetrics.getRegisteredFontNames():
            try:
                pdfmetrics.registerFont(TTFont(self.font_name, f"{self.font_name}.ttf"))
            except Exception:
                pdfmetrics.registerFont(TTFont("Courier-New-Bold", f"courbd.ttf"))

        self.init_canvas()

    def init_canvas(self):
        self.packet = BytesIO()
        self.canvas = canvas.Canvas(self.packet)
        self.canvas.setFont(self.font_name, self.font_size)

    def generate_pdf(self, df: pd.DataFrame) -> None:
        self.create_table_of_contents(df)
        for index, row in df.iterrows():
            self.create_song_page(row)
        self.canvas.save()

    def create_table_of_contents(self, df: pd.DataFrame) -> None:
        self.canvas.setFont(self.font_name, self.font_size)
        text:str = self.prepare_text_for_table_of_contents(df)
        self.set_page_size_table_of_contents(text)
        if df.iloc[0].get("Language", "").strip() == "Hebrew":
            self.print_table_of_contents_RTL(text)
        else:
            self.print_table_of_contents_LTR(text)

    def create_song_page(self, row: pd.Series) -> None:
        self.canvas.setFont(self.font_name, self.font_size)
        text:str = self.prepare_text_for_song(row)
        self.set_page_size_song(text)
        if row.get("Language", "").strip() == "Hebrew":
            self.print_song_header_RTL(row)
            self.print_song_text_RTL(text)
        else:
            self.print_song_header_LTR(row)
            self.print_song_text_LTR(text)

    def prepare_text_for_table_of_contents(self, df: pd.DataFrame) -> str:
        text = ""
        for index, row in df.iterrows():
            title = str(row.get("Title", ""))
            artist = str(row.get("Artist", ""))
            text += f"{artist} - {title}\n"
        text = "\n".join(sorted(text.splitlines()))
        text = "\n".join([f"{i+1}. {line}" for i, line in enumerate(text.splitlines())])
        return text
    
    def prepare_text_for_song(self, row: pd.Series) -> str:
        text = str(row.get("Text", ""))
        return text
    
    def set_page_size_table_of_contents(self, text: str) -> None:
        num_of_lines = len(text.splitlines())
        self.page_height = self.top_margin + self.bottom_margin + num_of_lines * self.font_size * self.line_leading
        self.canvas.setPageSize((self.page_width, self.page_height))

    def set_page_size_song(self, text: str) -> None:
        num_of_lines = len(text.splitlines()) + 3
        self.page_height = self.top_margin + self.bottom_margin + num_of_lines * self.font_size * self.line_leading
        self.canvas.setPageSize((self.page_width, self.page_height))

    def print_table_of_contents_LTR(self, text: str) -> None:
        current_y = self.page_height - self.top_margin
        line_height = self.font_size * self.line_leading

        for line in text.splitlines():
            self.canvas.drawString(self.left_margin, current_y, line)
            current_y -= line_height

        self.canvas.showPage()

    def print_table_of_contents_RTL(self, text: str) -> None:
        current_y = self.page_height - self.top_margin
        line_height = self.font_size * self.line_leading

        for line in text.splitlines():
            text_width = self.canvas.stringWidth(line, self.font_name, self.font_size)
            x_position = self.page_width - self.right_margin - text_width
            self.canvas.drawString(x_position, current_y, line[::-1])
            current_y -= line_height

        self.canvas.showPage()

    def print_song_header_LTR(self, row: pd.Series) -> None:
        line1 = f"{row.get('Artist', '')} - {row.get('Title', '')}"
        line2 = f"Capo: {row.get('Capo Transpose', '')} | Sing: {row.get('Singing Style', '')} | Strum: {row.get('Strumming Style', '')}"
        line3 = f"Genre: {row.get('Genre', '')} | Order: {row.get('Order', '')}"
        y_position = self.page_height - self.top_margin
        for line in [line1, line2, line3]:
            text_width = self.canvas.stringWidth(line, self.font_name, self.font_size)
            x_position = (self.page_width - text_width) / 2
            self.canvas.drawString(x_position, y_position, line)
            y_position -= self.font_size * self.line_leading

    def print_song_header_RTL(self, row: pd.Series) -> None:
        line1 = f"{row.get('Artist', '')} - {row.get('Title', '')}"
        line2 = f"Capo: {row.get('Capo Transpose', '')} | Sing: {row.get('Singing Style', '')} | Strum: {row.get('Strumming Style', '')}"
        line3 = f"Genre: {row.get('Genre', '')} | Order: {row.get('Order', '')}"
        y_position = self.page_height - self.top_margin
        for line in [line1[::-1], line2, line3]:
            text_width = self.canvas.stringWidth(line, self.font_name, self.font_size)
            x_position = (self.page_width - text_width) / 2
            self.canvas.drawString(x_position, y_position, line)
            y_position -= self.font_size * self.line_leading

    def print_song_text_LTR(self, text: str) -> None:
        line_height = self.font_size * self.line_leading
        current_y = self.page_height - self.top_margin - 3 * line_height

        for line in text.splitlines():
            self.canvas.drawString(self.left_margin, current_y, line)
            current_y -= line_height

    def print_song_text_RTL(self, text: str) -> None:
        line_height = self.font_size * self.line_leading
        current_y = self.page_height - self.top_margin - 3 * line_height

        for line in text.splitlines():
            if any('א' <= char <= 'ת' for char in line):
                line = line[::-1]
                line = line.replace('(', '^').replace(')', '(').replace('^', ')')
                line = line.replace('[', '^').replace(']', '[').replace('^', ']')
            text_width = self.canvas.stringWidth(line, self.font_name, self.font_size)
            x_position = self.page_width - self.right_margin - text_width
            self.canvas.drawString(x_position, current_y, line)
            current_y -= line_height

    def save_pdf(self, dir: str, filename: str = "songbook.pdf") -> None:
        pdf_path = os.path.join(dir, filename)
        if os.path.exists(pdf_path):
            raise FileExistsError(f"File {pdf_path} already exists.")
        with open(pdf_path, "wb") as f:
            f.write(self.packet.getvalue())