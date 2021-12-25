import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent,
        meaning that every value in a variable's domain satisfy the unary 
        constraints.

        Remove any values that are inconsistent with a variable's unary
        constraints; in this case, the length of the word.
        """
        # Apply unary constraint 
        variables = self.domains.keys()
        for var in variables:
            domain = self.domains[var].copy()
            for word in self.domains[var]:
                if len(word) != var.length:
                    domain.discard(word)
            # overwrite domain
            self.domains[var] = domain

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # if there are no overlaps between variables, 
        # then there are no restrictions
        if not self.crossword.overlaps[x,y]:
            return False

        n1, n2 = self.crossword.overlaps[x,y]
        
        domain = self.domains[x].copy()
        
        for d1 in self.domains[x]:
            # initialize acceptable flag to latter remove unacceptable domains from x
            fl_acceptable = False

            for d2 in self.domains[y]:
                # equal words are not acceptable
                if d1 == d2:
                    continue
                
                if d1[n1] == d2[n2]:
                    fl_acceptable = True
                    break
                
            # if all of them are unnacceptable, remove from x's domain:
            if not fl_acceptable:
                domain.discard(d1)
        
        if self.domains[x] == domain:
            return False
        else:
            self.domains[x] = domain

        return True

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if not arcs:
            # consider all arcs in the problem
            variables = self.domains.keys()
            arcs = []
            for v1 in variables:
                for v2 in variables:
                    if v1 == v2:
                        continue
                    arc = (v1, v2)
                    arcs.append(arc)
        else:
            pass

        while len(arcs) > 0:
            v1, v2 = arcs.pop()

            if self.revise(v1, v2):
                if not self.domains[v1]:
                    # there's no way to solve this problem
                    return False
                for vn in (self.crossword.neighbors(v1) - {v2}):
                    # if we've modified v1's domain, there might 
                    # be some other (vn, v1) that was arc-consistent, but 
                    # now is not anymore. 
                    arcs.append((vn, v1))


        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        self.consistent(assignment)
        variables = set(self.domains.keys())
        for var in variables:
            if var not in assignment.keys():
                return False

            if not assignment.get(var):
                return False
        
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        words = []
        variables = set(assignment.keys())
        
        for v1 in variables:
            
            assigned_word = assignment.get(v1, '')
            # if the size differs from expected, not consistent
            if not len(assigned_word) == v1.length:
                return False
            
            # append to check whether they have same values afterwards
            words.append(assigned_word)

            # if conflicting characters, not consistent
            for v2 in variables:
                if v1 != v2:
                    
                    overlaps = self.crossword.overlaps[v1,v2]
                    if not overlaps:
                        continue
                    n1, n2 = overlaps
                    if assignment[v1][n1] != assignment[v2][n2]:
                        return False

        # if there are repeated ones, not consistent
        if len(words) != len(set(words)):
            return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        return self.domains[var]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        assigned_variables = set(assignment.keys())
        all_variables = set(self.domains.keys())
        unassigned_variables = all_variables - assigned_variables
        chosen = unassigned_variables.pop()

        return chosen

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result:
                    return result
            else:
                assignment.pop(var)
            

            
            



def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
