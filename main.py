from tkinter import *
from tkinter import ttk
import bacon


class MainWindow:

    def __init__(self, root):
        root.title("Five Strips of Bacon")
        content = ttk.Frame(root)

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
            #print("cover:", cover, "len(hidden):", len(hidden_str))
            if cover >= len(hidden_str):
                calc_button.config(state="normal")
            else:
                calc_button.config(state="disabled")


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
            binary_version = ""
            for i, character in enumerate(secret_bin_str):
                binary_version += character
                if (i+1) % 5 == 0:
                    binary_version += " "

            bin_text.delete("1.0", "end")
            bin_text.insert("1.0", binary_version)

            cipher_text.delete("1.0", "end")
            cipher_text.insert("1.0", output)


        def copy_to_clipboard():
            field_value = cipher_text.get("1.0", 'end-1c')
            content.clipboard_clear()
            content.clipboard_append(field_value)


        discord_var = IntVar()

        hidden_label = ttk.Label(content, text="Hidden Text - Bacon cipher is alpha only")
        hidden_text = Text(content, height=3)
        cover_label = ttk.Label(content, text="Cover Text - Will not encode punctuation")
        cover_text = Text(content, height=3)
        cipher_label = ttk.Label(content, text="Cipher Text")
        cipher_text = Text(content, height=6)
        bin_label = ttk.Label(content, text="Bitmask- Bold,Italic,Strikethrough,Capital,Underline")
        bin_text = Text(content, height=6)
        calc_button = Button(content, text="Calculate cipher", command=calculate_cipher, state="disabled")
        clip_button = Button(content, text="Copy cipher", command=copy_to_clipboard)
        discord_checkbox = ttk.Checkbutton(content, text="Discord format", state="normal", variable=discord_var)

        pad_x = 10
        pad_y = 5

        content.grid(column=0, row=0, padx=pad_x, pady=pad_y)
        hidden_label.grid(column=0, row=0, columnspan=2, padx=pad_x, pady=pad_y)
        hidden_text.grid(column=0, row=1, columnspan=2, padx=pad_x, pady=pad_y)
        cover_label.grid(column=0, row=2, columnspan=2, padx=pad_x, pady=pad_y)
        cover_text.grid(column=0, row=3, columnspan=2, padx=pad_x, pady=pad_y)
        cipher_label.grid(column=0, row=4, columnspan=2, padx=pad_x, pady=pad_y)
        cipher_text.grid(column=0, row=5, columnspan=2, padx=pad_x, pady=pad_y)
        bin_label.grid(column=0, row=6, columnspan=2, padx=pad_x, pady=pad_y)
        bin_text.grid(column=0, row=7, columnspan=2, padx=pad_x, pady=pad_y)
        calc_button.grid(column=0, row=8, padx=pad_x, pady=pad_y, sticky="E")
        clip_button.grid(column=0, row=8, padx=pad_x, pady=pad_y, sticky="W")
        discord_checkbox.grid(column=1, row=8, padx=pad_x, pady=pad_y)

        hidden_text.bind("<FocusOut>", convert_hidden)
        cover_text.bind("<KeyRelease>", check_length)
        discord_var.set(True)



if __name__ == '__main__':
    root = Tk()
    MainWindow(root)
    root.mainloop()
