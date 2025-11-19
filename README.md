# Kakuro Solver - CSP Implementation

A comprehensive Python implementation of a Kakuro puzzle solver using Constraint Satisfaction Problem (CSP) techniques. This project includes multiple solving algorithms, a puzzle generator, and performance comparison tools.

## Overview

Kakuro (also known as "Cross Sums") is a logic puzzle that combines elements of crosswords and Sudoku. Players must fill a grid with digits 1-9 such that:
- Each horizontal or vertical run sums to a specified target
- No digit is repeated within a run
- All cells must be filled

This implementation provides various CSP algorithms to solve Kakuro puzzles efficiently.

## Features

- **Multiple Solving Algorithms**:
  - Algorithm 1: Backtracking with Forward Checking
  - Algorithm 2: MRV+Degree heuristic with MAC (Maintaining Arc Consistency) and LCV (Least Constraining Value)
  
- **Puzzle Generator**: Create random Kakuro puzzles of varying sizes and difficulties

- **Solution Verification**: Automatic validation of solutions against all constraints

- **Performance Metrics**: Track execution time and number of assignments

- **Pre-loaded Puzzles**: Four difficulty levels (0-3) of hand-crafted puzzles

## File Structure

```
├── csp.py                  # Core CSP framework and algorithms
├── kakuro_algo.py          # Main solver with algorithm comparison
├── kakuro_generator.py     # Random puzzle generator
├── kakuro_optimized.py     # Optimized solver implementation
├── search.py               # Search algorithms and utilities
└── utils.py                # Helper functions and data structures
```

## Requirements

```bash
pip install sortedcontainers numpy
```

## Usage

### Basic Usage

Run the main solver:

```bash
python kakuro_algo.py
```

You'll be prompted to:
1. Choose between hardcoded puzzles or generate a new one
2. Select puzzle difficulty (0-3) or generation parameters
3. Choose which algorithm(s) to run

### Example Session

```
Select puzzle source:
1. Hardcoded puzzles (difficulty 0-3)
2. Generate new puzzle
Enter your choice (1 or 2): 1

Select difficulty (0, 1, 2, 3): 2

Select which algorithm(s) to run:
1. Algorithm 1 (Backtracking + Forward Checking)
2. Algorithm 2 (MRV+Degree + MAC + LCV)
3. Run Both and Compare
Enter your choice (1, 2, or 3): 3
```


## Algorithm Details

### Algorithm 1: Backtracking + Forward Checking
- Uses standard backtracking search
- Forward checking to prune inconsistent values
- Simple but effective for smaller puzzles

### Algorithm 2: MRV+Degree + MAC + LCV
- **MRV (Minimum Remaining Values)**: Select variables with fewest legal values
- **Degree Heuristic**: Break ties by choosing variables with most constraints
- **MAC (Maintaining Arc Consistency)**: Propagate constraints after each assignment
- **LCV (Least Constraining Value)**: Order values to preserve maximum flexibility

## Puzzle Format

Puzzles are represented as 2D lists where:
- `'*'` = Black cell (no value)
- `'_'` = White cell (to be filled)
- `[down_sum, right_sum]` = Clue cell with sum constraints
  - `down_sum`: Sum for vertical run below
  - `right_sum`: Sum for horizontal run to the right
  - `''` indicates no constraint in that direction

### Example Puzzle

```python
kakuro1 = [
    ['*', '*', '*', [6, ''], [3, '']],
    ['*', [4, ''], [3, 3], '_', '_'],
    [['', 10], '_', '_', '_', '_'],
    [['', 3], '_', '_', '*', '*']
]
```

## CSP Constraint Implementation

The `KakuroConstraints` method enforces:

1. **All-Different Constraint**: No duplicate values in any run
2. **Sum Constraint**: Values in each run must sum to the target
3. **Partial Sum Validation**: Early pruning when partial sums exceed targets
4. **Feasibility Check**: Verify remaining cells can reach target sum

## Performance Comparison

When running both algorithms, you'll see metrics like:

```
PERFORMANCE COMPARISON
================================================================================
Algorithm                                     Time (ms)       Assignments    
--------------------------------------------------------------------------------
Algorithm 1 (Backtracking + FC)              125.50          458            
Algorithm 2 (MRV+Degree+MAC+LCV)             43.20           127            

⚡ Algorithm 2 was FASTER by 2.90x
📊 Algorithm 2 used 72.3% FEWER assignments (127 vs 458)
```

## Solution Verification

All solutions are automatically verified to ensure:
- All cells are filled with digits 1-9
- Each run sums to its target value
- No duplicates exist within any run

```
VERIFYING SOLUTION...
------------------------------------------------------------
✓ Solution is CORRECT! All constraints satisfied.
```



## Contributing

Feel free to extend this implementation with:
- New solving algorithms
- Additional heuristics
- GUI interface
- More puzzle formats
- Performance optimizations
