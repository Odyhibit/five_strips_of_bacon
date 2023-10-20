# Five slices of bacon
Is it steganography if it's obvious?

no.

Bacon's cipher was designed to hide text inside other text, or objects in photos.

Each character in the hidden text requires 5 bits of information. Maybe weather a character is bold, or not. Maybe wheather a line of people in a photo have their head turned to the side or not.
So why not "hide" 5 bits of information in a single character? Who would even notice?
Turns out everyone. This is an obnoxious combination. 
This works on the markdown used by discord. I included a zero width space character, because adjacent similar text modifiers would break stuff.

<img width="429" alt="Screenshot 2023-03-09 at 1 30 06 AM" src="https://user-images.githubusercontent.com/1384102/223951580-bd514d96-8f8f-40f6-97e7-5284ada5cbe9.png">


GitHubs markdown uses html for underline. Perhaps a GitHub/Discord selection can be added to the next version. The other modifiers need to be placed inside the html tags for underline. like this
**~~<ins>i</ins>~~**​<ins>S</ins>​ *~~I~~*​<ins>~~T~~</ins>​ **s**​<ins>t</ins>​**i**​*L*​*~~l~~*​ s​<ins>*t*</ins>​<ins>~~E~~</ins>​~~g~~​*a*​~~n~~​o​**~~g~~**​<ins>R</ins>​<ins>A</ins>​**p**​<ins>H</ins>​*Y*​ <ins>~~I~~</ins>​**f**​ <ins>*i*</ins>​**~~T~~**​'**S**​ ~~i~~​n​ <ins>*p*</ins>​~~l~~​<ins>A</ins>​<ins>**~~i~~**</ins>​**~~n~~**​ *S*​i​<ins>*g*</ins>​<ins>**h**</ins>​t?

<img width="735" alt="Screenshot 2023-03-09 at 1 10 26 AM" src="https://user-images.githubusercontent.com/1384102/223947538-f4e6f0fd-d53c-44da-beab-05fa3fc280c8.png">

Decoding them might be a pain, but making them is easy.



GitHub example encoding
* **Bold** text
* *italic* text
* <ins>underline</ins> text
* ~~strikethrough~~ text
* ***Bold italic*** text
* ~~**strike Bold**~~ text
* *~~italic strike~~* text
* <ins>~~underline strikethrough~~</ins> text
