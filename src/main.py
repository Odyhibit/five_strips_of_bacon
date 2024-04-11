from customtkinter import *
from PIL import ImageTk

import src.bacon as bacon
import src.decode_five_strips_of_bacon as decode_bacon


class MainWindow:

    def __init__(self, root):

        tabcontrol = CTkTabview(root)
        tabcontrol.pack(expand=True)
        icon_path = ImageTk.PhotoImage(file="five-strips-of-bacon/src/resources/bacon_five.png")
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
                if letter == " ":
                    new_text += " "
            new_text = new_text.replace("J", "I")
            new_text = new_text.replace("V", "U")
            hidden_text.insert("1.0", new_text)
            check_length(e)

        def check_length(e):
            cover_str = cover_text.get("1.0", "end-1c")
            hidden_str = hidden_text.get("1.0", "end-1c").replace(" ", "")
            cover = 0
            for letter in cover_str:
                if letter.isalpha():
                    cover += 1
            # print("cover:", cover, "len(hidden):", len(hidden_str))
            if cover >= len(hidden_str):
                calc_button.configure(state="normal", text="Calculate cipher")
            else:
                calc_button.configure(state="disabled", text="Need more cover text")

        def calculate_cipher():
            # BISCUT Bold Italic Strikethrough Capital Underline - Text
            word_joiner = "\u2060"
            no_break_space = "\ufeff"
            hidden_str = hidden_text.get("1.0", "end-1c")
            secret_bin_str = bacon.get_bit_mask(hidden_text.get("1.0", "end -1c").lower(),
                                                bacon.original_bacon_dictionary)
            cover_text_str = cover_text.get("1.0", "end -1c")
            output_format = output_type.get()
            output, this_letter = "", ""
            cover_index, hidden_index, bin_str_index = 0, 0, 0
            need_to_end_code = True
            while cover_index < len(cover_text_str):
                if hidden_index < len(hidden_str):
                    if cover_text_str[cover_index].isalpha():
                        if hidden_str[hidden_index] == " ":
                            output += word_joiner
                            hidden_index += 1
                            continue
                        else:
                            output += bacon.add_bacon(cover_text_str[cover_index],
                                                      secret_bin_str[bin_str_index * 5: bin_str_index * 5 + 5],
                                                      output_format)
                            hidden_index += 1
                            bin_str_index += 1
                    if cover_text_str[cover_index] == " ":
                        output += " "
                else:
                    if need_to_end_code:
                        output += no_break_space
                        need_to_end_code = False
                    output += cover_text_str[cover_index]
                cover_index += 1

            cipher_text.delete("1.0", "end")
            cipher_text.insert("1.0", output)

        def decode_cipher():
            covered_text = ciphered_text.get("1.0", "end -1c")
            plain_text = decode_bacon.decode_cover_text(covered_text)
            plain_text_text.delete("1.0", "end")
            plain_text_text.insert("1.0", plain_text)

        def paste_cipher():
            covered_text = root.clipboard_get()
            ciphered_text.delete("1.0", "end")
            ciphered_text.insert("1.0", covered_text)

        def copy_to_clipboard():
            field_value = cipher_text.get("1.0", 'end-1c')
            root.clipboard_clear()
            root.clipboard_append(field_value)

        #  ENCODING
        output_type = StringVar(root, "Discord")

        hidden_label = CTkLabel(master=tabcontrol.tab("Encode"),
                                text="Hidden Text - alphabet, and spaces only (I/J and U/V are combined)")
        hidden_text = CTkTextbox(master=tabcontrol.tab("Encode"), height=20, width=400)
        cover_label = CTkLabel(master=tabcontrol.tab("Encode"), text="Cover Text")
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
        CTkRadioButton(tabcontrol.tab("Encode"), text="Discord", variable=output_type, value="Discord").grid(column=0,
                                                                                                             row=8,
                                                                                                             columnspan=2,
                                                                                                             padx=5)
        CTkRadioButton(tabcontrol.tab("Encode"), text="GitHub", variable=output_type, value="GitHub").grid(column=0,
                                                                                                           row=9,
                                                                                                           columnspan=2,
                                                                                                           padx=5)

        hidden_text.bind("<FocusOut>", convert_hidden)
        cover_text.bind("<KeyRelease>", check_length)

        # DECODING
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


def main():
    root = CTk()
    MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
