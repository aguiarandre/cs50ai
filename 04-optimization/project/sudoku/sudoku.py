from typing import List 
from collections import defaultdict


class Variable:
    def __init__(self, i, j, value=None):
        self.i = i
        self.j = j
        self.cells = [(i, j)]
        self.value = value
        self.groups = None

    def __str__(self):
        return f"({self.i}, {self.j}): {self.value}"

    def __repr__(self):
       return f"Variable({self.i}, {self.j}): {self.value}"

    def __hash__(self):
        return hash((self.i, self.j, str(self.cells)))
    
    def __eq__(self, other):
        return (
            (self.i == other.i) and
            (self.j == other.j) and
            (self.cells == other.cells) and
            (self.value == other.value)
        )
    
    def __gt__(self, other):
        result = (
            (self.i >= other.i) 
        )
        if self.i == other.i:
            result = (
                (self.j >= other.j)
            )
        return result
        
class Group:
    def __init__(self, i: int, j: int, values: List):
        # starting point
        self.i = i
        self.j = j
        # None means not found yet
        self.values = values
        self.cells = []
        
    def __hash__(self):
        return hash((self.i, self.j, str(self.cells)))
    
    def __eq__(self, other):
        return (
            (self.i == other.i) and
            (self.j == other.j) and
            (self.cells == other.cells) 
        )
        
class Row(Group):
    def __init__(self, i: int, j: int, values: List):
        super().__init__(i, j, values)
        for k in range(len(values)):
            self.cells.append(
                (i, j + k)
            )

    def __str__(self):
        return f"({self.i}): {[(str(val) if val else '_') for val in self.values]}"

    def __repr__(self):
        return f"Row({self.i}, {self.j}, {[val for val in self.values]}, {[val for val in self.cells]})"

class Column(Group):
    def __init__(self, i: int, j: int, values: List):
        super().__init__(i, j, values)
        for k in range(len(values)):
            self.cells.append(
                (i + k, j)
            )

    def __str__(self):
        nl = '\n'
        return f"({self.j}):\n{nl.join([(str(val) if val else '_') for val in self.values])}"

    def __repr__(self):
        return f"Column({self.i}, {self.j}, {[val for val in self.values]}, {[val for val in self.cells]})"

class Box(Group):

    def __init__(self, i: int, j: int, values: List):
        super().__init__(i, j, values)
        starting_i = i
        starting_j = j

        for row in range(i, i + 3):
            for col in range(j, j + 3):
                self.cells.append(
                    (row, col)
                )

    def __str__(self):
        s = ''

        for index, val in enumerate(self.values):
            if not val:
                val = '_'
            if (index+1) % 3 == 0 and index != 0:
                val = str(val) + '\n'
            s += str(val)

        return f"({self.i}, {self.j}):\n{s}"

    def __repr__(self):
        return f"Box({self.i}, {self.j}, {[val for val in self.values]}, {[val for val in self.cells]})"

class Sudoku:

    def __init__(self, structure_file):
        
        self.groups = []
        
        # Determine structure of crossword
        with open(structure_file) as f:
            contents = f.read().splitlines()
            self.contents = contents
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        if self.height != self.width:
            raise ValueError('Sudoku structure is not square')
        
        # Create data structures to store information from the puzzle
        # Row data:
        for i, row in enumerate(contents):
            values = [(int(symbol) if symbol != '#' else None) for symbol in row]
            self.groups.append(Row(i, 0, values))

        # Column data:
        for j in range(self.width):
            values = []
            for row in contents:
                values.append(int(row[j]) if row[j] != '#' else None)
            self.groups.append(Column(0, j, values))

        # Box data:
        row_counter = 0
        for box_number in range(self.height):
            values = []
            if (box_number % 3) == 0 and box_number !=0:
                row_counter += 1
            
            box_row = box_number // 3
            box_column = box_number % 3

            for i in range(3 * row_counter, 3 * (row_counter + 1)):
                for j in range(3 * box_column, 3 * (box_column + 1)):
                    values.append(int(contents[i][j]) if contents[i][j] != '#' else None)

            self.groups.append(Box(box_row * 3, box_column * 3, values))

        # compute variables:
        self.variables = set()
        for i, row in enumerate(contents):
            for j, value in enumerate(row):
                if value == '#':
                    # givens are not needed
                    self.variables.add(Variable(i, j))

        # store the group variables in its .groups attribute
        self.compute_overlaps()
        
    def compute_overlaps(self, ):
        self.overlaps = dict()
        for v in self.variables:
            cells1 = v.cells

            for g in self.groups:
                cells2 = g.cells
                intersections = set(cells1).intersection(cells2)
                
                if not intersections:
                        self.overlaps[v, g] = None
                else:
                    intersection = intersections.pop()
                    self.overlaps[v, g] = (
                        cells1.index(intersection), 
                        cells2.index(intersection)
                    )
            v.groups = self.neighbors(v)



    def compute_group_overlaps(self, ):
        ''' 
        Compute a dict whose values are lists of overlaps within groups.

        For each pair (group1, group2), one can find overlaps by acessing
        self.overlaps[group1, group2]. The result will be a list containing 
        tuples. Each tuple represents the position in self.cells of group1
        and group2 where the overlap is located. 
        For example:
        If a group1 Row is located in positions:
        [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8)]
        and a group2 Box is located in positions:
        [(0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 8), (2, 6), (2, 7), (2, 8)]
        Their overlaps are located at:
        [(6, 0), (8, 2), (7, 1)]
        That is, for the 6th cell on group1 and 0th cell in group2 (this refers to (0,6)).
        Another overlap is the 8th cell in group 1 and 2nd cell in group2 (this refers to (0,8)) 
        and same rationale for the 7th item on group1 and 1st item in group2 (0,7).
        '''    
        self.group_overlaps = defaultdict(lambda: [])
        for g1 in self.groups:
            for g2 in self.groups:
                if g1 == g2:
                    continue
                cells1 = g1.cells
                cells2 = g2.cells
                intersections = set(cells1).intersection(cells2)
                
                if not intersections:
                    self.group_overlaps[g1, g2] = None
                else:
                    while len(intersections):
                        intersection = intersections.pop()
                        self.group_overlaps[g1, g2].append(
                            (cells1.index(intersection),
                             cells2.index(intersection))
                        )

    def group_neighbors(self, group):
        """Given a group, return set of overlapping groups."""
        return set(
            g for g in self.groups
            if g != group and self.group_overlaps[g, group]
        )
    
    def neighbors(self, var):
        """Given a variable, return set of its overlapping groups."""
        result = set()
        for g in self.groups:
            if self.overlaps.get((var, g), None):
                result.add(g)
        return result
    
    def neighboring_variables(self, var):
        """
        Given a variable, get the set of all cells that it is related to. 
        Meaning all cells from neighboring groups.
        """
        groups_related = var.groups
        cells_related = set()
        for g in groups_related:
            for i, j in g.cells:
                cells_related.add(Variable(i, j))

        return cells_related

    def save(self, filename, assigment=None):
        """
        Save sudoku to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        cell_border_strong = 9
        interior_size = cell_size - 2 * cell_border
        letters = self.contents

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size,
             self.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.height):
            for j in range(self.width):
                # generate bold lines for box divisions
                cell_border_row = cell_border_strong if (i % 3) == 0 and i else cell_border
                cell_border_col = cell_border_strong if (j % 3) == 0 and j else cell_border
                
                rect = [
                    (j * cell_size + cell_border_col,
                     i * cell_size + cell_border_row),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                draw.rectangle(rect, fill="white")
                if letters[i][j] != '#':
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        if assigment:
            for var in assigment.keys():
                i, j = var.i, var.j
                solution = str(var.value)
                # generate bold lines for box divisions
                cell_border_row = cell_border_strong if (i % 3) == 0 and i else cell_border
                cell_border_col = cell_border_strong if (j % 3) == 0 and j else cell_border
                
                rect = [
                    (j * cell_size + cell_border_col,
                     i * cell_size + cell_border_row),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                draw.rectangle(rect, fill="white")

                w, h = draw.textsize(solution, font=font)
                draw.text(
                    (rect[0][0] + ((interior_size - w) / 2),
                        rect[0][1] + ((interior_size - h) / 2) - 10),
                    solution, fill="red", font=font
                )

        img.save(filename)