import sys
from sudoku import Sudoku

class SudokuSolver:
    
    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.domains = {
            group: list(range(10))
            for group in self.sudoku.groups
        }

    def solve(self, ):
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())
    
    def enforce_node_consistency(self):
        """
        Enforce UNARY constraints. The unary constraints in this 
        problem is the rule to not repeat any number within a group.

        """
        raise NotImplementedError

    def revise(self, x, y):
        raise NotImplementedError

    def ac3(self, arcs=None):
        raise NotImplementedError
    
    def assignment_complete(self, assignment):
        raise NotImplementedError

    def consistent(self, assigment):
        raise NotImplementedError
    
    def order_domain_values(self, var, assignment):
        raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        raise NotImplementedError

    
    def backtrack(assignment):
        raise NotImplementedError

def main():

    # Check usage
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python solve.py structure [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) == 3 else None

    # Generate sudoku
    sudoku = Sudoku(structure)
    solver = SudokuSolver(sudoku)
    assignment = solver.solve()

    # Print result
    # if assignment is None:
    #     print("No solution.")
    # else:
    #     creator.print(assignment)
    if output:
        sudoku.save(output)


if __name__ == "__main__":
    main()
