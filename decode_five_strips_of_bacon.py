from tkinter import Tk

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


def grab_clipboard() -> []:
    a = Tk()
    cb = a.clipboard_get()
    a.destroy()
    return cb


def process_char(letter: str) -> str:
    output = [0, 0, 0, 0, 0]
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
    if "__" in prefix:
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


def decode_cover_text(cover_text: str) -> str:
    if "\u200b" in cover_text:
        clipboard = cover_text.split("\u200B")
    else:
        clipboard = cover_text.split()

    output = ""
    for letter in clipboard:
        secret_letter = process_char(letter)
        output += secret_letter
    return output



def main():
    cover_text = grab_clipboard()
    print(decode_cover_text(cover_text))


if __name__ == "__main__":
    main()
