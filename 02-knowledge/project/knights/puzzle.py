from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
sentence = And(AKnight, AKnave)
knowledge0 = And(
    # game knowledge
    # each character is either a knight or a knave,
    Or(AKnight, AKnave),
    # but not both
    Biconditional(AKnight, Not(AKnave)),
    # if a knight states a sentence, then it is true
    Implication(AKnight, sentence),
    # if a knave states a sentence, then the sentence is false
    Implication(AKnave, Not(sentence)),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
sentence = And(AKnave, BKnave)

knowledge1 = And(
    # game knowledge
    # each character is either a knight or a knave,
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    # but not both
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    # if a knight states a sentence, then it is true
    Implication(AKnight, sentence),
    # if a knave states a sentence, then the sentence is false
    Implication(AKnave, Not(sentence)),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
sentenceA = Or(And(AKnight, BKnight), And(AKnave, BKnave))
sentenceB = Or(Biconditional(AKnight, BKnave), Biconditional(AKnave, BKnight))

knowledge2 = And(
    # game knowledge
    # each character is either a knight or a knave,
      # each character is either a knight or a knave,
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    # but not both
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    # if a knight states a sentence, then it is true
    Implication(AKnight, sentenceA),
    # if a knave states a sentence, then the sentence is false
    Implication(AKnave, Not(sentenceA)),
    Implication(BKnight, sentenceB),
    Implication(BKnave, Not(sentenceB)),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

sentenceA_1 = AKnight
sentenceA_2 = AKnave

sentenceB_2 = CKnave
sentenceC = AKnight

knowledge3 = And(
    # game knowledge
    # each character is either a knight or a knave,
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    # but not both
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(CKnight, Not(CKnave)),
    
    # A says
    Or(
        And(
            Implication(AKnight, sentenceA_1), 
            Implication(AKnave, Not(sentenceA_1)),
        ),
        And(
            Implication(AKnight, sentenceA_2), 
            Implication(AKnave, Not(sentenceA_2)),
        )
    ),

    # B says
    # B says "A said 'I am a knave'.". If B is telling the truth (BKnight), then
    # it must be the fact that if a is a knave, it must but a knight (a paradox)
    Implication(BKnight, Implication(AKnave, AKnight)),

    Implication(BKnight, sentenceB_2),
    Implication(BKnave, Not(sentenceB_2)),

    # C Says
    # if a knight states a sentence, then it is true
    Implication(CKnight, sentenceC),
    # if a knave states a sentence, then the sentence is false
    Implication(CKnave, Not(sentenceC)),


)


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
