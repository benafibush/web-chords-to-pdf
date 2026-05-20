import re
from Line import Line


class Song:

    _lines = None
    _page_width_in_chars = None

    def __init__(self, lines, page_width_in_chars):
        self._page_width_in_chars = page_width_in_chars
        self.populate_lines(lines, page_width_in_chars)
        self.classify_line_types()
        self.wrap_lines()

    def get_len(self):
        return len(self._lines)

    def get_lines(self):
        return self._lines

    def populate_lines(self, lines, page_width_in_chars):
        self._lines = []
        lines = lines.split('\n')
        for line in lines:
            self._lines.append(Line(line, page_width_in_chars))

    def classify_line_types(self):
        for line in self._lines:
            line.classify_if_empty()
        for line in self._lines:
            line.classify_if_heading()
        for line in self._lines:
            line.classify_if_lyrics()
        for i in range(len(self._lines) - 1):
            line = self._lines[i]
            next_line = self._lines[i + 1]
            line.classify_if_chords(next_line)

    def wrap_lines(self):

        # Cases:
        # Long line, no type - no wrapping
        # Long lyrics with short chords or no chords - wrap only lyrics
        # Long lyrics with long chords - wrap them together
        # Long chords with no lyrics - wrap only chords
        # Long chords with short lyrics - wrap them together

        new_lines = []
        skip_line = False

        for line_idx, line in enumerate(self._lines):

            if skip_line:
                skip_line = False
                continue

            if 0 < line_idx:
                prev_line = self._lines[line_idx - 1]
            else:
                prev_line = None
            if line_idx+1 < len(self._lines):
                next_line = self._lines[line_idx + 1]
            else:
                next_line = None

            line_replacement = [line]

            if line.is_chords() and line.is_too_long():
                if next_line is not None:
                    if next_line.is_lyrics():
                        if next_line.is_too_long():
                            continue
                        else:
                            line_replacement = line.wrap_within_reference([next_line])
                            skip_line = True
                    else:
                        line_replacement = line.split_to_wrapped_lines()
                else:
                    line_replacement = line.split_to_wrapped_lines()

            if line.is_lyrics() and line.is_too_long():
                if prev_line is not None:
                    if prev_line.is_chords():
                        if prev_line.is_too_long():
                            line_replacement = prev_line.wrap_within_reference(line.split_to_wrapped_lines())
                        else:
                            line_replacement = line.split_to_wrapped_lines()
                    else:
                        line_replacement = line.split_to_wrapped_lines()
                else:
                    line_replacement = line.split_to_wrapped_lines()

            new_lines += line_replacement

        self._lines = new_lines


def test():
    text = ("\nIt doesn't matter if you love him, or capital H-I-M \n" +
            "Bm\nJust put your paws up \n" +
            "Bm\n'Cause you were Born This Way, baby \n \n" +
            "E5    D5     A5    E5 \n \n \n[Verse] \n \n" +
            "E                     D \n" +
            "My mama told me when I was young \n" +
            "A          Asus           Amaj7     Bm \n" +
            "We are all born superstars \n" +
            "E                              D \n" +
            "She rolled my hair and put my lipstick on \n" +
            "A               Asus2           Amaj7     Bm7 \n" +
            "In the glass of her boudoir \n \n" +
            "E                                   D \n" +
            "There's nothin' wrong with lovin' who you are \n" +
            "A                              A5 \n" +
            "She said, Cause he made you perfect, babe \n" +
            "E                                       D \n" +
            "So hold your head up, girl and you you'll go far,\n" +
            "A                    A5 \n" +
            "listen to me when I say \n \n \n[Pre-Chorus]"
            )
    text = ("                    Am         G           F       G      Esus4                 E     F \n" +
            "All the leaves are brown                  and the sky is gray \n" +
            "( All the leaves are brown )             (and the skies are grey ey )")
    song_lines = Song(text, 50)
    for song_line in song_lines._lines:
        print(song_line.get_text())


# test()
