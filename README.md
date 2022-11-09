# Hangman AI
#### Video Demo:  <https://youtu.be/Seeip7YgHNo>
## Overview of Project Goal
The premise of this project is to take a word inputted by the user and, using the feedback provided in a traditional game of Hangman, generate that word in as few guesses as possible. Here, the program takes the role which is usually regarded as "playing" Hangman, so is more of a Hangman AI than a Hangman Game.

I chose this topic primarily because I though its implementation would be challenging, but within my means - without much focus on the optimal user experience/commercial viability. However, for arguments sake, I will also make the case that the program serves as a test of how good a Hangman word is, or more generally its rarity in comparison to the rest of the English language.

## How the Program Works
Evidently, it is no challenge to return a users input, so the design focuses on playing Hangman honestly - that is only using information gained from previous guesses.

The program first parses a text document for words that could be the hangman word (based on what we should know). In excruciating detail this means they are of the same size, don't contain guessed letters that weren't in the hangman word, have the letters in the positions that match what we have guessed so far, and finally don't have any extra copies of said letters.

The program then guesses the most frequent letter of this sample, and tests it against the hangman word. Information from this guess is appended to the parsing criteria, and the cycle repeats until the whole word has been recreated.

Functionally, the program is done, but just spitting the output into the terminal would leave the user dissatisfied, or at least unable to appreciate the decisions the AI made at each step of the process. Instead, the guesses are passed to and animated by a custom scene implemented using manim. This then creates a video which shows the process step by step, and determines how close the users word came to "winning".

Note the animation quality defaults to 480p, but can be increased to 720p/1080p by passing "-q medium/high" respectively as command line arguments. Running "python project.py" will automatically take care of the animation.

## Design Choices
I would summarise my main design considerations as minimising guesses, preventing scope creep, and user experience, in rough order of importance.

Scope creep refers to continually expanding goals after beginning the project, and is the easiest of the above to address. This encompasses design choices like not accommodating for hyphenated/multiple words, or adding the other side of the hangman game. The former simply don't fit into my idea of hangman inputs, and add significant complexity to both the animation and trial word validation.

The latter falls in theory benefits user experience, but in practice required a total overhaul of the program to do correctly. Manim is a library typically used to animate maths videos, and has no real focus on interaction. In particular, I couldn't find a way to append a clip to the video while keeping the user at the same timestamp. This would mean a user would have to go through all previous animations with each guess - which I didn't deep acceptable. Since this wasn't inline with my goals anyway, I ultimately scrapped the idea.

On manim more generally, this was the only animation library I had heard of, and since I liked its style and found it easy to use, I chose not to entertain other options. I'm prepared to admit there was probably a better option, but I wanted to learn this library and also believed it was sufficient for my needs. The program defaults to low quality to render in a timely manner, as I ultimately decided they were more likely to leave if they had to wait longer, than if the quality was worse.

For minimising guesses, other than the steps in "How the Project Works", the main topic of debate was the text document initially used. The program gets significantly weaker if a input word is not featured,  but since each candidate word is weighed equally, too many obscure words dilute the pool of more likely options. I settled for "words.txt" as it seemed to perform the best out of the documents I tried, and 58,000 words seemed sufficient. Longer open source lists were also often made for autocorrect applications, and so had place/organisation names that I wouldn't consider to be viable hangman words.

As a final note on user experience I opted to have the user type in the full word as opposed to a more transparent option. While I could have the honesty of the program more apparent, by exchanging information in a more interactive manner (asking for size, positions of guesses...), a user can just check the code if they don't believe me. In my opinion the latter makes the experience more cumbersome, and prone to user error - a lose-lose for all but most distrustful users.

## Other Files
The installation lines for required packages are featured in "requirements.txt", and the output creates a media folder that houses the animation. The file "test_project.py" features unit tests on the 3 unit functions of the main program. For this we instead parse "testwords.txt" which was created to have easily countable contents, while allowing for testing of all potential validation mistakes.

Most of the animations are imported from "hangman.py". This serves to declutter and bring clarity to the "project.py" file, as the animations can be hard to follow, and I felt the animation functions should be separate from the "logical" ones. The one exception is "show_valid_add_letters", which uses "letter_position" from the main file, and so stays there to prevent circular imports.

In event of tied frequencies the program defers to the most used letter [of those tied] across all words. This order was/can be calculated using "default_order".
