import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> N V | Det N V | NA V | V
NA -> Adj N | N ConjS | N Adv | N | Det N | Det N PP
V -> V DetP | V PP | V Adv | V Adv ConjS | V N PP | V N
DetP -> Det NA | PP | Det Adj | Det Adj Adj Adj
PP -> P NA | P Det NA
ConjS -> Conj S
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    contents = []
    contents.extend([
        word.lower() for word in
        nltk.word_tokenize(sentence)
        if any(c.isalpha() for c in word)
    ])
    return contents


def np_chunk(tree):
    chunks = []

    for subtree in tree.subtrees():
        if subtree.label() == "N" or subtree.label() == "Det N":
            if not any(child.label() == "N" or child.label() == "Det N" for child in subtree.subtrees(lambda t: t != subtree)):
                chunks.append(subtree)

    return chunks

if __name__ == "__main__":
    main()
