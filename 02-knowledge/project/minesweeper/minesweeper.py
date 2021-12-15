import random
import logging

FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
logging.basicConfig(
    filename='history.log', format=FORMAT, level=logging.INFO)

logger = logging.getLogger('minesweeper')
class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.

        A cell is known to be a mine when:
        - any time the number of cells is equal to the count, we know that all of that sentence's cells must be mines.
        """
        if len(self.cells) == self.count:
            # it means all neighboring cells are mines
            # for example, if nearby_mines((0,0)) = 3, it must mean that
            # {(1,0), (1,1), (0,1)} = 3, or in plain english, they are all mines

            return self.cells
        
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            # it means all neighboring cells are safe
            # for example, if nearby_mines((0,0)) = 0, it must mean that 
            # {(1,0), (1,1), (0,1)} = 0, or in plain english, they are all safe

            return self.cells
        
        
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # if this sentence contains information about this cell, update it
        if cell not in self.cells:
            return None
        # remove cell from sentence
        # for instance, if I have:
        # {(1,0), (1,1), (0, 1)} = 2, and I discover somehow that (0,1) is a mine
        # then I remove (0,1) from the set and the resulting sentence would be
        # {(1,0), (1,1)} = 1
        self.cells.discard(cell)
        self.count -= 1


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # if this sentence contains information about this cell, update it
        if cell not in self.cells:
            return None

        # remove cell from sentence
        # for instance, if I have:
        # {(1,0), (1,1), (0, 1)} = 2, and I discover somehow that (0,1) is safe
        # then I remove (0,1) from the set and the resulting sentence would be
        # {(1,0), (1,1)} = 2
        self.cells.discard(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        # mark cell as safe
        self.safes.add(cell)

        # update knowledge to express that the cell is safe as well
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # step 1: mark as a move made
        self.moves_made.add(cell)
        
        # step 2: mark the cell as safe
        self.mark_safe(cell)
        
        # step 3: add the sentence regarding the new information coming from the click
        nearbies = set()
        # run through nearby elements
        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                # if cell within bounds
                if 0 <= i < self.height and 0 <= j < self.width:               
                    nearbies.add((i,j))
        
        # nearbies are the knowledge, remove self.safes to account the fact that they are not mines
        sentence = Sentence(nearbies - self.safes, count)
        
        # include only if new knowledge.
        if sentence not in self.knowledge:
            self.knowledge.append(sentence)
            logger.info(f'Knowledge included: {sentence}')
        

        # step 5
        new_cells = set()
        knowledge = []
        for sentence_a in self.knowledge:
            for sentence_b in self.knowledge:
                if sentence_a != sentence_b:
                    
                    if sentence_a.cells.issubset(sentence_b.cells):
                        new_cells = sentence_b.cells - sentence_a.cells
                        new_count = sentence_b.count - sentence_a.count
                    elif sentence_b.cells.issubset(sentence_a.cells):
                        new_cells = sentence_a.cells - sentence_b.cells 
                        new_count = sentence_a.count - sentence_b.count
                    if new_cells:
                        new_sentence = Sentence(new_cells, new_count)
                        if new_sentence not in self.knowledge and new_sentence not in knowledge:
                            knowledge.append(new_sentence)

        for k in knowledge:
            logger.info(f'Inferred knowledge: {k}')

        if len(knowledge):
            self.knowledge += knowledge

        # clean up knowledge to discard equal values
        self.knowledge = self.get_distinct_sentences()

        # step 4: mark safes and mines from knowledge
        for sentence in self.knowledge:
            known_safes = sentence.known_safes().copy()
            known_mines = sentence.known_mines().copy()
            if known_safes:
                logger.info(f'Marking {known_safes} as safes')
                for cell in known_safes:
                    self.mark_safe(cell)
            if known_mines:
                logger.info(f'Marking {known_mines} as mines')
                for cell in known_mines:
                    self.mark_mine(cell)

    def get_distinct_sentences(self):
        unique_sentences = []
        for s in self.knowledge:
            if s not in unique_sentences:
                unique_sentences.append(s)

        return unique_sentences

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # remove from set of safe moves, the moves already made.
        
        possible_safe_moves = self.safes - self.moves_made - self.mines
        logger.info(f'Possible safe moves: {possible_safe_moves}')
        logger.info(f'Mines known: {self.mines}')

        # if empty, we will have to make a random move
        if not len(possible_safe_moves):
            return None

        chosen = possible_safe_moves.pop()

        logger.info(f'Chosen move: {chosen}')

        return chosen

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        # Try to make an educated guess instead of a random move.
        # Make educated guesses after half the board is occupied
        # The educated guess can only envision its 'field of view', 
        # which considers only mine information, not far away.
        # So it seems better to, at the beginning, generate a really 
        # random choice.
        #if len(self.moves_made) / (self.height * self.width) > 0.5:
        guess = self.make_educated_guess()
        if guess:
            return guess
        logger.info('AI making random move. Cross your fingers ...')
        # create the set of all possible moves:
        all_possibilities = set()
        for i in range(self.height):
            for j in range(self.width):
                all_possibilities.add((i, j))
        
        possible_moves = all_possibilities - self.moves_made - self.mines - self.safes 
        # if no move was found, return None
        if not len(possible_moves):
            return None

        chosen = possible_moves.pop()
        
        
        logger.info(f'Chosen move: {chosen}')
        return chosen

    def make_educated_guess(self):
        """
        Returns a move to make on the Minesweeper board.
        
        This is similar to the random-move, however, it tries to use the probability
        of having a mine within a set of cells into account.

        The idea is: if you have two knowledges:
            - {(1,1), (2,2), (3,3)} = 1
            - {(4,4), (5,5)} = 1

        The first knowledge also tells you that the probability of having a mine is 1 out of 3 (33%)
        whereas the second knowledge is telling you that, if you pick one at random from it, you end 
        up with 1 out of 2 (50%) probability of choosing a mine. Hence, the first option is a better 
        guess.

        """
        # consider a random move as the ceiling
        # consider MINES to be the square root of the board for now
        MINES = int((self.height * self.width) ** 0.5) 
        complete_board = (self.height * self.width)
        explosion_probability = MINES / (complete_board - len(self.moves_made))
        educated_guess = set()

        logger.info(f'Random probability: {explosion_probability}')

        for sentence in self.knowledge:
            # i want to get the minimum value of explosion_probability
            # exclude division by zero
            if len(sentence.cells):
                if sentence.count / len(sentence.cells) < explosion_probability:
                    # number of mines / number of cells
                    explosion_probability = sentence.count / len(sentence.cells)
                    educated_guess = sentence.cells


        # create the set of all possible moves:
        possible_moves = educated_guess - self.moves_made - self.mines - self.safes 
        
        # if no move was found, return None
        if not len(possible_moves):
            return None

        logger.info('AI making educated guess. You may be more confident ...')
        logger.info(f'Educated Guess domain: {educated_guess}')
        logger.info(f'Probability of exploding: {explosion_probability}')

        chosen = possible_moves.pop()        
        logger.info(f'Chosen move: {chosen}')
        return chosen
