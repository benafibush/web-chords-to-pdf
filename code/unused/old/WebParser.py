from code.unused.old.WebPage import WebPage
from code.unused.old.Songbook import Songbook


class WebParser:

    def make_songbook(self, web_pages: [WebPage]) -> Songbook:
        songbook = Songbook()
        artist, title, text = parse_webpage
        for webpage in web_pages:
            songbook.add_song(artist, title, text)
        return songbook
