using System;
using System.Collections.Generic;
using System.Text;

namespace OneWordSearchGenerator
{
    class Program
    {
        enum Direction
        {
            Up = 0,
            Down = 1,
            Left = 2,
            Right = 3,
            UpLeft = 4,
            UpRight = 5,
            DownLeft = 6,
            DownRight = 7,

        }

        static void Main(string[] args)
        {
            // Generate a word search containing one single word
            // Fill in the gaps with only the letters from the word
            // Ensuring that the word is never repeated again
            int width = 15;
            int height = 15;
            int? seed = null;
            string word1 = "HOLLY";
            string word2 = "";
            char[,] grid = new char[width, height];

            Console.Clear();
            Console.WriteLine($"\n\nRunning on a grid of {width} by {height} with the word '{word1}'\n\n");

            PopulateWithDots(ref grid);
            var endPosition = InsertWordIntoGrid(word1, ref grid, seed);
            PrintGrid(grid);
            var success = FillGrid(ref grid, endPosition, word1, word2, seed);
            if (!success)
                Console.WriteLine("---  Failed!!!!!  ---");
            PrintGrid(grid);
        }

        static void PopulateWithDots(ref char[,] grid)
        {
            int rows = grid.GetLength(0);
            int cols = grid.GetLength(1);
            for (int i = 0; i < cols; i++)
            {
                for (int j = 0; j < rows; j++)
                {
                    grid[i, j] = '.';
                }
            }
        }


        static (int, int) InsertWordIntoGrid(string word, ref char[,] grid, int? seed = null)
        {
            // Insert the word at a random location in a random direction
            Random rand = seed.HasValue ? new Random(seed.Value) : new Random();
            Direction dir = (Direction)rand.Next(0, 8);

            // Figure out the min and max X and Y values that can be for the start
            // location, then pick one and insert in the direction
            // We make it a little harder by avoiding the outer 2 edges
            int minX = 2;
            int maxX = grid.GetLength(1) - 3;
            int minY = 2;
            int maxY = grid.GetLength(0) - 3;

            // Direction we want to add letters in the grid
            int xInc = 0;
            int yInc = 0;

            // X
            switch(dir)
            {
                case Direction.Left:
                case Direction.UpLeft:
                case Direction.DownLeft:
                    minX += word.Length;
                    xInc = -1;
                    break;

                case Direction.Right:
                case Direction.UpRight:
                case Direction.DownRight:
                    maxX -= word.Length;
                    xInc = 1;
                    break;
            }

            // Y
            switch (dir)
            {
                case Direction.Up:
                case Direction.UpLeft:
                case Direction.UpRight:
                    minY += word.Length;
                    yInc = -1;
                    break;

                case Direction.Down:
                case Direction.DownLeft:
                case Direction.DownRight:
                    maxY -= word.Length;
                    yInc = 1;
                    break;
            }

            // Pick random X and Y
            int x = rand.Next(minX, maxX + 1);
            int y = rand.Next(minY, maxY + 1);

            // Insert at XY and add word in direction
            for(int i=0; i<word.Length; i++)
            {
                grid[y, x] = word[i];

                x += xInc;
                y += yInc;
            }

            return (x, y);
        }

        static void PrintGrid(char[,] grid)
        {
            // Print grid to console so we can see whats going on!
            int rows = grid.GetLength(0);
            int cols = grid.GetLength(1);
            for(int i = 0; i < rows; i++)
            {
                StringBuilder builder = new StringBuilder();
                for(int j = 0; j < cols; j++)
                {
                    builder.Append(grid[i, j]);
                }
                Console.WriteLine(builder.ToString());
            }
            Console.WriteLine("\n\n");
        }


        static Queue<(int, int)> _spaces = new Queue<(int, int)>();
        static bool FillGrid(ref char[,] grid, (int, int) endOfWord, string word, string supplementaryWord, int? seed = null)
        {
            Random rand = seed.HasValue ? new Random(seed.Value) : new Random();
            int maxY = grid.GetLength(0);
            int maxX = grid.GetLength(1);
            _spaces.Enqueue(endOfWord);
            while(_spaces.Count > 0)
            {
                var point = _spaces.Dequeue();
                int x = point.Item1;
                int y = point.Item2;

                // Check if point is blank/dot
                if (grid[y, x] == '.')
                {
                    // Insert random letter, return FALSE if we can't fit *any*
                    if (!InsertLetterAtSpace(ref grid, point, word, supplementaryWord, rand))
                        return false;
                }

                // Queue up all blank spaces around this point in compass directions
                if (y > 0 && grid[y - 1, x] == '.')
                    _spaces.Enqueue((x, y - 1));

                if (y < maxY - 1 && grid[y + 1, x] == '.')
                    _spaces.Enqueue((x, y + 1));

                if (x > 0 && grid[y, x - 1] == '.')
                    _spaces.Enqueue((x - 1, y));

                if (x < maxX - 1 && grid[y, x + 1] == '.')
                    _spaces.Enqueue((x + 1, y));
            }

            return true;
        }

        static bool InsertLetterAtSpace(ref char[,] grid, (int, int) point, string word, string supplementaryWord, Random rand)
        {
            // Start at random position in word
            string concat = word + supplementaryWord;
            // Scramble concat
            concat = concat.Trim();
            concat = concat.Scramble();

            int r = rand.Next(0, concat.Length);

            // Loop through word trying to insert a letter such that it does NOT make the word in any direction
            for (int i = 0; i < concat.Length; i++)
            {
                int charIndex = i + r;
                if (charIndex >= concat.Length)
                    charIndex -= concat.Length;

                char c = concat[charIndex];

                // Try and insert c at space
                bool canInsert = CheckWordNotThere(ref grid, point, c, word);
                if (!canInsert)
                    continue;

                if (string.IsNullOrEmpty(supplementaryWord) == false)
                {
                    canInsert = CheckWordNotThere(ref grid, point, c, supplementaryWord);
                    if (!canInsert)
                        continue;
                }

                if (canInsert)
                {
                    grid[point.Item2, point.Item1] = c;
                    return true;
                }
            }

            return false;
        }

        static bool CheckWordNotThere(ref char[,] grid, (int, int) point, char c, string word)
        {
            int x = point.Item1;
            int y = point.Item2;

            int span = word.Length - 1;
            StringBuilder letters = new StringBuilder();

            // First Check Up and Down
            // Add the letters above
            for(int i = span; i > 0; i--)
            {
                if (grid.PointInGrid(x, y - i))
                    letters.Append(grid[y - i, x]);
            }
            // Add the letter
            letters.Append(c);
            // Add the letters after
            for (int i = 1; i <= span; i++)
            {
                if (grid.PointInGrid(x, y + i))
                    letters.Append(grid[y + i, x]);
            }
            // Check result
            if (letters.ContainsWords(word))
                return false;




            //Second check left and right
            letters.Clear();
            // Add the letters to the left
            for (int i = span; i > 0; i--)
            {
                if (grid.PointInGrid(x - i, y))
                    letters.Append(grid[y, x - i]);
            }
            // Add the letter
            letters.Append(c);
            // Add the letter to the right
            for (int i = 1; i <= span; i++)
            {
                if (grid.PointInGrid(x + i, y))
                    letters.Append(grid[y, x + i]);
            }
            // Check result
            if (letters.ContainsWords(word))
                return false;





            // Third check DownLeft UpRight Diagonal
            letters.Clear();
            // Add the letters down and left
            for (int i = span; i > 0; i--)
            {
                if (grid.PointInGrid(x - i, y + i))
                    letters.Append(grid[y + i, x - i]);
            }
            // Add the letter
            letters.Append(c);
            // Add the letters up and right
            for (int i = 1; i <= span; i++)
            {
                if (grid.PointInGrid(x + i, y - i))
                    letters.Append(grid[y - i, x + i]);
            }
            // Check result
            if (letters.ContainsWords(word))
                return false;





            // Finally check UpLeft DownRight Diagonal
            letters.Clear();
            // Add the letters up and left
            for (int i = span; i > 0; i--)
            {
                if (grid.PointInGrid(x - i, y - i))
                    letters.Append(grid[y - i, x - i]);
            }
            // Add the letter
            letters.Append(c);
            // Add the letters down and right
            for (int i = 1; i <= span; i++)
            {
                if (grid.PointInGrid(x + i, y + i))
                    letters.Append(grid[y + i, x + i]);
            }
            // Check result
            if (letters.ContainsWords(word))
                return false;




            return true;
        }
    }


    public static class StringExtensions
    {
        public static bool PointInGrid(this char[,] grid, int x, int y)
            => x >= 0 && y >= 0 && y < grid.GetLength(0) && x < grid.GetLength(1);

        public static bool ContainsWords(this string sb, params string[] words)
        {
            foreach(var word in words)
            {
                var reverse = word.Reverse();
                if (sb.Contains(word) || sb.Contains(reverse))
                    return true;
            }

            return false;
        }

        public static bool ContainsWords(this StringBuilder sb, params string[] words)
            => sb.ToString().ContainsWords(words);

        public static string Scramble(this string s, Random rand = null)
        {
            if (rand == null)
                rand = new Random();

            StringBuilder scramble = new StringBuilder();
            scramble.Append(s);
            int length = scramble.Length;
            for (int i = 0; i < length; ++i)
            {
                int index1 = (rand.Next() % length);
                int index2 = (rand.Next() % length);

                Char temp = scramble[index1];
                scramble[index1] = scramble[index2];
                scramble[index2] = temp;

            }

            return scramble.ToString();
        }

        public static string Reverse(this string input)
        {
            char[] chars = input.ToCharArray();
            Array.Reverse(chars);
            return new String(chars);
        }
    }
}
