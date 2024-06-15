"""Code used to decode the custom 5 item bacon ciphers."""
from tkinter import Tk


def grab_clipboard() -> []:
    """Returns the contents of the clipboard"""
    a = Tk()
    cb = a.clipboard_get()
    a.destroy()
    return cb


def process_char(letter: str) -> str:
    """decodes the attributes of one letter, and returns a hidden character
    
    letter - string containing modifier characters, and the cover character
    returns - string that is one decoded character
    """
    output = [0, 0, 0, 0, 0]
    letter = letter.replace("/", "")
    prefix_size = len(letter) // 2
    prefix = letter[:prefix_size]
    cover_character = letter[prefix_size:prefix_size + 1]
    if "***" in prefix:
        output[0] = 1
        output[1] = 1
    elif "**" in prefix:
        output[0] = 1
    elif "*" in prefix:
        output[1] = 1
    if "~~" in prefix:
        output[2] = 1
    if "__" in prefix or "<ins>" in prefix:
        output[4] = 1
    if cover_character.isupper():
        output[3] = 1
    binary_string = "".join(map(str, output))
    if binary_string in reverse_bacon_dictionary:
        return_letter = reverse_bacon_dictionary[binary_string]
    else:
        return f"{binary_string} is not a valid bacon encoding."
    if not cover_character.isalpha():
        return_letter = " "
    return return_letter


def process_word(cover_text: str) -> str:
    """Split cover text on zero-width space. use process_letter() to decode each
    letter, and it's markdown characters.
    
    :param cover_text: string containing cover text, and markdown characters
    :return: string of text hidden in markdown from covertext
    """
    output = ""
    if "\u200b" in cover_text:
        letter_markdown_list = cover_text.split("\u200B")
    else:
        letter_markdown_list = cover_text.split()

    for letter_markdown in letter_markdown_list:
        secret_letter = process_char(letter_markdown)
        output += secret_letter
    return output


def decode_cover_text(cover_text: str) -> str:
    """word_joiner is used to encode spaces in the original plain text.
    no_break_space is used to mark the end of the encoding.

    :param cover_text:
    :return: the original plaintext where i,j=i  u,v=u due to the bacon cipher limitations
    """
    word_joiner = "\u2060"
    no_break_space = "\ufeff"
    output = ""

    if no_break_space in cover_text:
        cover_text = cover_text[:cover_text.find(no_break_space)]
    word_list = cover_text.split(word_joiner)

    for word in word_list:
        output += process_word(word) + " "

    return output.upper()


def main():
    """Get the contents of the clipboard, and decode it.

    :return: the original plaintext where i,j=i  u,v=u due to the bacon cipher limitations
    """
    cover_text = grab_clipboard()
    print(decode_cover_text(cover_text))


if __name__ == "__main__":
    reverse_bacon_dictionary = {"00000": "a",
                                "00001": "b",
                                "00010": "c",
                                "00011": "d",
                                "00100": "e",
                                "00101": "f",
                                "00110": "g",
                                "00111": "h",
                                "01000": "i",
                                "01001": "k",
                                "01010": "l",
                                "01011": "m",
                                "01100": "n",
                                "01101": "o",
                                "01110": "p",
                                "01111": "q",
                                "10000": "r",
                                "10001": "s",
                                "10010": "t",
                                "10011": "u",
                                "10100": "w",
                                "10101": "x",
                                "10110": "y",
                                "10111": "z"}
    main()
