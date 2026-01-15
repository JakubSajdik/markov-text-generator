import sys
import random

def tokenize(text):
    #here I split the text into words / tokens
    text = text.lower()
    tokens = []
    temp = ''
    for char in text:
        if 'a' <= char <= 'z':
            temp += char
        else:
            if temp != '':
                tokens.append(temp)
                temp = ''
    #if anything is still inside temp I empty it
    if temp != '':
        tokens.append(temp)
    return tokens

def build_markov(tokens):
    #here i create dict of dicts based on which i will be able to predict the next word
    model = {}
    for i in range(len(tokens)-1):
        w = tokens[i]
        nxt = tokens[i+1]

        if w not in model:
            model[w] = {}
        if nxt not in model[w]:
            model[w][nxt] = 0
    #I raise the weight if the word appears after the previous one multiple times
        model[w][nxt] += 1

    return model


def weighted_choice(counts):
    # here i choose what word will follow the previous word, based on probability
    total = sum(counts.values())
    r = random.randrange(total)
    cumulative = 0

    for word, c in counts.items():
        cumulative += c
        if r < cumulative:
            return word



def generate_text(model, num_words):
    # here i take the the model and generate words from random seed in range num_words(user input)

    current = random.choice(list(model.keys()))
    result = [current]

    for _ in range(num_words - 1):
        if current not in model or not model[current]:
            break

        next_word = weighted_choice(model[current])
        result.append(next_word)
        current = next_word

    return " ".join(result)


def main():
    # 1. load user input
    if len(sys.argv) != 3:
        print("Usage: python markov.py <input_file> <num_words>")
        sys.exit(1)
    filename = sys.argv[1]
    num_words = int(sys.argv[2])

    # 2. load data
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()

    # 3. process
    tokens = tokenize(text)
    if len(tokens) < 2:
        print("Not enough tokens to build a Markov model.")
        sys.exit(1)

    model = build_markov(tokens)
    output = generate_text(model, num_words)

    # 4. output
    print(output)

if __name__ == "__main__":
    main()

