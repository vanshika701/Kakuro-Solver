"""
Kakuro Puzzle Generator
Generates random Kakuro puzzles of varying sizes and difficulties
"""

import random
from itertools import combinations

class KakuroGenerator:
    """Generate Kakuro puzzles with guaranteed solutions"""
    
    def __init__(self, rows=5, cols=5, density=0.6):
        """
        Initialize generator
        
        Args:
            rows: Number of rows in the grid
            cols: Number of columns in the grid
            density: Ratio of white cells to total cells (0.0 to 1.0)
        """
        self.rows = rows
        self.cols = cols
        self.density = density
        self.grid = None
        self.solution = None
        
    def generate(self):
        """Generate a new Kakuro puzzle"""
        # Keep trying until we get a valid puzzle
        max_attempts = 50
        for attempt in range(max_attempts):
            if self._try_generate():
                return self.grid
        
        # If we couldn't generate, return a simple puzzle
        print(f"Warning: Could not generate puzzle after {max_attempts} attempts. Using simpler layout.")
        return self._generate_simple_puzzle()
    
    def _try_generate(self):
        """Try to generate a valid puzzle"""
        # Step 1: Create grid structure
        self._create_grid_structure()
        
        # Step 2: Fill with valid numbers
        if not self._fill_grid():
            return False
        
        # Step 3: Create the puzzle format with clues
        self._create_puzzle_with_clues()
        
        return True
    
    def _create_grid_structure(self):
        """Create the structure of black and white cells"""
        self.grid = [['*' for _ in range(self.cols)] for _ in range(self.rows)]
        self.solution = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        
        # Calculate target number of white cells
        target_white = int(self.rows * self.cols * self.density)
        
        # Place white cells in a structured way
        white_count = 0
        
        # Create horizontal and vertical runs
        for i in range(1, self.rows):
            for j in range(1, self.cols):
                # Randomly decide to start a new region
                if random.random() < 0.7 and white_count < target_white:
                    # Create a horizontal or vertical run
                    if random.random() < 0.5:
                        # Horizontal run
                        length = random.randint(2, min(4, self.cols - j))
                        for k in range(length):
                            if j + k < self.cols and white_count < target_white:
                                self.grid[i][j + k] = '_'
                                white_count += 1
                    else:
                        # Vertical run
                        length = random.randint(2, min(4, self.rows - i))
                        for k in range(length):
                            if i + k < self.rows and white_count < target_white:
                                self.grid[i + k][j] = '_'
                                white_count += 1
    
    def _fill_grid(self):
        """Fill the grid with valid numbers using backtracking"""
        # Find all white cells
        white_cells = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == '_':
                    white_cells.append((i, j))
        
        # Get all runs (horizontal and vertical sequences)
        runs = self._get_all_runs()
        
        if not runs:
            return False
        
        # Use backtracking to fill the grid
        return self._backtrack_fill(white_cells, runs, 0)
    
    def _backtrack_fill(self, white_cells, runs, index):
        """Backtracking algorithm to fill grid with valid values"""
        if index >= len(white_cells):
            return True
        
        i, j = white_cells[index]
        
        # Try digits 1-9
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
        # Check all runs that contain this cell
        for run_cells in runs:
            if (row, col) in run_cells:
                # Check for duplicates in the run
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
        
        # Copy structure
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == '_':
                    puzzle[i][j] = '_'
        
        # Add clue cells
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
    
    def print_solution(self):
        """Print the solution"""
        print("\nSolution:")
        print("=" * 50)
        for i, row in enumerate(self.solution):
            row_str = ""
            for j, val in enumerate(row):
                if self.grid[i][j] == '_':
                    row_str += f"[{val}]\t"
                else:
                    row_str += "[*]\t"
            print(row_str)
        print("=" * 50)


# Example usage
if __name__ == "__main__":
    # Generate different difficulty puzzles
    
    print("EASY PUZZLE (5x5, low density)")
    easy_gen = KakuroGenerator(rows=5, cols=5, density=0.5)
    easy_puzzle = easy_gen.generate()
    easy_gen.print_puzzle()
    
    print("\n\nMEDIUM PUZZLE (6x6, medium density)")
    medium_gen = KakuroGenerator(rows=6, cols=6, density=0.6)
    medium_puzzle = medium_gen.generate()
    medium_gen.print_puzzle()
    
    print("\n\nHARD PUZZLE (8x8, high density)")
    hard_gen = KakuroGenerator(rows=8, cols=8, density=0.65)
    hard_puzzle = hard_gen.generate()
    hard_gen.print_puzzle()
    
    # You can access the puzzles as:
    # easy_puzzle, medium_puzzle, hard_puzzle
    # These are in the same format as kakuro1, kakuro2, etc.