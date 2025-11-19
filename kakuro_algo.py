from csp import *
import sys
import time
import random
from itertools import combinations

# Original hardcoded puzzles (kept for reference)
kakuro1 = [['*', '*', '*', [6, ''], [3, '']],
           ['*', [4, ''], [3, 3], '_', '_'],
           [['', 10], '_', '_', '_', '_'],
           [['', 3], '_', '_', '*', '*']]

kakuro2 = [
    ['*', [10, ''], [13, ''], '*'],
    [['', 3], '_', '_', [13, '']],
    [['', 12], '_', '_', '_'],
    [['', 21], '_', '_', '_']]

kakuro3 = [
    ['*', [17, ''], [28, ''], '*', [42, ''], [22, '']],
    [['', 9], '_', '_', [31, 14], '_', '_'],
    [['', 20], '_', '_', '_', '_', '_'],
    ['*', ['', 30], '_', '_', '_', '_'],
    ['*', [22, 24], '_', '_', '_', '*'],
    [['', 25], '_', '_', '_', '_', [11, '']],
    [['', 20], '_', '_', '_', '_', '_'],
    [['', 14], '_', '_', ['', 17], '_', '_']]

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


class KakuroGenerator:
    """Generate Kakuro puzzles with guaranteed solutions"""
    
    def __init__(self, rows=5, cols=5, density=0.6):
        self.rows = rows
        self.cols = cols
        self.density = density
        self.grid = None
        self.solution = None
        
    def generate(self):
        """Generate a new Kakuro puzzle"""
        max_attempts = 50
        for attempt in range(max_attempts):
            if self._try_generate():
                return self.grid
        
        print(f"Warning: Could not generate puzzle after {max_attempts} attempts. Using simpler layout.")
        return self._generate_simple_puzzle()
    
    def _try_generate(self):
        """Try to generate a valid puzzle"""
        self._create_grid_structure()
        
        if not self._fill_grid():
            return False
        
        self._create_puzzle_with_clues()
        return True
    
    def _create_grid_structure(self):
        """Create the structure of black and white cells, ensuring runs have minimum length 2"""
        self.grid = [['*' for _ in range(self.cols)] for _ in range(self.rows)]
        self.solution = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        
        target_white = int(self.rows * self.cols * self.density)
        white_count = 0
        
        for i in range(1, self.rows):
            for j in range(1, self.cols):
                if random.random() < 0.7 and white_count < target_white:
                    
                    # Horizontal run attempt
                    if random.random() < 0.5:
                        max_h_len = self.cols - j
                        if max_h_len >= 2:
                            length = random.randint(2, min(4, max_h_len))
                            for k in range(length):
                                if j + k < self.cols and white_count < target_white:
                                    self.grid[i][j + k] = '_'
                                    white_count += 1
                    
                    # Vertical run attempt
                    else:
                        max_v_len = self.rows - i
                        if max_v_len >= 2:
                            length = random.randint(2, min(4, max_v_len))
                            for k in range(length):
                                if i + k < self.rows and white_count < target_white:
                                    self.grid[i + k][j] = '_'
                                    white_count += 1
    
    def _fill_grid(self):
        """Fill the grid with valid numbers using backtracking"""
        white_cells = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == '_':
                    white_cells.append((i, j))
        
        runs = self._get_all_runs()
        
        if not runs:
            return False
        
        return self._backtrack_fill(white_cells, runs, 0)
    
    def _backtrack_fill(self, white_cells, runs, index):
        """Backtracking algorithm to fill grid with valid values"""
        if index >= len(white_cells):
            return True
        
        i, j = white_cells[index]
        digits = list(range(1, 10))
        random.shuffle(digits)
        
        for digit in digits:
            if self._is_valid_placement(i, j, digit, runs):
                self.solution[i][j] = digit
                
                if self._backtrack_fill(white_cells, runs, index + 1):
                    return True
                
                self.solution[i][j] = 0
        
        return False
    
    def _is_valid_placement(self, row, col, digit, runs):
        """Check if placing digit at (row, col) is valid"""
        for run_cells in runs:
            if (row, col) in run_cells:
                for r, c in run_cells:
                    if (r, c) != (row, col) and self.solution[r][c] == digit:
                        return False
        return True
    
    def _get_all_runs(self):
        """Get all horizontal and vertical runs of white cells"""
        runs = []
        
        # Horizontal runs
        for i in range(self.rows):
            run = []
            for j in range(self.cols):
                if self.grid[i][j] == '_':
                    run.append((i, j))
                else:
                    if len(run) >= 2:
                        runs.append(run)
                    run = []
            if len(run) >= 2:
                runs.append(run)
        
        # Vertical runs
        for j in range(self.cols):
            run = []
            for i in range(self.rows):
                if self.grid[i][j] == '_':
                    run.append((i, j))
                else:
                    if len(run) >= 2:
                        runs.append(run)
                    run = []
            if len(run) >= 2:
                runs.append(run)
        
        return runs
    
    def _create_puzzle_with_clues(self):
        """Create the final puzzle format with clues"""
        puzzle = [['*' for _ in range(self.cols)] for _ in range(self.rows)]
        
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == '_':
                    puzzle[i][j] = '_'
        
        for i in range(self.rows):
            for j in range(self.cols):
                if puzzle[i][j] == '*':
                    down_sum = self._get_down_sum(i, j)
                    right_sum = self._get_right_sum(i, j)
                    
                    if down_sum > 0 or right_sum > 0:
                        puzzle[i][j] = [down_sum if down_sum > 0 else '', 
                                       right_sum if right_sum > 0 else '']
        
        self.grid = puzzle
    
    def _get_down_sum(self, row, col):
        """Get the sum for cells below this position"""
        if row >= self.rows - 1:
            return 0
        
        total = 0
        count = 0
        for i in range(row + 1, self.rows):
            if self.grid[i][col] == '_':
                total += self.solution[i][col]
                count += 1
            else:
                break
        
        return total if count >= 2 else 0
    
    def _get_right_sum(self, row, col):
        """Get the sum for cells to the right of this position"""
        if col >= self.cols - 1:
            return 0
        
        total = 0
        count = 0
        for j in range(col + 1, self.cols):
            if self.grid[row][j] == '_':
                total += self.solution[row][j]
                count += 1
            else:
                break
        
        return total if count >= 2 else 0
    
    def _generate_simple_puzzle(self):
        """Generate a simple fallback puzzle"""
        return [
            ['*', '*', [6, ''], [3, '']],
            ['*', [4, ''], [3, 3], '_', '_'],
            [['', 10], '_', '_', '_', '_'],
            [['', 3], '_', '_', '*', '*']
        ]
    
    def print_puzzle(self):
        """Print the puzzle in a readable format"""
        print("\nGenerated Kakuro Puzzle:")
        print("=" * 50)
        for row in self.grid:
            row_str = ""
            for cell in row:
                if cell == '*':
                    row_str += "[*]\t\t"
                elif cell == '_':
                    row_str += "[_]\t\t"
                else:
                    row_str += f"{cell[0]}\\{cell[1]}\t\t"
            print(row_str)
        print("=" * 50)


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
            if not different_values_constraint(A, a, B, b):
                return False

            for s in self.sums:
                variables = s[1]
                wantedResult = s[0]

                if A in variables and B in variables:
                    
                    numbers_toSum = []
                    tempValue = 0

                    for var in variables:
                        if var == A:
                            numbers_toSum.append(a)
                        elif var == B:
                            numbers_toSum.append(b)
                        else:
                            if self.curr_domains is not None and len(self.curr_domains[var]) == 1:
                                numbers_toSum.append(next(iter(self.curr_domains[var])))
                            else:
                                tempValue += 1 

                    current_Sum = sum(numbers_toSum)

                    if tempValue == 0:
                        if current_Sum != wantedResult:
                            return False
                    else:
                        if current_Sum >= wantedResult: 
                            return False
                            
                        max_possible_sum = current_Sum + sum(range(10 - tempValue, 10))
                        
                        if max_possible_sum < wantedResult:
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
                        if isinstance(assignment[var], set) and len(assignment[var]) == 1:
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


def mrv_degree(assignment, csp):
    """Variable selection using MRV with degree heuristic as tie-breaker."""
    unassigned = [v for v in csp.variables if v not in assignment]
    
    def heuristic_value(var):
        if csp.curr_domains:
            domain_len = len(csp.curr_domains[var])
        else:
            domain_len = num_legal_values(csp, var, assignment)
        
        degree = sum(1 for neighbor in csp.neighbors[var] if neighbor not in assignment)
        
        return (domain_len, -degree)
    
    return min(unassigned, key=heuristic_value)


def verify_solution(kakuro, assignment):
    """Verify if the solution satisfies all Kakuro constraints"""
    all_valid = True
    
    for target_sum, variables in kakuro.sums:
        values = []
        for var in variables:
            if var in assignment:
                val = assignment[var]
                if isinstance(val, set):
                    val = next(iter(val))
                values.append(val)
        
        actual_sum = sum(values)
        if actual_sum != target_sum:
            print(f"✗ Sum constraint violated: {variables}")
            print(f"  Expected sum: {target_sum}, Got: {actual_sum}")
            print(f"  Values: {values}")
            all_valid = False
        
        if len(values) != len(set(values)):
            print(f"✗ Duplicate values in: {variables}")
            print(f"  Values: {values}")
            all_valid = False
    
    return all_valid


def run_algorithm_1(k):
    """Run Algorithm 1: Backtracking + Forward Checking"""
    print("=" * 60)
    print("ALGORITHM 1: Backtracking + Forward Checking")
    print("=" * 60)
    print()
    
    start = float(round(time.time()*1000))
    result = backtracking_search(k, inference=forward_checking)
    end = float(round(time.time()*1000))
    
    print()
    if result:
        k.display(k.infer_assignment())
    else:
        print("No solution found!")
    
    print("EXECUTION-TIME: %.2f ms" % (end-start))
    print("ASSIGNMENTS: ", k.nassigns)
    print()
    
    if result:
        print("-" * 60)
        print("VERIFYING SOLUTION...")
        print("-" * 60)
        assignment = k.infer_assignment()
        is_valid = verify_solution(k, assignment)
        if is_valid:
            print("✓ Solution is CORRECT! All constraints satisfied.")
        else:
            print("✗ Solution has ERRORS! Some constraints violated.")
        print("-" * 60)
    
    return ("Algorithm 1 (Backtracking + FC)", end-start, k.nassigns)


def run_algorithm_2(k):
    """Run Algorithm 2: MRV+Degree + MAC + LCV"""
    print()
    print("=" * 60)
    print("ALGORITHM 2: MRV+Degree + MAC + LCV")
    print("=" * 60)
    print()
    
    start = float(round(time.time()*1000))
    
    result = backtracking_search(k, 
                                 select_unassigned_variable=mrv_degree, 
                                 order_domain_values=lcv, 
                                 inference=mac)
    
    end = float(round(time.time()*1000))
    
    print()
    if result:
        k.display(k.infer_assignment())
    else:
        print("No solution found!")
    
    print("EXECUTION-TIME: %.2f ms" % (end-start))
    print("ASSIGNMENTS: ", k.nassigns)
    print()
    
    if result:
        print("-" * 60)
        print("VERIFYING SOLUTION...")
        print("-" * 60)
        assignment = k.infer_assignment()
        is_valid = verify_solution(k, assignment)
        if is_valid:
            print("✓ Solution is CORRECT! All constraints satisfied.")
        else:
            print("✗ Solution has ERRORS! Some constraints violated.")
        print("-" * 60)
    
    return ("Algorithm 2 (MRV+Degree+MAC+LCV)", end-start, k.nassigns)


# Main execution
if __name__ == "__main__":
    print("=" * 60)
    print("KAKURO SOLVER - ALGORITHM COMPARISON")
    print("=" * 60)
    print()
    
    # Step 1: Choose puzzle source
    print("Select puzzle source:")
    print("1. Hardcoded puzzles (difficulty 0-3)")
    print("2. Generate new puzzle")
    source_choice = input("Enter your choice (1 or 2): ")
    print()
    
    if source_choice == "1":
        # Use hardcoded puzzles
        difficulty = input("Select difficulty (0, 1, 2, 3): ")
        print()
        
        if difficulty == "0":
            puzzle = kakuro1
        elif difficulty == "1":
            puzzle = kakuro2
        elif difficulty == "2":
            puzzle = kakuro3
        elif difficulty == "3":
            puzzle = kakuro4
        else:
            print("Input must be an integer between 0 and 3")
            sys.exit(1)
    
    elif source_choice == "2":
        # Generate new puzzle
        print("Puzzle Generation Options:")
        print("Size options:")
        print("  1. Small (5x5)")
        print("  2. Medium (6x6)")
        print("  3. Large (8x8)")
        print("  4. Custom size")
        
        size_choice = input("Select size (1-4): ")
        
        if size_choice == "1":
            rows, cols, density = 5, 5, 0.5
        elif size_choice == "2":
            rows, cols, density = 6, 6, 0.6
        elif size_choice == "3":
            rows, cols, density = 8, 8, 0.65
        elif size_choice == "4":
            rows = int(input("Enter number of rows (4-10): "))
            cols = int(input("Enter number of columns (4-10): "))
            density = float(input("Enter density (0.4-0.7): "))
        else:
            rows, cols, density = 5, 5, 0.5
        
        print(f"\nGenerating {rows}x{cols} puzzle with density {density}...")
        generator = KakuroGenerator(rows=rows, cols=cols, density=density)
        puzzle = generator.generate()
        generator.print_puzzle()
        print()
    
    else:
        print("Invalid choice. Please run the program again.")
        sys.exit(1)
    
    # Display initial puzzle
    k = MyKakuro(puzzle)
    print("-> Kakuro game (initial)")
    k.display()
    print()
    
    # Step 2: Select algorithm approach
    print("Select which algorithm(s) to run:")
    print("1. Algorithm 1 (Backtracking + Forward Checking)")
    print("2. Algorithm 2 (MRV+Degree + MAC + LCV)")
    print("3. Run Both and Compare")
    algo_choice = input("Enter your choice (1, 2, or 3): ")
    print()
    
    results = []
    
    if algo_choice == "1":
        k1 = MyKakuro(puzzle)
        result1 = run_algorithm_1(k1)
        results.append(result1)
        
    elif algo_choice == "2":
        k2 = MyKakuro(puzzle)
        result2 = run_algorithm_2(k2)
        results.append(result2)
        
    elif algo_choice == "3":
        k1 = MyKakuro(puzzle)
        result1 = run_algorithm_1(k1)
        results.append(result1)
        
        k2 = MyKakuro(puzzle)
        result2 = run_algorithm_2(k2)
        results.append(result2)
        
        print("\n" + "=" * 80)
        print("PERFORMANCE COMPARISON")
        print("=" * 80)
        print(f"{'Algorithm':<45} {'Time (ms)':<15} {'Assignments':<15}")
        print("-" * 80)
        for name, exec_time, assignments in results:
            print(f"{name:<45} {exec_time:<15.2f} {assignments:<15}")
        print("=" * 80)
        
        if len(results) == 2:
            time_algo1 = results[0][1]
            time_algo2 = results[1][1]
            assignments_algo1 = results[0][2]
            assignments_algo2 = results[1][2]

            print()
            print("ANALYSIS FOR THIS RUN:")
            print("-" * 80)

            # Time comparison
            if time_algo2 < time_algo1:
                speedup = time_algo1 / time_algo2
                print(f"⚡ Algorithm 2 was FASTER by {speedup:.2f}x")
            elif time_algo1 < time_algo2:
                speedup = time_algo2 / time_algo1
                print(f"⚡ Algorithm 1 was FASTER by {speedup:.2f}x")
            else:
                print("⚖️  Both algorithms had equal execution time")

            # Assignments comparison
            if assignments_algo2 < assignments_algo1:
                efficiency = ((assignments_algo1 - assignments_algo2) / assignments_algo1) * 100
                print(f"📊 Algorithm 2 used {efficiency:.1f}% FEWER assignments ({assignments_algo2} vs {assignments_algo1})")
            elif assignments_algo1 < assignments_algo2:
                efficiency = ((assignments_algo2 - assignments_algo1) / assignments_algo2) * 100
                print(f"📊 Algorithm 1 used {efficiency:.1f}% FEWER assignments ({assignments_algo1} vs {assignments_algo2})")
            else:
                print("📊 Both algorithms used the same number of assignments")

            print()
            
            print("=" * 80)
        
    else:
        print("Invalid choice. Please run the program again.")
        sys.exit(1)