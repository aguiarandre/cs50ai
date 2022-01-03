import sys
from sudoku import Sudoku, Variable, Row, Column, Box
from datetime import datetime

class SudokuSolver:
    
    def __init__(self, sudoku):
        self.sudoku = sudoku
        # domains is a map from Variable to List[int]
        # and refers to the possible values a single cell may have
        self.domains = {
            var: set(range(1, 10))
            for var in self.sudoku.variables
        }

        # domains is a map from an instance of a Group to List[int]
        # and refers to the possible values an entire group may have,
        # be it a Row, a Column or a Box.
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
        problem are simply the rules of the game: 
            Numbers within a group may not be repeated.

        The strategy here is:
            For every group (Row, Column and Box), remove from its domain 
            any value that does not satisfy the constraint, i.e., any value 
            in the domain that is already in the values attribute of the group.

            After each group has its constraints satisfied, run every cell in that 
            group and propagate the Group domain to the Variable domain.
            As a cell may be selected three times (for a Row group, a Column and a Box)
            we gather the intersection of the domains to be the final domain.
        """
        # Apply unary constraint on each and every group
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


    def revise(self, v1, v2):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        
        # I have a variable Variable(i,j)
        # I run through its domain, say [4,6]
        # I need to check whether 4 is possible anywhere within v's neighbors cells
        domain = self.domains[v1].copy()
        for d in domain:
            fl_possible = False
            # check if d may or may not be assigned to this cell
            if not v2.groups:
                return False

            for g in v2.groups:
                if d not in g.values:
                    # if anytime d falls here, it means
                    # this value in the domain is possible
                    fl_possible = True
                    continue
            # after checking all groups, see if possible
            if any(fl_possible):
                # no revision is needed if possible
                continue
            else:
                # remove this value from the domain
                self.domains[v1].remove(d)
            
        if len(domain) != len(self.domains[v1]):
            # it means a revision was made
            return True

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

        if not arcs:
            variables = set(self.domains.keys())
            arcs = []
            for v1 in variables:
                for v2 in self.sudoku.neighboring_variables(v1):
                    arcs.append((v1, v2))
        else:
            pass
        
        while len(arcs) > 0:
            v1, v2 = arcs.pop()

            if self.revise(v1, v2):
                if not self.domains[v1]:
                    # there's no way to solve this problem
                    return False
                for vn in (self.sudoku.neighboring_variables(v1) - {v2}):
                    # if we've modified v1's domain, there might 
                    # be some other (vn, v1) that was arc-consistent, but 
                    # now is not anymore. 
                    arcs.append((vn, v1))

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
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        TODO: for now, it is simply returning the domain 
        """
        return self.domains[var]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. 
        TODO: If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        assigned_variables = set(assignment.keys())
        all_variables = set(self.domains.keys())
        unassigned_variables = all_variables - assigned_variables

        # give preference for variables whose domain is small.
        sorted_domain = sorted(self.domains.items(), key = lambda x : len(x[1]))
        
        for each_var, _ in sorted_domain:
            if each_var in unassigned_variables:
                return each_var
        
        # if no more variables are found within the domain, return the empty set
        return set()

    def inferences(self, assignment):
        """
        After assigning a new value to a variable, you can apply 
        some new constraints to help optimize the problem.
        TODO
        """
        pass

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
            # try this value
            assignment[var] = value
            self.update(var, assignment)

            now = datetime.now().strftime('%H%M%S%f')
            filename = f'media/1/output_{now}.png'
            self.sudoku.save(filename, assignment)
            
            # TODO: include inferences after selecting a variable 
            if self.consistent(assignment):
                
                inferences = self.inferences(assignment)
                if inferences:
                    # TODO: add inferences to assignment
                    pass

                # after checking consistency, keep testing down the tree
                result = self.backtrack(assignment)
                if result:
                    # if a result is found, go ahead and output it.
                    return result
            
            # however, if we end up in a inconsistent non-result,
            # we have to rollback our assumptions, i.e., remove 
            # values from our assignment, from our cells, from our 
            # groups and from any inferences 
            # TODO: remove inferences from assignment
            assignment[var] = None
            assignment.pop(var)
            self.rollback(var)
            
    def update(self, var, assignment):
        """
        Get the assigned value and update both its neighboring groups
        and the variable.
        """
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
        """
        Exclude any information from the variable, so we can backtrack again.
        """
        for n in self.sudoku.neighbors(var):
            if isinstance(n, Row):
                k = var.j
            elif isinstance(n, Column):
                k = var.i
            else: # isinstance(n, Box)
                k = ((var.i - n.i) * 3) + (var.j - n.j)
            n.values[k] = None
        var.value = None
                
    def print(self, assignment=None):
        letters = self.sudoku.contents
        for i in range(self.sudoku.height):
            for j in range(self.sudoku.width):
                if letters[i][j] != "#":
                    print(letters[i][j], end='')
                else:
                    for var in assignment.keys():
                        if var.i == i and var.j == j:
                            print(assignment.get(var, 'x'), end='')
            print()

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
        solver.print(assignment)
    if output:
        sudoku.save(output, assignment)


if __name__ == "__main__":
    main()
