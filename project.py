from manim import *
from hangman import *
import argparse


class HangmanGame(MovingCameraScene):
    def construct(self):
        HangmanGallows.construct(self)
        underlines = Hangman.create_underlines(self, hangman)
        j = 0
        unique_letters = list(
            dict.fromkeys([d["letter"] for d in TrialWord.known_letters])
        )
        for letter in unique_letters:
            l = Hangman.create_letter(self, text=letter)
            if letter in hangman.word:
                show_valid_add_letters(
                    self, letter, hangman, vgroup=underlines, text_object=l
                )
            elif j > 8:
                Hangman.just_enlarge_red(self, text_object=l)
            elif j > 7:
                Hangman.also_remove_man(self, vgroup=Hangman.man, text_object=l)
                j += 1
            else:
                Hangman.also_add_to_man(
                    self, vgroup=Hangman.man, text_object=l, index=j
                )
                j += 1
            Hangman.shrink_and_remove(self, text_object=l)


def show_valid_add_letters(
    self, letter, hangman, vgroup=VGroup(), text_object=Text("a")
):
    all_copies = VGroup()
    for i in letter_position(letter, hangman):
        l_text = Text(letter.upper()).next_to(vgroup[i], UP).scale(vgroup[i].width)
        all_copies.add(l_text)
    self.play(
        text_object.animate.set_color(GREEN).scale(1.5),
        FadeIn(all_copies),
        runtime=0.5,
    )


class HangmanWord:
    def __init__(self, word):
        self.word = word
        self.size = len(word)

    @property
    def word(self):
        return self._word

    @word.setter
    def word(self, word):
        if word.isalpha():
            self._word = word
        else:
            raise ValueError("Contains special characters/numbers")


class TrialWord:
    known_letters = []

    def __init__(self, word):
        self.l_pos = [{"letter": l, "position": k} for k, l in enumerate(word)]
        self.word = word
        self.size = len(word)
        self.letter_frequency = self.count_letters()

    @property
    def word(self):
        return self._word

    @word.setter
    def word(self, word):
        if letters_match(self) == False:
            raise ValueError("doesn't have all letters in the right place")
        if has_extra_copies(word):
            raise ValueError("has duplicates where hangman doesn't")
        if has_invalid_letter(word):
            raise ValueError("has invalid letter")
        self._word = word

    def count_letters(self):
        d = {letter: 0 for letter in "eisarntolcdugpmhbyfvwkxqjz"}
        for letter in self.word:
            d[letter] += 1
        return d

    def __add__(self, other):
        return {
            letter: self.letter_frequency[letter] + other[letter]
            for letter in "eisarntolcdugpmhbyfvwkxqjz"
        }


def main():
    global hangman
    while True:
        try:
            hangman = HangmanWord(input("Hangman Word: ").strip().lower())
            break
        except ValueError:
            pass
    match_candidate_letters(hangman)
    args = setup_parser()
    with tempconfig({"quality": f"{args.q}_quality"}):
        scene = HangmanGame()
        scene.render()


def match_candidate_letters(hangman):
    letters_found = 0
    while letters_found < hangman.size:
        letter_frequency = get_letter_frequency(hangman)
        most_frequent_letter = get_most_frequent(letter_frequency)
        no_copies = True
        for i in letter_position(most_frequent_letter, hangman):
            TrialWord.known_letters.append(
                {"letter": most_frequent_letter, "position": i}
            )
            letters_found += 1
            no_copies = False
        if no_copies:
            TrialWord.known_letters.append(
                {"letter": most_frequent_letter, "position": "None"}
            )


def letter_position(l, hangman):
    for position, letter in enumerate(hangman.word):
        if letter == l:
            yield position


def get_most_frequent(letter_frequency):
    i = 0
    list_of_d = [
        {"letter": l, "frequency": letter_frequency[l]} for l in letter_frequency
    ]
    while True:
        most_frequent_letter = sorted(
            list_of_d, key=lambda d: d["frequency"], reverse=True
        )[i]["letter"]
        if most_frequent_letter not in [d["letter"] for d in TrialWord.known_letters]:
            return most_frequent_letter
        else:
            i += 1


def get_letter_frequency(hangman, doc="words.txt"):
    with open(doc) as file:
        cumulative_frequency = {letter: 0 for letter in "eisarntolcdugpmhbyfvwkxqjz"}
        for line in file:
            line = line.rstrip()
            if len(line) == hangman.size and line.isalpha():
                try:
                    word = TrialWord(line)
                    cumulative_frequency = word + cumulative_frequency
                except ValueError:
                    pass
        return cumulative_frequency


def letters_match(self):
    does_have = [d for d in TrialWord.known_letters if d["position"] != "None"]
    return all(d in self.l_pos for d in does_have)


def has_extra_copies(word):
    in_hangman = [
        d["letter"] for d in TrialWord.known_letters if d["position"] != "None"
    ]
    mutual_letters = [l for l in word if l in in_hangman]
    return len(mutual_letters) != len(in_hangman)


def has_invalid_letter(word):
    not_in = [d["letter"] for d in TrialWord.known_letters if d["position"] == "None"]
    for letter in not_in:
        if letter in word:
            return True
    return False


def setup_parser():
    parser = argparse.ArgumentParser(description="Play Hangman against the AI")
    parser.add_argument(
        "-q", default="low", help="video quality low/medium/high", type=str
    )
    arg = parser.parse_args()
    if arg.q not in ["low", "medium", "high"]:
        arg.q = "low"
    return arg


if __name__ == "__main__":
    main()
