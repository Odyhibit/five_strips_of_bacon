# Five slices of bacon
Is it steganography if it's obvious?

no.

Bacon's cipher was designed to hide text inside other text, or objects in photos.

Each character in the hidden text requires 5 bits of information. Maybe weather a character is bold, or not. Maybe wheather a line of people in a photo have their head turned to the side or not.
So why not "hide" 5 bits of information in a single character? Who would even notice?
Turns out everyone. This is an obnoxious combination. 
This works on the markdown used by discord. I included a zero width space character, because adjacent similar text modifiers would break stuff.
It does not work well on GitHubs markdown. Some nested text modifiers do not work.

<img width="735" alt="Screenshot 2023-03-09 at 1 10 26 AM" src="https://user-images.githubusercontent.com/1384102/223947538-f4e6f0fd-d53c-44da-beab-05fa3fc280c8.png">

Decoding them might be a pain, but making them is easy.

*__h__*​~~i~~​D​*e*​ ~~m~~​*E*​
