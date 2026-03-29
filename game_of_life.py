import argparse, random, time, sys, os

def make_grid(w, h, density=0.3, seed=None):
    if seed: random.seed(seed)
    return [[1 if random.random() < density else 0 for _ in range(w)] for _ in range(h)]

def step(grid):
    h, w = len(grid), len(grid[0])
    new = [[0]*w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            n = sum(grid[(y+dy)%h][(x+dx)%w] for dy in (-1,0,1) for dx in (-1,0,1)) - grid[y][x]
            if grid[y][x]: new[y][x] = 1 if n in (2,3) else 0
            else: new[y][x] = 1 if n == 3 else 0
    return new

def display(grid, alive="█", dead=" "):
    return "\n".join("".join(alive if c else dead for c in row) for row in grid)

def main():
    p = argparse.ArgumentParser(description="Game of Life")
    p.add_argument("-w", "--width", type=int, default=40)
    p.add_argument("-H", "--height", type=int, default=20)
    p.add_argument("-g", "--generations", type=int, default=100)
    p.add_argument("-d", "--density", type=float, default=0.3)
    p.add_argument("--seed", type=int)
    p.add_argument("--delay", type=float, default=0.1)
    args = p.parse_args()
    grid = make_grid(args.width, args.height, args.density, args.seed)
    for gen in range(args.generations):
        sys.stdout.write(f"\033[H\033[J")
        print(f"Generation {gen}")
        print(display(grid))
        alive = sum(sum(row) for row in grid)
        print(f"Alive: {alive}")
        grid = step(grid)
        time.sleep(args.delay)

if __name__ == "__main__":
    main()
