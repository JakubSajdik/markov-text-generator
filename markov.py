import sys          
import random       


def tokenize(text):
    """
    Convert raw text into a list of word tokens.
    Rules:
    - we will put everything into lowecase
    - we will only keep alphabetic characters
    - also we will keep apostrophes and dashes only if they are surrounded by letters
    """

    
    text = (text.lower().replace("’", "'").replace("–", "-")) # normalize some unicode punctuation

    tokens = []     # final list of words
    temp = ''       # current word being built character by character

    for i in range(len(text)):

        # case 1: alphabetic character, always part of a word
        if text[i].isalpha():
            temp += text[i]

        # case 2: apostrophe or dash
        # keep it ONLY if it is between two letters (for example don't, blue-green)
        elif text[i] in ["'", "-"]:
            if 0 < i < len(text) - 1:
                if text[i+1].isalpha() and text[i-1].isalpha():
                    temp += text[i]

        # case 3: any other character is a boundary
        else:
            if temp != '':
                tokens.append(temp)
                temp = ''

    # flush last token if text ends with a letter, not symol
    if temp != '':
        tokens.append(temp)

    return tokens


def build_markov(tokens):
    """
    Build a first-order markov model.
    model[word][next_word] = number of times next_word follows word
    """

    model = {}

    for i in range(len(tokens) - 1):
        w = tokens[i]        # current word
        nxt = tokens[i + 1]  # word that follows it

        # create dictionary if word was not seen before
        if w not in model:
            model[w] = {}

        # create a count if not seen
        if nxt not in model[w]:
            model[w][nxt] = 0

        # increment frequency (this is the "learning" or whatever)
        model[w][nxt] += 1

    return model


def weighted_choice(counts):
    """
    Choose a key from counts(which is a dict) with probability
    proportional to its value.
    """

    total = sum(counts.values())       # total weight
    r = random.randrange(total)        # random intger in [0, total-1]
    cumulative = 0

    # walk through cumulative until we hit the correct key
    for word, c in counts.items():
        cumulative += c
        if r < cumulative:
            return word


def generate_text(model, num_words):
    """
    Generate text using the Markov model.
    - start from a random first word
    - repeatedly sample next word using weighted choise function
    """

    # choose random starting word
    current = random.choice(list(model.keys()))
    result = [current]

    # generate remaining words
    for _ in range(num_words - 1):

        # stop early if current word does not have any word that follows it in model
        if current not in model or not model[current]:
            break

        # choose next word based on probabilities that the markov model has
        next_word = weighted_choice(model[current])

        result.append(next_word)
        current = next_word

    return " ".join(result)


def main():
    """
    Entry point of the program.
    Handles:
    - arguments
    - loading file user gives it
    - construction of the model
    - and generating the text
    """

    # 1. command line arguments check
    if len(sys.argv) != 3:
        print("Usage: python markov.py <input_file> <num_words>")
        sys.exit(1)

    filename = sys.argv[1]
    num_words = int(sys.argv[2])

    # 2. read input text
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()

    # 3. tokenize text
    tokens = tokenize(text)

    # need at least one transition otherwise it would not work
    if len(tokens) < 2:
        print("Not enough tokens to build a Markov model.")
        sys.exit(1)

    # build model and generate output
    model = build_markov(tokens)
    output = generate_text(model, num_words)

    # 4. output result
    print(output)


# this ensures that the code runs only in this code, not if its imported
if __name__ == "__main__":
    main()
