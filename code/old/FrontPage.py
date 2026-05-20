from reportlab.pdfgen import canvas
from io import BytesIO
from pdfrw import PdfReader


class FrontPage (canvas.Canvas):

    _packet = None
    _cfg = None
    _setlist = None
    _pdf = None

    def __init__(self, songbook, pdf_cfg):
        self._packet = BytesIO()
        self._cfg = pdf_cfg
        super().__init__(self._packet, pagesize=(self._cfg.page_width_cm, self._cfg.page_height_px))
        self._setlist = songbook.get_setlist()
        self._file_name = songbook.get_file_name()
        self._language = songbook.get_language()
        self.generate_page()

    def generate_page(self):

        def convert_to_pdf():
            self.save()
            self._packet.seek(0)
            self._pdf = PdfReader(self._packet)

        def write_setlist():
            x = self._cfg.left_margin_px
            y = self._cfg.page_height_px - self._cfg.top_margin_px - self._leading * 2
            if self._language == 'EN':
                for num, title in enumerate(self._setlist):
                    line = str(num+1) + '.' + ' '*(3-len(str(num+1))) + title
                    self.drawString(x, y, line)
                    y -= self._leading
            if self._language == 'HE':
                for num, title in enumerate(self._setlist):
                    line = title[::-1] + ' '*(3-len(str(num+1))) + '.' + str(num+1)
                    self.drawRightString(self._cfg.page_width_px-x, y, line)
                    y -= self._leading

        def write_file_title():
            x_for_center = max(0, (self._cfg.page_width_px - len(self._file_name) * self._cfg.char_to_px) / 2)
            y = self._cfg.page_height_px - self._cfg.top_margin_px - self._leading
            self.drawString(x_for_center, y, self._file_name)

        def format_page():
            num_of_rows = len(self._setlist)
            self._cfg.page_height_px = (num_of_rows + 2) * self._cfg.font_size * 1.2 + self._cfg.top_margin_px
            self.setPageSize((self._cfg.page_width_px, self._cfg.page_height_px))
            self.setFont(self._cfg.font, self._cfg.font_size)

        format_page()
        write_file_title()
        write_setlist()
        convert_to_pdf()



    def get_page(self):
        return self._pdf.pages[0]

