from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
A_statement = And(AKnight, AKnave)  # This is what A says

knowledge0 = And(
    # A is either a knight or a knave, but not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # The core of the puzzle: what A says
    Implication(AKnight, A_statement),  # If A is a knight, then the statement is true
    Implication(AKnave, Not(A_statement)),  # If A is a knave, then the statement is false
)

A1_statement = And(AKnave, BKnave)
# Puzzle 1
# A says "We are both knaves."
# B says nothing.
Basic_statement = And(Or(AKnight, AKnave),
                      Or(BKnight, BKnave),
                      Not(And(AKnight, AKnave)),
                      Not(And(BKnight, BKnave)))
knowledge1 = And(
    Basic_statement,
    Implication(AKnight, A1_statement), Implication(AKnave, Not(A1_statement)),
)

A2_statement = Or(And(AKnave, BKnave), And(AKnight, BKnight))
B2_statement = Or(And(AKnave, BKnight),
                  And(BKnight, AKnave),
                  And(BKnave, AKnight),
                  And(AKnight, BKnave))
# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Basic_statement,
    Implication(A2_statement, B2_statement), Implication(AKnight, Not(B2_statement)),
)

A3_statement = And(AKnave, AKnight)
B3_statement = AKnave
B3C_statement = CKnave
C_statement = AKnight
# Final knowledge base
knowledge3 = And(
    Basic_statement,
    Or(CKnight, CKnave),Not(And(CKnight, CKnave)),
    Implication(BKnight, And(B3_statement, B3C_statement)),
    Implication(BKnave, Not(And(B3_statement, B3C_statement))),
    Implication(CKnight, C_statement), Implication(CKnave, Not(C_statement)),
)
knowledge3.add(Not(BKnight))
def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
