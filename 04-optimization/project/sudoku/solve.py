import sys
from sudoku import Sudoku, Variable, Row, Column, Box
from datetime import datetime

class SudokuSolver:
    
    def __init__(self, sudoku):
        self.sudoku = sudoku


        self.domains = {
            var: set(range(1, 10))
            for var in self.sudoku.variables
        }

        self.group_domains = {
            group: set(range(1, 10))
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
        # Apply unary constraint on each group
        groups = self.group_domains.keys()

        for g in groups:
            domain = self.group_domains[g].copy()
            for number in self.group_domains[g]:
                # if the number in the domain is already within the group's values
                if number in g.values:
                    domain.remove(number)
            # overwrite domain
            self.group_domains[g] = domain

            # update restriction for each cell in that group
            # if that cell is not yet given
            for i, j in g.cells:
                var = Variable(i,j)
                if var in self.sudoku.variables: 
                    self.domains[var] = set(self.domains[var]).intersection(set(domain))


    def revise(self, x, y):
        """
        x and y are Variable's
        """
        return False

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each group is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Apply the binary constraints, which refers to inter-groups constraints.
        
        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        
        return True
    
    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        sudoku variable); return False otherwise.
        """
        incomplete_check = []
        variables = set(self.domains.keys())
        for var in variables:
            # if there are any variable not assigned, not complete
            incomplete_check.append(var not in assignment.keys())


            # if no value is assigned even though the var is there, not complete
            incomplete_check.append(not assignment.get(var))
        
        # if any of these incomplete_check results in a True statement
        fl_incomplete = any(incomplete_check)
        if fl_incomplete:
            return False
        
        # totally complete only if complete and consistent, 
        # but consistency check may be expensive
        return not fl_incomplete and self.consistent(assignment)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., if no rule was broken)
        Return False otherwise.
        """
        variables = set(assignment.keys())
        # timestamp = datetime.now().strftime('%H%M%S%ff')
        # self.sudoku.save(f'testing/output_{timestamp}.png', assignment)

        for v in variables:
            
            assigned_value = assignment[v]
            # if assigned_value already in some of the cell's group neighbors, 
            # then not consistent
            for n in v.groups:
                if assigned_value in n.values:
                    if n.values.count(assigned_value) > 1:
                        return False
        return True
    
    def order_domain_values(self, var, assignment):
        """TODO: optimize"""
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
        sorted_domain = sorted(self.domains.items(), key = lambda x : len(x[1]))
        for each_var, _ in sorted_domain:
            if each_var in unassigned_variables:
                return each_var

        return set()

    
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        puzzle and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to int (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            self.update(var, assignment)
            # TODO: you can enforce node consistency after each update for all var`s neighbors
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result:
                    return result
            
            assignment[var] = None
            assignment.pop(var)
            self.rollback(var)

    def update(self, var, assignment):
        value = assignment[var]
        for n in self.sudoku.neighbors(var):
            if isinstance(n, Row):
                k = var.j
            elif isinstance(n, Column):
                k = var.i
            else: # isinstance(n, Box)
                k = ((var.i - n.i) * 3) + (var.j - n.j)

            n.values[k] = value

        var.value = value
    
    def rollback(self, var):
        for n in self.sudoku.neighbors(var):
            if isinstance(n, Row):
                k = var.j
            elif isinstance(n, Column):
                k = var.i
            else: # isinstance(n, Box)
                k = ((var.i - n.i) * 3) + (var.j - n.j)

            n.values[k] = None
        
        var.value = None
                
        
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
    if assignment is None:
        print("No solution.")
    else:
        print('assignment:', assignment)
    if output:
        sudoku.save(output, assignment)


if __name__ == "__main__":
    main()
