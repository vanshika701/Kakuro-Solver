from csp import *
import sys
import time

# difficulty 0
kakuro1 = [['*', '*', '*', [6, ''], [3, '']],
           ['*', [4, ''], [3, 3], '_', '_'],
           [['', 10], '_', '_', '_', '_'],
           [['', 3], '_', '_', '*', '*']]

# difficulty 0
kakuro2 = [
    ['*', [10, ''], [13, ''], '*'],
    [['', 3], '_', '_', [13, '']],
    [['', 12], '_', '_', '_'],
    [['', 21], '_', '_', '_']]

# difficulty 1
kakuro3 = [
    ['*', [17, ''], [28, ''], '*', [42, ''], [22, '']],
    [['', 9], '_', '_', [31, 14], '_', '_'],
    [['', 20], '_', '_', '_', '_', '_'],
    ['*', ['', 30], '_', '_', '_', '_'],
    ['*', [22, 24], '_', '_', '_', '*'],
    [['', 25], '_', '_', '_', '_', [11, '']],
    [['', 20], '_', '_', '_', '_', '_'],
    [['', 14], '_', '_', ['', 17], '_', '_']]

# difficulty 2
kakuro4 = [
    ['*', '*', '*', '*', '*', [4, ''], [24, ''], [11, ''],
        '*', '*', '*', [11, ''], [17, ''], '*', '*'],
    ['*', '*', '*', [17, ''], [11, 12], '_', '_', '_',
        '*', '*', [24, 10], '_', '_', [11, ''], '*'],
    ['*', [4, ''], [16, 26], '_', '_', '_', '_', '_',
        '*', ['', 20], '_', '_', '_', '_', [16, '']],
    [['', 20], '_', '_', '_', '_', [24, 13], '_', '_', [
        16, ''], ['', 12], '_', '_', [23, 10], '_', '_'],
    [['', 10], '_', '_', [24, 12], '_', '_', [16, 5],
        '_', '_', [16, 30], '_', '_', '_', '_', '_'],
    ['*', '*', [3, 26], '_', '_', '_', '_', ['', 12],
        '_', '_', [4, ''], [16, 14], '_', '_', '*'],
    ['*', ['', 8], '_', '_', ['', 15], '_', '_',
        [34, 26], '_', '_', '_', '_', '_', '*', '*'],
    ['*', ['', 11], '_', '_', [3, ''], [17, ''], ['', 14],
        '_', '_', ['', 8], '_', '_', [7, ''], [17, ''], '*'],
    ['*', '*', '*', [23, 10], '_', '_', [3, 9], '_',
        '_', [4, ''], [23, ''], ['', 13], '_', '_', '*'],
    ['*', '*', [10, 26], '_', '_', '_', '_', '_',
        ['', 7], '_', '_', [30, 9], '_', '_', '*'],
    ['*', [17, 11], '_', '_', [11, ''], [24, 8], '_', '_',
        [11, 21], '_', '_', '_', '_', [16, ''], [17, '']],
    [['', 29], '_', '_', '_', '_', '_', ['', 7], '_',
        '_', [23, 14], '_', '_', [3, 17], '_', '_'],
    [['', 10], '_', '_', [3, 10], '_', '_', '*',
        ['', 8], '_', '_', [4, 25], '_', '_', '_', '_'],
    ['*', ['', 16], '_', '_', '_', '_', '*',
        ['', 23], '_', '_', '_', '_', '_', '*', '*'],
    ['*', '*', ['', 6], '_', '_', '*', '*', ['', 15], '_', '_', '_', '*', '*', '*', '*']]


class MyKakuro(CSP):

    def __init__(self, puzzle):
        variables = []
        for i, line in enumerate(puzzle):
            for j, element in enumerate(line):
                if element == '_':
                    var1 = str(i)
                    if len(var1) == 1:
                        var1 = "0" + var1
                    var2 = str(j)
                    if len(var2) == 1:
                        var2 = "0" + var2
                    variables.append("X" + var1 + var2)

        domains = {}
        for var in variables:
            domains[var] = set(range(1, 10))

        self.sums = []

        for i, line in enumerate(puzzle):
            for j, element in enumerate(line):
                if element != '_' and element != '*':
                    # down - column
                    if element[0] != '':
                        x = []
                        for k in range(i + 1, len(puzzle)):
                            if puzzle[k][j] != '_':
                                break
                            var1 = str(k)
                            if len(var1) == 1:
                                var1 = "0" + var1
                            var2 = str(j)
                            if len(var2) == 1:
                                var2 = "0" + var2
                            x.append("X" + var1 + var2)
                        self.sums.append((element[0], x))
                    # right - line
                    if element[1] != '':
                        x = []
                        for k in range(j + 1, len(puzzle[i])):
                            if puzzle[i][k] != '_':
                                break
                            var1 = str(i)
                            if len(var1) == 1:
                                var1 = "0" + var1
                            var2 = str(k)
                            if len(var2) == 1:
                                var2 = "0" + var2
                            x.append("X" + var1 + var2)
                        self.sums.append((element[1], x))

        neighbors = {}
        for v in variables:
            neighbors[v] = []
            for s in self.sums:
                if v in s[1]:
                    neighbors[v] += s[1]
                    neighbors[v].remove(v)

        CSP.__init__(self, variables, domains,
                     neighbors, self.KakuroConstraints)

        self.puzzle = puzzle

    def KakuroConstraints(self, A, a, B, b):
        # Check if a and b are different
        diff = different_values_constraint(A, a, B, b)
        if diff == False:
            return False

        # Check if sums are valid
        numbers_toSum = []
        tempValue = 0

        for s in self.sums:
            variables = s[1]
            wantedResult = s[0]

            if A in variables and B in variables:
                for var in variables:
                    if var == A:
                        numbers_toSum.append(a)
                    elif var == B:
                        numbers_toSum.append(b)
                    else:
                        if self.curr_domains == None or len(self.curr_domains[var]) > 1:
                            tempValue += 1
                        elif len(self.curr_domains[var]) == 1:
                            numbers_toSum.append(*self.curr_domains[var])

                Sum = sum(numbers_toSum)

                if tempValue == 0:
                    if Sum == wantedResult:
                        return True
                    else:
                        return False
                else:
                    if Sum <= wantedResult:
                        return True
                    else:
                        return False
        
        return True

    def display(self, assignment=None):
        for i, line in enumerate(self.puzzle):
            puzzle = ""
            for j, element in enumerate(line):
                if element == '*':
                    puzzle += "[*]\t"
                elif element == '_':
                    var1 = str(i)
                    if len(var1) == 1:
                        var1 = "0" + var1
                    var2 = str(j)
                    if len(var2) == 1:
                        var2 = "0" + var2
                    var = "X" + var1 + var2
                    if assignment is not None:
                        if isinstance(assignment[var], set) and len(assignment[var]) is 1:
                            puzzle += "[" + str(first(assignment[var])) + "]\t"
                        elif isinstance(assignment[var], int):
                            puzzle += "[" + str(assignment[var]) + "]\t"
                        else:
                            puzzle += "[_]\t"
                    else:
                        puzzle += "[_]\t"
                else:
                    puzzle += str(element[0]) + "\\" + str(element[1]) + "\t"
            print(puzzle)


# Optimized MRV + Degree heuristic
def mrv_degree(assignment, csp):
    """
    Most optimized variable selection heuristic.
    Combines Minimum Remaining Values (MRV) with Degree heuristic as tiebreaker.
    """
    unassigned = [v for v in csp.variables if v not in assignment]
    
    def heuristic_value(var):
        # Get domain size (MRV)
        if csp.curr_domains:
            domain_len = len(csp.curr_domains[var])
        else:
            domain_len = num_legal_values(csp, var, assignment)
        
        # Get degree (number of unassigned neighbors)
        degree = sum(1 for neighbor in csp.neighbors[var] if neighbor not in assignment)
        
        # Return tuple: prioritize smallest domain, then highest degree
        return (domain_len, -degree)
    
    return min(unassigned, key=heuristic_value)


# Main execution
if __name__ == "__main__":
    print("=" * 60)
    print("KAKURO SOLVER - Optimized Algorithm")
    print("=" * 60)
    print()
    
    difficulty = input("Select difficulty (0, 1, 2, 3): ")
    print()
    
    if difficulty == "0":
        k = MyKakuro(kakuro1)
    elif difficulty == "1":
        k = MyKakuro(kakuro2)
    elif difficulty == "2":
        k = MyKakuro(kakuro3)
    elif difficulty == "3":
        k = MyKakuro(kakuro4)
    else:
        print("Input must be an integer between 0 and 3")
        sys.exit(1)
    
    print("-> Kakuro game (initial)")
    k.display()
    print()
    print("____________ Optimized Backtracking (MRV+Degree + MAC + LCV) ________________")
    print()
    
    startOfAlgorithm = float(round(time.time()*1000))
    result = backtracking_search(k, 
                                 select_unassigned_variable=mrv_degree, 
                                 order_domain_values=lcv, 
                                 inference=mac)
    endOfAlgorithm = float(round(time.time()*1000))
    
    print()
    if result:
        k.display(k.infer_assignment())
    else:
        print("No solution found!")
    
    print("EXECUTION-TIME: %.2f ms" % (endOfAlgorithm-startOfAlgorithm))
    print("ASSIGNMENTS: ", k.nassigns)