from BrowsingManager import BrowsingManager
from Song import Song


class Songbook:

    _songs: [Song]

    _file_name = None  # FIXME: songbook should not hold the destination file name. That is the PDF writer's job
    _domain = None
    _urls_file_path = None
    _webpages = []
    _max_line_len = None

    def __init__(self):
        self._songs = []

    def __len__(self) -> int:
        return len(self._songs)

    def add_song(self, artist, title, text) -> None:
        # new_song = Song(artist, title, text)
        # self._songs.append(new_song)
        pass

    def old__init__(self, urls_file_path, max_line_len, domain):
        self._web_manager = BrowsingManager(domain, max_line_len)
        self._file_name = urls_file_path.split('/')[-1].split('.')[0]
        self._domain = domain
        self._urls_file_path = urls_file_path
        self._max_line_len = max_line_len
        self.parse_urls()  # FIXME: This function does more than one thing
        self.sort()

    def parse_urls(self):
        with open(self._urls_file_path) as f:
            urls = f.readlines()
            # Remove whitespace characters like `\n` at the end of each line
            urls = [url.strip() for url in urls]
        self._webpages = []
        self._webpages = self._web_manager.load_pages_parallely(urls)

    def sort(self):
        self._webpages.sort(key=lambda site: (site.get_title()))

    def get_webpages(self):
        return self._webpages

    def get_language(self):
        if self._domain == 'UG':
            return 'EN'
        if self._domain == 'TAB4U':
            return 'HE'

    def get_setlist(self):
        setlist = []
        for webpage in self._webpages:
            setlist.append(webpage.get_title())
        return setlist

    def get_file_name(self):
        return self._file_name


def test():
    urls_file_path = '../../input_urls/UG-test.txt'
    songbook = Songbook(urls_file_path, 150, 'UG')
    print (songbook._webpages[0]._song_name)
    songbook.sort()
    print (songbook._webpages[0]._song_name)


if __name__ == '__main__':
    test()
