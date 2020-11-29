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

def printGrid(grid, size):
    for y in range(size):
        output = list()
        for x in range(size):
            output.append(grid[(y * size) + x])
        print ''.join(output)

def insertWord(grid, word, size):
    minx = 2
    maxx = size - 3
    miny = 2
    maxy = size - 3
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
        grid[(y * size) + x] = c
        x += vx
        y += vy

    print 'Direction : {0}'.format(d)
    return (x - vx), (y - vy)

def pointInGrid(x, y, size):
    if x >= 0 and x < size and y >= 0 and y < size:
        return True
    return False

def CheckWordNotThere(grid, x, y, c, word, size):
    reverse = word[::-1]
    span = len(word) - 1
    letters = list()

    # First Check Up and Down
    # Add the letters above
    for i in xrange(span, 0, -1):
        if (pointInGrid(x, y - i, size)):
            letters.append(grid[((y - i) * size) + x])

    # Add the letter
    letters.append(c)
    # Add the letters after
    for i in xrange(1, span):
        if (pointInGrid(x, y + i, size)):
            letters.append(grid[((y + i) * size) + x])

    # Check result
    result = ''.join(letters)
    if word in result or reverse in result:
        return False




    # Second check left and right
    del letters [:]
    for i in xrange(span, 0, -1):
        if (pointInGrid(x - i, y, size)):
            letters.append(grid[(y * size) + x - i])

    # Add the letter
    letters.append(c)
    # Add the letters after
    for i in xrange(1, span):
        if (pointInGrid(x + i, y, size)):
            letters.append(grid[(y * size) + x + i])

    # Check result
    result = ''.join(letters)
    if word in result or reverse in result:
        return False




    # Thirdly check DownLeft and UpRight
    del letters [:]
    for i in xrange(span, 0, -1):
        if (pointInGrid(x - i, y + i, size)):
            letters.append(grid[((y + i) * size) + x - i])

    # Add the letter
    letters.append(c)
    # Add the letters after
    for i in xrange(1, span):
        if (pointInGrid(x + i, y - i, size)):
            letters.append(grid[((y - i) * size) + x + i])

    # Check result
    result = ''.join(letters)
    if word in result or reverse in result:
        return False




    # Finally check UpLeft and DownRight
    del letters [:]
    for i in xrange(span, 0, -1):
        if (pointInGrid(x - i, y - i, size)):
            letters.append(grid[((y - i) * size) + x - i])

    # Add the letter
    letters.append(c)
    # Add the letters after
    for i in xrange(1, span):
        if (pointInGrid(x + i, y + i, size)):
            letters.append(grid[((y + i) * size) + x + i])

    # Check result
    result = ''.join(letters)
    if word in result or reverse in result:
        return False

    # No word present!
    return True

def insertLetter(grid, x, y, word, extra, size):
    # Build the list of chars to insert in order we want to try
    # First, add all the neighbouring letters
    # Then add the remaining letters (scrambled) in front, this means
    # neighbouring letters should be attempted last, so result in less
    # blocks of the same letters
    neighbours = list()
    if (pointInGrid(x - 1, y, size)):
        c = grid[(y * size) + x - 1]
        if (c is not '.' and c not in neighbours):
            neighbours.append(c)
    if (pointInGrid(x + 1, y, size)):
        c = grid[(y * size) + x + 1]
        if (c is not '.' and c not in neighbours):
            neighbours.append(c)
    if (pointInGrid(x, y - 1, size)):
        c = grid[((y - 1) * size) + x]
        if (c is not '.' and c not in neighbours):
            neighbours.append(c)
    if (pointInGrid(x, y + 1, size)):
        c = grid[((y + 1) * size) + x]
        if (c is not '.' and c not in neighbours):
            neighbours.append(c)

    # merge the word and extra work together, and scramble letters
    # so that we don't try to insert letters in the same order every time.
    letters = list()
    for i in range(len(word)):
        if word[i] not in neighbours:
            letters.append(word[i])
    for i in range(len(extra)):
        if extra[i] not in neighbours:
            letters.append(extra[i])

    # Shuffle letters
    random.shuffle(letters)

    # Add neighbours onto end
    for i in range(len(neighbours)):
        letters.append(neighbours[i])

    # Loop through word trying to insert a letter such that it does NOT make the word in any direction
    for i in xrange(len(letters) - 1):
        c = letters[i]

        canInsert = CheckWordNotThere(grid, x, y, c, word, size)
        if not canInsert:
            continue

        if extra is not '':
            canInsert = CheckWordNotThere(grid, x, y, c, extra, size)
            if not canInsert:
                continue
        
        if canInsert:
            grid[(y * size) + x] = c
            return True
    
    return False

def fillGrid(grid, end, word, extra, size):
    q = queue.Queue()
    q.put(end)
    while not q.empty():
        p = q.get()

        x = p[0]
        y = p[1]

        # Check if grid value is blank
        if grid[(y * size) + x] is '.':
            success = insertLetter(grid, x, y, word, extra, size)
            if not success:
                return False
            
        
        # Queue up blank spaces around current point
        if (y > 0 and grid[((y - 1) * size) + x] is '.'):
            q.put((x, y - 1))

        if (y < size - 1 and grid[((y + 1) * size) + x] is '.'):
            q.put((x, y + 1))

        if (x > 0 and grid[(y * size) + x - 1] is '.'):
            q.put((x - 1, y))

        if (x < size - 1 and grid[(y * size) + x + 1] is '.'):
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
    grid = ['.' for i in xrange(args.size * args.size)]

    # Insert word
    end = insertWord(grid, args.word, args.size)
    print end
    printGrid(grid, args.size)

    # Fill Grid with letters
    success = fillGrid(grid, end, args.word, args.extra, args.size)
    if not success:
        print '--- FAILED ---'
    else:
        print 'Success!'
    printGrid(grid, args.size)

if __name__ == '__main__':
    main()