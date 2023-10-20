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
markdown_prefix = ["**", "*", "~~", "", "<ins>"]
markdown_suffix = ["**", "*", "~~", "", "</ins>"]


# create a bit_mask for the hidden_text
def get_bit_mask(hide_me: str, dictionary_choice: {}) -> str:
    mask = ""
    for char in hide_me:
        if char in dictionary_choice:
            mask += dictionary_choice[char]
    return mask


def add_bacon(letter: str, bit_mask: str, output_format: str) -> str:
    zero_width_space = "\u200B"
    prefix, suffix = "", ""
    prefix_list, suffix_list = [], []
    if output_format == "Discord":
        prefix_list = discord_prefix
        suffix_list = discord_suffix
    if output_format == "Markdown":
        prefix_list = markdown_prefix
        suffix_list = markdown_suffix
    for i in range(5):
        if bit_mask[i] == "1":
            prefix = prefix + prefix_list[i]
            suffix = suffix_list[i] + suffix
    if bit_mask[3] == "1":
        this_letter = str(letter).upper()
    else:
        this_letter = str(letter)
    return prefix + this_letter + prefix[::-1] + zero_width_space

