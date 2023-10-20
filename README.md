# Five slices of bacon
Is it steganography if it's obvious?

no.

Bacon's cipher was designed to hide text inside other text, or objects in photos.

Each character in the hidden text requires 5 bits of information. For example it could be if a character is bold, or not. Maybe wheather people in a photo have their head turned to the side or not.
So why not "hide" 5 bits of information in a single character? Who would even notice?
Turns out everyone. This is an obnoxious combination. 
This works on the markdown used by discord. I included a zero width space character, because adjacent similar text modifiers would break stuff.

<img width="429" alt="Screenshot 2023-03-09 at 1 30 06 AM" src="https://user-images.githubusercontent.com/1384102/223951580-bd514d96-8f8f-40f6-97e7-5284ada5cbe9.png">


GitHubs markdown uses html for underline. Simply select the output format you wish, either Discord style markdown, or GitHub style markdown.

<img width="720" alt="Screenshot 2023-10-19 at 10 50 08 PM" src="https://github.com/Odyhibit/five_slices_of_bacon/assets/1384102/a128fe9b-ab46-442c-9773-c3c8db3f428b">

Decoding them might be a pain, but making them is easy.

