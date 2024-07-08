"""This is the main GUI file."""
import pathlib

from customtkinter import CTkLabel, CTkTextbox, CTkButton, CTkRadioButton, CTkTabview, \
    os, StringVar, CTk
from PIL import ImageTk, Image

import src.encode_five_strips_of_bacon as encode_bacon
import src.decode_five_strips_of_bacon as decode_bacon


class MainWindow:
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-statements
    """The main window"""

    def __init__(self, root):
        current_dir = pathlib.Path(__file__).parent.resolve()

        image = Image.open(os.path.join(current_dir, "bacon_five.png"))
        icon_path = ImageTk.PhotoImage(image)
        root.wm_iconbitmap()
        root.iconphoto(False, icon_path)
        root.title("Five Strips of Bacon")

        tabcontrol = CTkTabview(root)
        tabcontrol.pack(expand=True)
        tabcontrol.pack(padx=20, pady=20)
        tabcontrol.add("Encode")
        tabcontrol.add("Decode")

        def convert_hidden(e):
            """This converts the secret text to show the limits of the bacon cipher.
            Only uppercase. J -> I and V -> U.
            """
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

        def tab_to_hidden_text(e):
            if e.keycode == 9:
                cover_text.focus_set()

        def check_length(e):
            """Check to see if there are enough cover text characters to hide the plaintext.
            If there is then we enable the calc_button, if not we disable it.

            :return: nothing is returned
            """

            if e.keycode == 9:
                calc_button.focus_set()
            cover_str = cover_text.get("1.0", "end-1c")
            hidden_str = hidden_text.get("1.0", "end-1c")

            cover_len = count_alpha(cover_str)
            hidden_len = count_alpha(hidden_str)
            if cover_len >= hidden_len:
                calc_button.configure(state="normal", text="Calculate cipher")
                cover_label.configure(text="Cover Text - long enough")
            else:
                calc_button.configure(state="disabled", text="Need more cover text")
                cover_label.configure(text=f"Cover Text - {hidden_len - cover_len} left")

        def count_alpha(text: str) -> int:
            """count the number of alphabet characters in a bit of text"""
            count = 0
            for letter in text:
                if letter.isalpha():
                    count += 1
            return count

        def calculate_cipher():
            """This function does the heavy lifting for the encoding.
            BISCUT Bold Italic Strikethrough Capital Underline - Text

            :return: returns nothing
            """

            hidden_str = hidden_text.get("1.0", "end-1c")
            cover_text_str = cover_text.get("1.0", "end -1c")
            output_format = output_type.get()

            output = encode_bacon.encode_cover_text(hidden_str, cover_text_str, output_format)
            cipher_text.delete("1.0", "end")
            cipher_text.insert("1.0", output)

        def decode_cipher():
            """decode the ciphered text, put it in the plain_text textbox """
            covered_text = ciphered_text.get("1.0", "end -1c")
            plain_text = decode_bacon.decode_cover_text(covered_text)
            plain_text_text.delete("1.0", "end")
            plain_text_text.insert("1.0", plain_text)

        def paste_cipher():
            """Get the clipboard contents paste it into ciphered_text textbox"""
            covered_text = root.clipboard_get()
            ciphered_text.delete("1.0", "end")
            ciphered_text.insert("1.0", covered_text)

        def copy_to_clipboard():
            """copy the cipher_text textbox to the clipboard"""
            field_value = cipher_text.get("1.0", 'end-1c')
            root.clipboard_clear()
            root.clipboard_append(field_value)

        #  ENCODING
        output_type = StringVar(root, "Discord")

        hidden_label = CTkLabel(master=tabcontrol.tab("Encode"),
                                text="Hidden Text - alphabet, "
                                     "and spaces only (I/J and U/V are combined)")
        hidden_text = CTkTextbox(master=tabcontrol.tab("Encode"), height=20, width=400)
        cover_label = CTkLabel(master=tabcontrol.tab("Encode"), text="Cover Text")
        cover_text = CTkTextbox(master=tabcontrol.tab("Encode"), height=20, width=400)
        cipher_label = CTkLabel(master=tabcontrol.tab("Encode"), text="Cipher Text")
        cipher_text = CTkTextbox(master=tabcontrol.tab("Encode"), height=60, width=400)
        calc_button = CTkButton(master=tabcontrol.tab("Encode"),
                                text="Calculate cipher",
                                command=calculate_cipher,
                                state="disabled")
        clip_button = CTkButton(master=tabcontrol.tab("Encode"), text="Copy cipher",
                                command=copy_to_clipboard)

        pad_x = 20
        pad_y = (0, 20)

        hidden_label.grid(column=0, row=1, columnspan=3, padx=pad_x)
        hidden_text.grid(column=0, row=2, columnspan=3, padx=pad_x, pady=pad_y)
        cover_label.grid(column=0, row=3, columnspan=3, padx=pad_x)
        cover_text.grid(column=0, row=4, columnspan=3, padx=pad_x, pady=pad_y)
        cipher_label.grid(column=0, row=5, columnspan=3, padx=pad_x)
        cipher_text.grid(column=0, row=6, columnspan=3, padx=pad_x, pady=pad_y)
        calc_button.grid(column=0, row=8, padx=pad_x, pady=pad_y)
        clip_button.grid(column=2, row=8, padx=pad_x, pady=pad_y)
        CTkRadioButton(tabcontrol.tab("Encode"),
                       text="Discord",
                       variable=output_type,
                       value="Discord").grid(column=0, row=7, padx=5, pady=pad_y)
        CTkRadioButton(tabcontrol.tab("Encode"),
                       text="GitHub",
                       variable=output_type,
                       value="GitHub").grid(column=1, row=7, padx=5, pady=pad_y)
        CTkRadioButton(tabcontrol.tab("Encode"),
                       text="Unicode",
                       variable=output_type,
                       value="Unicode").grid(column=2, row=7, padx=5, pady=pad_y)

        hidden_text.bind("<FocusOut>", convert_hidden)
        hidden_text.bind("<KeyRelease>", tab_to_hidden_text)
        cover_text.bind("<KeyRelease>", check_length)

        # DECODING
        ciphered_label = CTkLabel(master=tabcontrol.tab("Decode"), text="paste ciphered text")
        ciphered_text = CTkTextbox(master=tabcontrol.tab("Decode"), height=60, width=400)
        plain_text_label = CTkLabel(master=tabcontrol.tab("Decode"), text="recovered message")
        plain_text_text = CTkTextbox(master=tabcontrol.tab("Decode"), height=20, width=400)
        decode_button = CTkButton(master=tabcontrol.tab("Decode"), text="Decode cipher",
                                  command=decode_cipher)
        paste_button = CTkButton(master=tabcontrol.tab("Decode"), text="Paste",
                                 command=paste_cipher)

        ciphered_label.grid(column=0, row=0, columnspan=2, padx=pad_x, pady=pad_y)
        ciphered_text.grid(column=0, row=1, columnspan=2, padx=pad_x, pady=pad_y)
        plain_text_label.grid(column=0, row=2, columnspan=2, padx=pad_x, pady=pad_y)
        plain_text_text.grid(column=0, row=3, columnspan=2, padx=pad_x, pady=pad_y)

        decode_button.grid(column=0, row=4, padx=pad_x, pady=pad_y)
        paste_button.grid(column=1, row=4, padx=pad_x, pady=pad_y)


def main():
    """Create the root window, and start the mainloop."""
    root = CTk()
    MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
