#!/usr/bin/env python3
"""game_of_life - Conway's Game of Life in the terminal."""
import sys, time, random, os

def create_grid(w, h, density=0.3):
    return [[random.random() < density for _ in range(w)] for _ in range(h)]

def step(grid):
    h, w = len(grid), len(grid[0])
    new = [[False]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            n = sum(grid[(r+dr)%h][(c+dc)%w] for dr in (-1,0,1) for dc in (-1,0,1) if dr or dc)
            new[r][c] = n == 3 or (grid[r][c] and n == 2)
    return new

def render(grid):
    return '\n'.join(''.join('██' if c else '  ' for c in row) for row in grid)

def count(grid):
    return sum(sum(row) for row in grid)

def main():
    args = sys.argv[1:]
    w = int(args[0]) if args and args[0].isdigit() else 40
    h = int(args[1]) if len(args)>1 and args[1].isdigit() else 20
    gens = int(args[args.index('-g')+1]) if '-g' in args else 100
    delay = float(args[args.index('-d')+1]) if '-d' in args else 0.1
    if '--seed' in args: random.seed(int(args[args.index('--seed')+1]))
    grid = create_grid(w, h)
    for gen in range(gens):
        os.system('clear' if os.name != 'nt' else 'cls')
        print(f"Generation {gen+1} | Alive: {count(grid)}")
        print(render(grid))
        grid = step(grid)
        time.sleep(delay)

if __name__ == '__main__': main()
