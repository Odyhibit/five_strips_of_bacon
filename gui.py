import customtkinter
from customtkinter import *
from PIL import ImageTk

import bacon
import decode_five_strips_of_bacon

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


# create a bit_mask for the hidden_text
def get_bit_mask(hide_me, dictionary_choice):
    mask = ""
    for char in hide_me:
        if char in dictionary_choice:
            mask += dictionary_choice[char]
    return mask


def process_char(letter: str, secret_bin_str: str) -> str:
    output, this_letter = "", ""
    prefix = ""
    if secret_bin_str[0] == "1":
        prefix += "**"
    if secret_bin_str[1] == "1":
        prefix += "*"
    if secret_bin_str[2] == "1":
        prefix += "~~"
    if secret_bin_str[4] == "1":
        prefix += "__"
    if secret_bin_str[3] == "1":
        this_letter = str(letter).upper()
    else:
        this_letter = str(letter)
    return output + prefix + this_letter + prefix[::-1] + "\u200B"


class MainWindow:

    def __init__(self, root):
        icon_path = ImageTk.PhotoImage(file="bacon-5.png")
        root.wm_iconbitmap()
        root.iconphoto(False, icon_path)
        root.title("Five Strips of Bacon")
        tabcontrol.pack(padx=20, pady=20)
        tabcontrol.add("Encode")
        tabcontrol.add("Decode")

        def convert_hidden(e):
            temp = hidden_text.get("1.0", "end-1c").upper()
            hidden_text.delete("1.0", "end")
            new_text = ""
            for letter in temp:
                if letter.isalpha():
                    new_text += letter
            hidden_text.insert("1.0", new_text)
            check_length(e)

        def check_length(e):
            cover_str = cover_text.get("1.0", "end-1c")
            hidden_str = hidden_text.get("1.0", "end-1c")
            cover = 0
            for letter in cover_str:
                if letter.isalpha():
                    cover += 1
            # print("cover:", cover, "len(hidden):", len(hidden_str))
            if cover >= len(hidden_str):
                calc_button.configure(state="normal")
            else:
                calc_button.configure(state="disabled")

        def calculate_cipher():
            # BISCUT Bold Italic Strikethrough Capital Underline - Text
            secret_bin_str = bacon.get_bit_mask(hidden_text.get("1.0", "end -1c").lower(),
                                                bacon.original_bacon_dictionary)
            cover_text_str = cover_text.get("1.0", "end -1c")
            output, this_letter = "", ""
            i, j = 0, 0
            while i < len(cover_text_str):
                if cover_text_str[i].isalpha() and (j * 5) < len(secret_bin_str):
                    output += bacon.process_char(cover_text_str[i], secret_bin_str[j * 5: j * 5 + 5])
                    j += 1
                else:
                    output += cover_text_str[i]
                i += 1

            cipher_text.delete("1.0", "end")
            cipher_text.insert("1.0", output)

        def decode_cipher():
            covered_text = ciphered_text.get("1.0", "end -1c")
            plain_text = decode_five_strips_of_bacon.decode_cover_text(covered_text)
            plain_text_text.insert("0.0", plain_text)

        def paste_cipher():
            covered_text = root.clipboard_get()
            ciphered_text.insert("0.0", covered_text)

        def copy_to_clipboard():
            field_value = cipher_text.get("1.0", 'end-1c')
            root.clipboard_clear()
            root.clipboard_append(field_value)

        #  ENCODING
        hidden_label = CTkLabel(master=tabcontrol.tab("Encode"), text="Hidden Text - Bacon cipher is alpha only")
        hidden_text = CTkTextbox(master=tabcontrol.tab("Encode"), height=20, width=400)
        cover_label = CTkLabel(master=tabcontrol.tab("Encode"), text="Cover Text - Will not encode punctuation")
        cover_text = CTkTextbox(master=tabcontrol.tab("Encode"), height=20, width=400)
        cipher_label = CTkLabel(master=tabcontrol.tab("Encode"), text="Cipher Text")
        cipher_text = CTkTextbox(master=tabcontrol.tab("Encode"), height=60, width=400)
        calc_button = CTkButton(master=tabcontrol.tab("Encode"), text="Calculate cipher", command=calculate_cipher,
                                state="disabled")
        clip_button = CTkButton(master=tabcontrol.tab("Encode"), text="Copy cipher", command=copy_to_clipboard)

        pad_x = 20
        pad_y = (0, 20)

        hidden_label.grid(column=0, row=1, columnspan=2, padx=pad_x)
        hidden_text.grid(column=0, row=2, columnspan=2, padx=pad_x, pady=pad_y)
        cover_label.grid(column=0, row=3, columnspan=2, padx=pad_x)
        cover_text.grid(column=0, row=4, columnspan=2, padx=pad_x, pady=pad_y)
        cipher_label.grid(column=0, row=5, columnspan=2, padx=pad_x)
        cipher_text.grid(column=0, row=6, columnspan=2, padx=pad_x, pady=pad_y)
        calc_button.grid(column=0, row=7, padx=pad_x, pady=pad_y)
        clip_button.grid(column=1, row=7, padx=pad_x, pady=pad_y)

        hidden_text.bind("<FocusOut>", convert_hidden)
        cover_text.bind("<KeyRelease>", check_length)

        #DECODING
        ciphered_label = CTkLabel(master=tabcontrol.tab("Decode"), text="paste ciphered text")
        ciphered_text = CTkTextbox(master=tabcontrol.tab("Decode"), height=60, width=400)
        plain_text_label = CTkLabel(master=tabcontrol.tab("Decode"), text="recovered message")
        plain_text_text = CTkTextbox(master=tabcontrol.tab("Decode"), height=20, width=400)
        decode_button = CTkButton(master=tabcontrol.tab("Decode"), text="Decode cipher", command=decode_cipher)
        paste_button = CTkButton(master=tabcontrol.tab("Decode"), text="Paste", command=paste_cipher)

        ciphered_label.grid(column=0, row=0, columnspan=2, padx=pad_x, pady=pad_y)
        ciphered_text.grid(column=0, row=1, columnspan=2, padx=pad_x, pady=pad_y)
        plain_text_label.grid(column=0, row=2, columnspan=2, padx=pad_x, pady=pad_y)
        plain_text_text.grid(column=0, row=3, columnspan=2, padx=pad_x, pady=pad_y)

        decode_button.grid(column=0, row=4, padx=pad_x, pady=pad_y)
        paste_button.grid(column=1, row=4, padx=pad_x, pady=pad_y)


if __name__ == '__main__':
    root = CTk()
    tabcontrol = customtkinter.CTkTabview(root)
    tabcontrol.pack(expand=True)
    # icon_bacon = PhotoImage(file="bacon-5.png")
    # root.iconphoto(False, icon_bacon)
    MainWindow(root)
    root.mainloop()
