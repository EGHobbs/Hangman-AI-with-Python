from project import TrialWord


def main():
    cumulative_frequency = get_total_frequency()
    print(*order_by_frequency(cumulative_frequency), sep="")


def get_total_frequency(doc="words.txt"):
    with open(doc) as file:
        cumulative_frequency = {letter: 0 for letter in "etaoinsrhdlucmfywgpbvkxqjz"}
        for line in file:
            line = line.rstrip()
            if line.isalpha():
                try:
                    word = TrialWord(line)
                    cumulative_frequency = word + cumulative_frequency
                except ValueError:
                    pass
        return cumulative_frequency


def order_by_frequency(letter_frequency):
    list_of_d = [
        {"letter": l, "frequency": letter_frequency[l]} for l in letter_frequency
    ]
    sorted_by_frequency = sorted(list_of_d, key=lambda d: d["frequency"], reverse=True)
    return [sorted_by_frequency[i]["letter"] for i in range(26)]


if __name__ == "__main__":
    main()
