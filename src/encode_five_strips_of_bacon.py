"""Module for encoding 5 bacon ciphers in markdown"""
original_bacon_dictionary = {"a": "00000",
                             "b": "00001",
                             "c": "00010",
                             "d": "00011",
                             "e": "00100",
                             "f": "00101",
                             "g": "00110",
                             "h": "00111",
                             "i": "01000",
                             "j": "01000",
                             "k": "01001",
                             "l": "01010",
                             "m": "01011",
                             "n": "01100",
                             "o": "01101",
                             "p": "01110",
                             "q": "01111",
                             "r": "10000",
                             "s": "10001",
                             "t": "10010",
                             "u": "10011",
                             "v": "10011",
                             "w": "10100",
                             "x": "10101",
                             "y": "10110",
                             "z": "10111"}

discord_prefix = ["**", "*", "~~", "", "__"]
discord_suffix = ["**", "*", "~~", "", "__"]
github_prefix = ["**", "*", "~~", "", "<ins>"]
github_suffix = ["**", "*", "~~", "", "</ins>"]


# create a bit_mask for the hidden_text
def get_bit_mask(hide_me: str, dictionary_choice: {}) -> str:
    """
    :param hide_me: this is the original plaintext
    :param dictionary_choice: this provides a way to use alternative encodings, currently
    only the original_bacon_dictionary is provided.
    :return: binary string from the original_bacon_dictionary concatenated together
    """
    mask = ""
    for char in hide_me:
        if char in dictionary_choice:
            mask += dictionary_choice[char]
    return mask


def add_bacon(letter: str, bit_mask: str, output_format: str) -> str:
    # pylint: disable=too-many-branches
    """Add appropriate markdown prefix, and suffix
    :param letter: one character of the covertext
    :param bit_mask: the binary string representing one hidden character
    :param output_format: which set of prefix/suffix to use
    :return: string  prefix + cover character + suffix + zero width character
    bold_cap_offset = 119743
    bold_small_offset = 119769
    italic_cap_offset = 119795
    italic_small_offset = 119821
    """
    zero_width_space = "\u200B"
    this_letter = letter
    prefix, suffix = "", ""
    prefix_list, suffix_list = [], []
    letter = letter.upper()
    letter_offset = ord(letter) - 65

    if output_format == "Unicode" and letter.isalpha():
        if bit_mask[0] == "1" and bit_mask[3] == "1":  # Bold and Capital
            this_letter = chr(0x1d400 + letter_offset)
        if bit_mask[0] == "1" and not bit_mask[3] == "1":  # Bold and small
            this_letter = chr(0x1d41a + letter_offset)
        if bit_mask[1] == "1" and bit_mask[3] == "1":  # Italic and Capital
            this_letter = chr(0x1D434 + letter_offset)
        if bit_mask[1] == "1" and not bit_mask[3] == "1":  # Italic and small
            this_letter = chr(0x1d44e + letter_offset)
            if letter_offset == 7:
                this_letter = chr(0x210e)  # glyph is reserved, so use plank's constant
        if bit_mask[0:2] == "00" and bit_mask[3] == "1":  # just capital
            this_letter = letter.upper()
        if bit_mask[2] == "1":  # Underline
            this_letter += "\u0336"
        if bit_mask[4] == "1":  # strikethrough
            this_letter += "\u0332"

    else:
        if output_format == "Discord":
            prefix_list = ["**", "*", "~~", "", "__"]
            suffix_list = ["**", "*", "~~", "", "__"]
        if output_format == "GitHub":
            prefix_list = ["**", "*", "~~", "", "<ins>"]
            suffix_list = ["**", "*", "~~", "", "</ins>"]
        for i in range(5):
            if bit_mask[i] == "1":
                prefix = prefix + prefix_list[i]
                suffix = suffix_list[i] + suffix
        if bit_mask[3] == "1":
            this_letter = str(letter).upper()
        else:
            this_letter = str(letter).lower()
    return prefix + this_letter + suffix + zero_width_space


def encode_cover_text(hidden_str: str, cover_text_str: str, output_format: str) -> str:
    """This function does the heavy lifting for the encoding.
               BISCUT Bold Italic Strikethrough Capital Underline - Text

               :return: cover text with modifiers
               """

    word_joiner = "\u2060"
    no_break_space = "\ufeff"
    secret_bin_str = get_bit_mask(hidden_str.lower(), original_bacon_dictionary)
    output = ""
    cover_index, hidden_index, bin_str_index = 0, 0, 0
    need_to_end_code = True

    while cover_index < len(cover_text_str):
        if hidden_index < len(hidden_str):
            if cover_text_str[cover_index].isalpha():
                if hidden_str[hidden_index] == " ":
                    output += word_joiner
                    hidden_index += 1
                else:
                    output += add_bacon(cover_text_str[cover_index],
                                        secret_bin_str[bin_str_index * 5: bin_str_index * 5 + 5],
                                        output_format)
                    hidden_index += 1
                    bin_str_index += 1
                    cover_index += 1
            elif cover_text_str[cover_index] == " ":
                output += " "
                cover_index += 1
        else:
            if need_to_end_code:
                output += no_break_space
                need_to_end_code = False
            output += cover_text_str[cover_index]
            cover_index += 1

    return output
