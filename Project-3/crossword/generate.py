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
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
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
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for v in self.domains:
            remove_w = set()
            for w in self.domains[v]:
                if len(w) != v.length:
                    remove_w.add(w)
            for w in remove_w:
                self.domains[v].remove(w)

    def revise(self, x, y):
        """
        Make variable x arc consistent with variable y.
        Remove values from domain of x that are inconsistent with y.

        Return True if a revision was made; False otherwise.
        """
        revised = False
        overlap = self.crossword.overlaps.get((x, y))
        if overlap is None:
            return False

        i, j = overlap
        to_remove = set()

        for word_x in self.domains[x]:
            match_found = False
            for word_y in self.domains[y]:
                if word_x[i] == word_y[j]:
                    match_found = True
                    break
            if not match_found:
                to_remove.add(word_x)

        if to_remove:
            self.domains[x] -= to_remove
            revised = True

        return revised

    def ac3(self, arcs=None):
        """
        Update self.domains such that each variable is arc consistent.
        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            queue = [(x, y) for x in self.crossword.variables for y in self.crossword.neighbors(x)]
        else:
            queue = list(arcs)

        while queue:
            x, y = queue.pop(0)
            if self.revise(x, y):
                if not self.domains[x]:
                    return False
                for z in self.crossword.neighbors(x) - {y}:
                    queue.append((z, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete:
        - Each variable in the crossword has a word assigned.
        - No variable is left unassigned.
        Otherwise, return False.
        """
        # Loop through all variables in the crossword
        for var in self.crossword.variables:
            # Check if the variable is missing from assignment or has no value
            if var not in assignment or assignment[var] is None:
                return False

        # All variables are assigned a value
        return True

    def consistent(self, assignment):
        # Check for correct word lengths and no duplicate words
        words = set()
        for var, word in assignment.items():
            if len(word) != var.length:
                return False
            if word in words:
                return False
            words.add(word)

        # Check for conflicts at overlaps
        for var1 in assignment:
            word1 = assignment[var1]
            for var2 in self.crossword.neighbors(var1):
                if var2 in assignment:
                    word2 = assignment[var2]
                    overlap = self.crossword.overlaps.get((var1, var2))
                    if overlap:
                        i, j = overlap
                        if word1[i] != word2[j]:
                            return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        conflict_dict = dict()

        for word in self.domains[var]:
            conflict = 0
            for n in self.crossword.neighbors(var):
                if n in assignment:
                    continue  # Skip already assigned neighbors
                overlap = self.crossword.overlaps.get((var, n))
                if overlap is None:
                    continue
                i, j = overlap
                for neighbor_word in self.domains[n]:
                    if word[i] != neighbor_word[j]:
                        conflict += 1
            conflict_dict[word] = conflict

        # Sort by increasing conflict
        sorted_words = sorted(conflict_dict, key=lambda w: conflict_dict[w])
        return sorted_words

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Step 1: Get list of unassigned variables
        unassigned_vars = [v for v in self.crossword.variables if v not in assignment]

        # Step 2: Apply MRV (Minimum Remaining Values) and Degree Heuristic
        def mrv_then_degree(var):
            # MRV: number of values left in the domain (smaller is better)
            mrv = len(self.domains[var])
            # Degree: number of neighbors that are unassigned (higher is better)
            degree = len([n for n in self.crossword.neighbors(var) if n not in assignment])
            return (mrv, -degree)  # we sort ascending on mrv, descending on degree

        # Step 3: Return the variable with best priority
        return min(unassigned_vars, key=mrv_then_degree)

    def backtrack(self, assignment):
        # If assignment is complete, return it
        if self.assignment_complete(assignment):
            return assignment

        # Select an unassigned variable
        var = self.select_unassigned_variable(assignment)

        # Iterate through ordered domain values
        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value

            # Check consistency
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result

        # If no assignment is possible, return None (not an empty dict!)
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
