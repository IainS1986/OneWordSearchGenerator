import sys
import argparse
import array
import random
import queue
from enum import Enum
from random import shuffle

class Direction(Enum):
    Up = 0
    Down = 1
    Left = 2
    Right = 3
    UpLeft = 4
    UpRight = 5
    DownLeft = 6
    DownRight = 7

def scramble(word):
    word = list(word)
    shuffle(word)
    return ''.join(word)

def printGrid(grid):
    for y in grid:
        output = ''
        for x in y:
            output = output + x
        print output

def insertWord(grid, word):
    minx = 2
    maxx = len(grid) - 3
    miny = 2
    maxy = len(grid) - 3
    vx = 0
    vy = 0
    d = Direction(random.randint(0, 7))

    if d is Direction.Left or d is Direction.UpLeft or d is Direction.DownLeft:
        minx += len(word)
        vx = -1
    if d is Direction.Right or d is Direction.UpRight or d is Direction.DownRight:
        maxx -= len(word)
        vx = 1
    if d is Direction.Up or d is Direction.UpLeft or d is Direction.UpRight:
        miny += len(word)
        vy = -1
    if d is Direction.Down or d is Direction.DownLeft or d is Direction.DownRight:
        maxy -= len(word)
        vy = 1

    x = random.randint(minx, maxx)
    y = random.randint(miny, maxy)

    for c in word:
        grid[y][x] = c
        x += vx
        y += vy

    print 'Direction : {0}'.format(d)
    return x, y

def pointInGrid(grid, x, y):
    if x >= 0 and x < len(grid) and y >= 0 and y < len(grid):
        return True
    return False

def CheckWordNotThere(grid, x, y, c, word):
    span = len(word) - 1
    letters = list()

    # First Check Up and Down
    # Add the letters above
    for i in xrange(span, 0, -1):
        if (pointInGrid(grid, x, y - i)):
            letters.append(grid[y - i][x])

    # Add the letter
    letters.append(c)
    # Add the letters after
    for i in xrange(1, span):
        if (pointInGrid(grid, x, y + i)):
            letters.append(grid[y + i][x])

    # Check result
    if word in ''.join(letters):
        return False




    # Second check left and right
    del letters [:]
    for i in xrange(span, 0, -1):
        if (pointInGrid(grid, x - i, y)):
            letters.append(grid[y][x - i])

    # Add the letter
    letters.append(c)
    # Add the letters after
    for i in xrange(1, span):
        if (pointInGrid(grid, x + i, y)):
            letters.append(grid[y][x + i])

    # Check result
    if word in ''.join(letters):
        return False




    # Thirdly check DownLeft and UpRight
    del letters [:]
    for i in xrange(span, 0, -1):
        if (pointInGrid(grid, x - i, y + i)):
            letters.append(grid[y + i][x - i])

    # Add the letter
    letters.append(c)
    # Add the letters after
    for i in xrange(1, span):
        if (pointInGrid(grid, x + i, y - i)):
            letters.append(grid[y - i][x + i])

    # Check result
    if word in ''.join(letters):
        return False




    # Finally check UpLeft and DownRight
    del letters [:]
    for i in xrange(span, 0, -1):
        if (pointInGrid(grid, x - i, y - i)):
            letters.append(grid[y - i][x - i])

    # Add the letter
    letters.append(c)
    # Add the letters after
    for i in xrange(1, span):
        if (pointInGrid(grid, x + i, y + i)):
            letters.append(grid[y + i][x + i])

    # Check result
    if word in ''.join(letters):
        return False

    # No word present!
    return True

def insertLetter(grid, x, y, word, extra):
    concat = word
    if extra is not '':
        concat += extra
    concat = scramble(concat)

    r = random.randint(0, len(concat) - 1)

    # Loop through word trying to insert a letter such that it does NOT make the word in any direction
    for i in xrange(len(concat) - 1):
        ci = i + r
        if ci >= len(concat):
            ci -= len(concat)
        
        c = concat[ci]

        canInsert = CheckWordNotThere(grid, x, y, c, word)
        if not canInsert:
            continue

        if extra is not '':
            canInsert = CheckWordNotThere(grid, x, y, c, extra)
            if not canInsert:
                continue
        
        if canInsert:
            grid[y][x] = c
            return True
    
    return False

def fillGrid(grid, end, word, extra):
    maxx = len(grid)
    maxy = len(grid)
    q = queue.Queue()
    q.put(end)
    while not q.empty():
        p = q.get()

        x = p[0]
        y = p[1]

        # Check if grid value is blank
        if grid[y][x] is '.':
            success = insertLetter(grid, x, y, word, extra)
            if not success:
                return False
            
        
        # Queue up blank spaces around current point
        if (y > 0 and grid[y - 1][x] is '.'):
            q.put((x, y - 1))

        if (y < maxy - 1 and grid[y + 1][x] is '.'):
            q.put((x, y + 1))

        if (x > 0 and grid[y][x - 1] is '.'):
            q.put((x - 1, y))

        if (x < maxx - 1 and grid[y][x + 1] is '.'):
            q.put((x + 1, y))
    
    return True

def main():
    parser = argparse.ArgumentParser(description='The One Word Search')
    parser.add_argument('-w', '--word', type=str, dest='word', default='word', help='The word to hide in the grid (default is \'word\')')
    parser.add_argument('--size', type=int, dest='size', default=15, help='The size of the wordsearch grid (default is 15)')
    parser.add_argument('--extra', type=str, dest='extra', default='', help='Extra letters to include (Optional)')
    parser.add_argument('--seed',type=int, dest='seed', default=0, help='Specify the seed for the random generator (Optional)')
    args = parser.parse_args()
    print 'Size : {0}'.format(args.size)
    print 'Word : {0}'.format(args.word)
    print 'Extra : {0}'.format(args.extra)
    print 'Seed : {0}'.format(args.seed)

    if args.seed is not None:
        random.seed = args.seed

    # Initialize the grid
    grid = [['.' for x in xrange(args.size)] for y in xrange(args.size)]

    # Insert word
    end = insertWord(grid, args.word)
    print end
    printGrid(grid)

    # Fill Grid with letters
    success = fillGrid(grid, end, args.word, args.extra)
    if not success:
        print '--- FAILED ---'
    else:
        print 'Success!'
    printGrid(grid)

if __name__ == '__main__':
    main()