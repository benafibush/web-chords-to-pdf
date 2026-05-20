import WebPage


class TAB4UWebPage(WebPage.WebPage):
    
    def __init__(self, url, max_line_len, browser):
        
        super().__init__(url, browser)

        self._language = "HE"
        self.set_name_and_artist()
        self.set_song_text()

        self.parse_song(max_line_len)

    def set_song_text(self):

        def cleanup(dirty_line):
            redundant = 'לחץ לתצוגה נוספת'
            clean_line = ''
            for part in dirty_line.split(redundant):
                clean_line += part
            clean_line = clean_line.replace(u'\xa0', u' ')
            return clean_line

        section = self._web_aux.soup.find(id="songContentTPL")
        raw_text = section.get_text()
        raw_lines = raw_text.split('\n')
        self._song_text = ''
        skip_line = False
        for idx, line in enumerate(raw_lines):
            if skip_line:
                skip_line = False
                continue
            if idx+1 < len(raw_lines):
                if line == '' and raw_lines[idx+1] == '':
                    skip_line = True
                    continue
            self._song_text += cleanup(line)+'\n'

    def set_name_and_artist(self):
        section = self._web_aux.soup.find('h1')
        self._artist = section.get_text().split(' - ')[0]
        self._song_name = section.get_text().split(' - ')[1].split('(')[0]

def test():
    url = "https://www.tab4u.com/tabs/songs/2137_%D7%A2%D7%91%D7%A8%D7%99_%D7%9C%D7%99%D7%93%D7%A8_-_%D7%99%D7%95%D7%AA%D7%A8_%D7%98%D7%95%D7%91_%D7%9B%D7%9C%D7%95%D7%9D.html?ton=-0.5"
    tab4u_webpage = TAB4UWebPage(url, 50)
    for line in tab4u_webpage.get_song()._lines:
        print(line.get_text())


# test()
