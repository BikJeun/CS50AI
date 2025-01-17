import sys
import copy

from crossword import *


class CrosswordCreator:
    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy() for var in self.crossword.variables
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
            (self.crossword.width * cell_size, self.crossword.height * cell_size),
            "black",
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border, i * cell_size + cell_border),
                    (
                        (j + 1) * cell_size - cell_border,
                        (i + 1) * cell_size - cell_border,
                    ),
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (
                                rect[0][0] + ((interior_size - w) / 2),
                                rect[0][1] + ((interior_size - h) / 2) - 10,
                            ),
                            letters[i][j],
                            fill="black",
                            font=font,
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
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        copySelf = copy.deepcopy(self)
        for v in copySelf.domains:
            for value in copySelf.domains[v]:
                if len(value) != v.length:
                    self.domains[v].remove(value)
        # print("1")

        # print(self.domains)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        overlap = self.crossword.overlaps[x, y]
        if overlap:
            i, j = overlap
            toRemove = set()
            for values in self.domains[x]:
                satisfies = False
                for yValues in self.domains[y]:
                    if values != yValues and values[i] == yValues[j]:
                        satisfies = True
                        break
                if not satisfies:
                    toRemove.add(values)

                if toRemove:
                    revised = True
                    for variable in toRemove:
                        self.domains[x].remove(variable)

                return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if not arcs:
            queue = []
            for var1 in self.crossword.variables:
                for var2 in self.crossword.neighbors(var1):
                    queue.append((var1, var2))
        else:
            queue = list(arcs)

        while queue:
            x, y = queue.pop()
            setY = set()
            setY.add(y)

            if self.revise(x, y):
                if self.domains[x] == 0:
                    return False
                for z in self.crossword.neighbors(x) - setY:
                    queue.append((z, x))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.crossword.variables:
            if var not in assignment.keys():
                return False
            if assignment[var] not in self.crossword.words:
                return False

        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for i in assignment:
            value = assignment[i]
            if i.length != len(value):
                return False

            for j in assignment:
                words = assignment[j]
                if i != j:
                    if value == words:
                        return False

                    overlap = self.crossword.overlaps[i, j]
                    if overlap:
                        x, y = overlap
                        if value[x] != words[y]:
                            return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        neighbour = self.crossword.neighbors(var)
        for i in assignment:
            if i in neighbour:
                neighbour.remove(i)

        result = []
        for value in self.domains[var]:
            toRemove = 0
            for neighbourKey in neighbour:
                for neighbourValue in self.domains[neighbourKey]:
                    overlap = self.crossword.overlaps[var, neighbourKey]
                    if overlap:
                        x, y = overlap
                        if value[x] != neighbourValue[y]:
                            toRemove += 1
            result.append([value, toRemove])
        # print("order domain values results: ")
        # print(result)
        result.sort(key=lambda x: x[1])
        return [value[0] for value in result]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        variables = []
        for var in self.crossword.variables:
            if var not in assignment:
                variables.append(
                    [var, len(self.domains[var]), len(self.crossword.neighbors(var))]
                )
        if variables:
            variables.sort(key=lambda x: (x[1], -x[2]))
            return variables[0][0]

        return None

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
            copyAssign = assignment.copy()
            copyAssign[var] = value
            if self.consistent(copyAssign):
                result = self.backtrack(copyAssign)
                if result:
                    return result

        return None


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
    # print(creator.domains)
    # for v in creator.domains:
    #     print(v.length)
    #     print("values: ")
    #     print(v.items())
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
