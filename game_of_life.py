#!/usr/bin/env python3
"""Conway's Game of Life simulator."""
import sys

def step(grid):
    rows, cols = len(grid), len(grid[0])
    new = [[0]*cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            n = sum(grid[(r+dr)%rows][(c+dc)%cols]
                    for dr in (-1,0,1) for dc in (-1,0,1) if (dr,dc) != (0,0))
            if grid[r][c]:
                new[r][c] = 1 if n in (2, 3) else 0
            else:
                new[r][c] = 1 if n == 3 else 0
    return new

def run(grid, steps):
    history = [grid]
    for _ in range(steps):
        grid = step(grid)
        history.append(grid)
    return history

def from_pattern(pattern, rows=20, cols=20, offset=(5,5)):
    grid = [[0]*cols for _ in range(rows)]
    for r, row in enumerate(pattern):
        for c, ch in enumerate(row):
            if ch in ("O", "1", "#"):
                grid[offset[0]+r][offset[1]+c] = 1
    return grid

def population(grid):
    return sum(sum(row) for row in grid)

def to_string(grid):
    return chr(10).join("".join("#" if c else "." for c in row) for row in grid)

GLIDER = ["OOO", "O..", ".O."]
BLINKER = ["OOO"]
BLOCK = ["OO", "OO"]

def test():
    # Blinker oscillates
    g = from_pattern(BLINKER, 5, 5, (2, 1))
    g2 = step(g)
    assert g2[1][2] == 1 and g2[2][2] == 1 and g2[3][2] == 1  # vertical
    g3 = step(g2)
    assert g3[2][1] == 1 and g3[2][2] == 1 and g3[2][3] == 1  # horizontal again
    # Block is still life
    g = from_pattern(BLOCK, 5, 5, (1, 1))
    g2 = step(g)
    assert g == g2
    # Glider moves
    g = from_pattern(GLIDER, 10, 10, (0, 0))
    pop0 = population(g)
    h = run(g, 4)
    assert population(h[4]) == pop0  # glider preserves population
    print("  game_of_life: ALL TESTS PASSED")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else:
        g = from_pattern(GLIDER)
        for i, state in enumerate(run(g, 5)):
            print(f"Step {i}:"); print(to_string(state)); print()
