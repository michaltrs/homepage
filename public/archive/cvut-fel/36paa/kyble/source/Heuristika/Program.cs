using System;
using System.Collections.Generic;
using System.Text;

namespace Kyble_heuristika
{
    class Program
    {
        static void Main(string[] args)
        {

            Input[] inputs = new Input[] { 
                // capacity, init_state, final_state
                new Input(new int[] {14, 10, 6, 2, 8}, new int[] {0, 0, 1, 0, 0}, new int[] {12, 6, 4, 1, 8}),
                new Input(new int[] {14, 10, 6, 2, 8}, new int[] {0, 0, 1, 0, 0}, new int[] {14, 4, 5, 0, 4}),
                new Input(new int[] {14, 10, 6, 2, 8}, new int[] {0, 0, 1, 0, 0}, new int[] {12, 6, 6, 2, 4}),
                new Input(new int[] {14, 10, 6, 2, 8}, new int[] {0, 0, 1, 0, 0}, new int[] {0, 2, 1, 2, 8}),

                new Input(new int[] {15, 12, 8, 4, 6}, new int[] {0, 0, 0, 0, 0}, new int[] {5, 5, 5, 0, 1}),
                new Input(new int[] {15, 12, 8, 4, 6}, new int[] {0, 0, 0, 0, 0}, new int[] {12, 1, 3, 4, 5}),
                new Input(new int[] {15, 12, 8, 4, 6}, new int[] {0, 0, 0, 0, 0}, new int[] {11, 1, 3, 4, 5}),
                new Input(new int[] {15, 12, 8, 4, 6}, new int[] {0, 0, 0, 0, 0}, new int[] {3, 12, 4, 0, 6}),
                new Input(new int[] {15, 12, 8, 4, 6}, new int[] {0, 0, 0, 0, 0}, new int[] {2, 0, 4, 3, 6}),

                new Input(new int[] {14, 10, 12, 3, 8}, new int[] {0, 0, 0, 0, 0}, new int[] {13, 9, 12, 2, 7}),
                new Input(new int[] {14, 10, 12, 3, 8}, new int[] {0, 0, 0, 0, 0}, new int[] {1, 5, 5, 3, 4}),
                new Input(new int[] {14, 10, 12, 3, 8}, new int[] {0, 0, 0, 0, 0}, new int[] {0, 9, 6, 3, 1}),
                new Input(new int[] {14, 10, 12, 3, 8}, new int[] {0, 0, 0, 0, 0}, new int[] {12, 0, 12, 0, 2}),
                new Input(new int[] {14, 10, 12, 3, 8}, new int[] {0, 0, 0, 0, 0}, new int[] {7, 3, 7, 0, 0}),
                new Input(new int[] {14, 10, 12, 3, 8}, new int[] {0, 0, 0, 0, 0}, new int[] {7, 0, 7, 0, 7}),
            };

            int maior = 1;
            int minor = 1;

            for (int i = 0; i < inputs.Length; i++)
            {                
                Heuristic bp = new Heuristic(inputs[i]);
                bp.Compute();


                Console.WriteLine("Input: {0}.{1}", maior, minor++);
                Console.WriteLine(bp);
                if (maior == 1 && minor == 5) { maior = 2; minor = 1;};
                if (maior == 2 && minor == 6) { maior = 3; minor = 1; };
            }

            Console.WriteLine("DONE");
            Console.ReadKey();

        }
    }
}
