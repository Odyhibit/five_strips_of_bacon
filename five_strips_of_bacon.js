// Bacon Cipher has A-Z with I/J and U/V combined
        const baconDictionary = {
            "a": "00000", "b": "00001", "c": "00010", "d": "00011", "e": "00100",
            "f": "00101", "g": "00110", "h": "00111", "j": "01000", "i": "01000",
            "k": "01001", "l": "01010", "m": "01011", "n": "01100", "o": "01101",
            "p": "01110", "q": "01111", "r": "10000", "s": "10001", "t": "10010",
            "v": "10011", "u": "10011", "w": "10100", "x": "10101", "y": "10110", "z": "10111"
        };

        const reverseBaconDictionary = Object.fromEntries(
            Object.entries(baconDictionary).map(([key, value]) => [value, key])
        );

        const hiddenInput = document.getElementById("hiddenText");
        const coverInput = document.getElementById("coverText");
        const cipherInput = document.getElementById("results");
        const messageInput = document.getElementById("message");
        const encodeButton = document.getElementById('encodeButton');
        const decodeButton = document.getElementById('decodeButton');


        coverInput.addEventListener('keyup', function() {
            // console.log(countAlphabet(coverInput.value), countAlphabet(hiddenText.value));
            if(countAlphabet(coverInput.value) >= countAlphabet(hiddenText.value)) {
                encodeButton.removeAttribute('disabled');
                messageInput.textContent = "";
            } else {
                let requiredLength = countAlphabet(hiddenText.value) - countAlphabet(coverInput.value);
                messageInput.textContent = "Cover text must be at least " + requiredLength + " characters longer.";
                encodeButton.setAttribute('disabled', '');
            }
        });

        hiddenInput.addEventListener('input', function() {
            let hiddenText = hiddenInput.value;
            hiddenInput.value = hiddenText.replace(/[^a-zA-Z\s]/g, '').toUpperCase();
        });

        coverInput.addEventListener('input', function(){
            let coverText = coverInput.value;
            coverInput.value = coverText.replace(/[^a-zA-Z\s]/g, '').toLowerCase();

        });

        cipherInput.addEventListener('input', function() {
            if(cipherInput.value.length > 0) {
                decodeButton.removeAttribute('disabled');
            } else {
                decodeButton.setAttribute('disabled', '');
            }
        });

        function getBitMask(hiddenText) {
            return hiddenText.toLowerCase().split('').map(char => baconDictionary[char] || '').join('');
        }

        function hasCodepoint(str, codePoint) {
          let count = 0;
          for (const char of str) {
            if (char === codePoint) {
              return true;
            }
            count++;
          }
          return false;
        }

        function isInRange(number, min, max) {
            return number >= min && number <= max;
        }

        function countAlphabet(text) {
            const cleanedText = text.toLowerCase().replace(/[^a-z]/g, ''); // Remove non-alphabetic characters and convert to lowercase
            return cleanedText.length;
        }

        function encodeCoverText() {
            /**
             * This function does the heavy lifting for the encoding.
             * BISCUT Bold Italic Strikethrough Capital Underline - Text
             *
             * @return {string} Cover text with modifiers
             */

            const wordJoiner = "\u2060";
            const noBreakSpace = "\ufeff";
            let output = "";
            let coverIndex = 0, hiddenIndex = 0, binStrIndex = 0;
            let needToEndCode = true;
            let hiddenText = document.getElementById("hiddenText").value;
            let coverText = document.getElementById("coverText").value;

            const secretBinStr = getBitMask(hiddenText);

            while (coverIndex < coverText.length) {
                if (hiddenIndex < hiddenText.length) {
                    if (/[a-zA-Z]/.test(coverText[coverIndex])) {
                        if (hiddenText[hiddenIndex] === " ") {
                            output += wordJoiner;
                            hiddenIndex++;
                        } else {
                            output += modifyLetter(
                                coverText[coverIndex],
                                secretBinStr.substring(binStrIndex * 5, binStrIndex * 5 + 5)
                            );
                            hiddenIndex++;
                            binStrIndex++;
                            coverIndex++;
                        }
                    } else if (coverText[coverIndex] === " ") {
                        output += " ";
                        coverIndex++;
                    }
                } else {
                    if (needToEndCode) {
                        output += noBreakSpace;
                        needToEndCode = false;
                    }
                    output += coverText[coverIndex];
                    coverIndex++;
                }
            }
            // console.log(output);
            document.getElementById("results").value = output;
        }


        function modifyLetter(letter, bitMask) {
            let zeroWidthSpace = "\u200B";
            let modifiedLetter = letter;


            if (/[a-zA-Z]/.test(letter)) {
                const letterOffset = letter.toUpperCase().charCodeAt(0) - 65;
                // console.log(bitMask, letterOffset,parseInt('0x1d400', 16) + letterOffset);
                // console.log(String.fromCodePoint(parseInt('0x1d41a', 16) + letterOffset));
                //Bold,uppercase
                if (bitMask[0] === "1" && bitMask[3] === "1") modifiedLetter = String.fromCodePoint(parseInt('0x1d400', 16) + letterOffset);
                //Bold, lowercase
                else if (bitMask[0] === "1" && bitMask[3] !== "1") modifiedLetter = String.fromCodePoint(parseInt('0x1d41a', 16) + letterOffset);
                // italic, uppercase
                else if (bitMask[1] === "1" && bitMask[3] === "1") modifiedLetter = String.fromCodePoint(parseInt('0x1D434', 16) + letterOffset);
                //italic, lowercase
                else if (bitMask[1] === "1" && bitMask[3] !== "1") modifiedLetter = String.fromCodePoint(parseInt('0x1d44e', 16)  + letterOffset);
                                if (letterOffset == 7){
                                    this_letter = String.fromCodePoint(parseInt(0x210e, 16));  // glyph is reserved, so use plank's constant
                                }
                //regular uppercase
                if (bitMask.substring(0, 2) === "00" && bitMask[3] === "1") modifiedLetter = letter.toUpperCase();
                // strikethrough
                if (bitMask[2] === "1") modifiedLetter += "\u0336";
                // underline
                if (bitMask[4] === "1") modifiedLetter += "\u0332";
            }
            // console.log(modifiedLetter, zeroWidthSpace);
            return modifiedLetter + zeroWidthSpace;
        }



        function decodeText() {
            const cipherText = document.getElementById("results").value;
            let output = "";
            let cover = "";
            let keep_going = true;
            const letters = cipherText.split("\u200B");
            console.log(letters)

            for (let char of letters) {
                if (hasCodepoint(char, "\ufeff")) {
                    keep_going = false;
                }
                char = char.trimStart();   // remove spaces from cover text

                if(hasCodepoint(char, "\u2060")) {
                    output += " ";        // add space from hidden text
                    char = char.slice(1); //then remove
                }

                if (char !== "" && keep_going){
                    let bitMask = decodeLetter(char);
                    output += reverseBaconDictionary[bitMask] || "?";
                }
            }

            for (const char of letters) {
                const codePoint = char.codePointAt(0);
                if(codePoint >= 32){
                    cover += decodeCoverLetter(char);
                }

                console.log(`Character: ${char}, Code Point: ${codePoint}`);
            }

            document.getElementById("hiddenText").value = output.toUpperCase();
            document.getElementById("coverText").value = cover;
        }

        function decodeLetter(letter) {
            // Bold, Itallic, Strikethrough, Capital, Underline
            // Bold 0x1D400 - 0x1D433
            // Itallic 0x1D434 - 0x1D467
            // Strikethrough \u0336
            // Capital 0x1D400-0x1D419 ||  0x1D434-1D44D || 0x41-0x5A
            // Underline \u0332

            let strikethrough = "\u0336";
            let underline = "\u0332";
            //console.log(letter);
            let output = [0, 0, 0, 0, 0];
            let firstCodePoint = letter.codePointAt(0);

            if (isInRange(firstCodePoint, 0x1D400, 0x1D433)) output[0] = 1;  // Bold
            if (isInRange(firstCodePoint, 0x1D434, 0x1D467)) output[1] = 1;  // Itallic
            if (hasCodepoint(letter,strikethrough)) output[2] = 1;    // Strikethrough
            if (isInRange(firstCodePoint, 0x1D400, 0x1D419) || isInRange(firstCodePoint, 0x1D434, 0x1D44D) || isInRange(firstCodePoint, 0x41, 0x5A)) output[3] = 1;    // Strikethrough
            if (hasCodepoint(letter,underline)) output[4] = 1;
            //console.log(output.join(""))
            return output.join("").toUpperCase();
        }

        function decodeCoverLetter(letter) {
            // Bold, Itallic, Strikethrough, Capital, Underline
            // Bold 0x1D400 - 0x1D433
            // Itallic 0x1D434 - 0x1D467
            // Strikethrough \u0336
            // Capital 0x1D400-0x1D419 ||  0x1D434-1D44D || 0x41-0x5A
            // Underline \u0332

            let strikethrough = "\u0336";
            let underline = "\u0332";
            let output = "";
            let firstCodePoint = letter.trimStart().codePointAt(0);
            let possibleSpace = letter.codePointAt(0);
            if (firstCodePoint == 0x2060)firstCodePoint = letter.trimStart().codePointAt(1);

            console.log(letter, firstCodePoint);
            if(possibleSpace === 32) output = " ";

            if (isInRange(firstCodePoint, 0x1D400, 0x1D419)) output += String.fromCharCode(firstCodePoint - 0x1D400 + 97);  // Bold upper
            if (isInRange(firstCodePoint, 0x1D41A, 0x1D433)) output += String.fromCharCode(firstCodePoint - 0x1D41A + 97);  // Bold lower

            if (isInRange(firstCodePoint, 0x1D434, 0x1D44C)) output += String.fromCharCode(firstCodePoint - 0x1D434 + 97);  // Itallic upper
            if (isInRange(firstCodePoint, 0x1D44E, 0x1D467)) output += String.fromCharCode(firstCodePoint - 0x1D44E + 97);  // Itallic lower

            if (isInRange(firstCodePoint, 0x41, 0x5A)) output += String.fromCharCode(firstCodePoint).toLowerCase();  //  upper
            if (isInRange(firstCodePoint, 0x61, 0x7A)) output += String.fromCharCode(firstCodePoint);  //  upper

            //console.log(output.join(""))
            return output;
        }