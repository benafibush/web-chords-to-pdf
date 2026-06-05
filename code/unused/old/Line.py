import re


class Line:

    _text = None
    _type = None
    _len = None
    _page_width_in_chars = None
    _language = None

    def __init__(self, text, page_width_in_chars, _type=None):
        self._text = text
        self._type = _type
        self._len = len(text)
        self.determine_language()
        self._page_width_in_chars = page_width_in_chars

    def get_text(self):
        return self._text

    def is_empty(self):
        return self._type == 'MT'

    def is_lyrics(self):
        return self._type == 'LY'

    def is_chords(self):
        return self._type == 'CH'

    def is_heading(self):
        return self._type == 'HD'

    def get_len(self):
        return self._len

    def get_last_idx(self):
        return self._len - 1

    def is_too_long(self):
        return self._page_width_in_chars < self._len

    def split_to_wrapped_lines(self):

        def split_to_words_incl_pre_whitespaces(text):

            split_list = []
            current_string = ''
            inside_a_word = False

            for char in text:
                if inside_a_word:
                    if char.isspace():
                        split_list.append(current_string)
                        current_string = char
                        inside_a_word = False
                    else:
                        current_string += char
                else:
                    current_string += char
                    if not char.isspace():
                        inside_a_word = True
            if inside_a_word:
                split_list.append(current_string)
            return split_list

        words = split_to_words_incl_pre_whitespaces(self._text)
        wrapped_lines = []  # Initialize the lines list
        current_line_text = ""  # Initialize the current line string
        for word in words:
            if len(current_line_text + word) <= self._page_width_in_chars:
                current_line_text += word
            else:
                if len(word) < self._page_width_in_chars:
                    wrapped_lines.append(
                        Line(current_line_text,
                             self._page_width_in_chars,
                             self._type))
                    current_line_text = word
                else:
                    for i in range(0, len(word), self._page_width_in_chars):
                        wrapped_lines.append(
                            Line(word[i:i + self._page_width_in_chars],
                                 self._page_width_in_chars,
                                 self._type))
        # Add the final line to the lines list
        wrapped_lines.append(Line(current_line_text, self._page_width_in_chars, self._type))
        return wrapped_lines

    def wrap_within_reference(self, reference_lines):

        def get_end_char_index():
            index = start_char_index + reference_line.get_last_idx()
            if self.get_last_idx() < index:
                index = self.get_last_idx()
            if index + 1 < self.get_last_idx():
                # If it's the middle of a word
                if not self._text[index].isspace() and not self._text[index + 1].isspace():
                    # Go back to word start
                    while not self._text[index].isspace() and start_char_index < index:
                        index -= 1
            return index

        result = reference_lines.copy()
        start_char_index = 0
        for ref_line_index, reference_line in enumerate(reference_lines):
            end_char_index = get_end_char_index()
            wrapped_line = Line(self._text[start_char_index:end_char_index + 1],
                                self._page_width_in_chars,
                                self._type)
            result.insert(ref_line_index*2, wrapped_line)
            start_char_index = end_char_index + 1
            if self.get_last_idx() < start_char_index:
                break
        # Add what's left, if any
        if start_char_index < self.get_last_idx():
            wrapped_line = Line(self._text[start_char_index:], self._page_width_in_chars, self._type)
            result.append(wrapped_line)
        return result

    def determine_language(self):
        hebrew_pattern = r"[א-ת]"
        if re.search(hebrew_pattern, self._text):
            self._language = 'HE'
        else:
            self._language = 'EN'

    def get_language(self):
        return self._language

    def classify_if_empty(self):
        empty_pattern = r"^\s*$"
        if re.match(empty_pattern, self._text):
            self._type = 'MT'

    def classify_if_heading(self):
        heading_pattern = r"^\W*\[.*\]\W*$"
        if re.match(heading_pattern, self._text):
            self._type = 'HD'

    def classify_if_lyrics(self):
        word_pattern = r"([a-zA-Zא-ת\'\,\.\"\(\)\-\:]{2,}|I)"
        lyrics_pattern = r"\W*" + word_pattern + r"\W+" + word_pattern + r"\W+" + word_pattern + r"\W*"
        if re.match(lyrics_pattern, self._text):
            self._type = 'LY'

    def classify_if_chords(self, next_line):
        chord_pattern = r"^[abdgijmsuA-G245679+#/ ]+$"
        if re.match(chord_pattern, self._text):
            if next_line.is_lyrics():
                self._type = 'CH'
