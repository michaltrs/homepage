using System;
using System.Collections.Generic;
using System.Text;
using System.IO;

namespace Batoh_BB
{
    class Program
    {
        static int mult = 10;

        static StreamReader sr;
        static StreamWriter sw;


        static void Main(string[] args)
        {
            if (args.Length == 2)
            {
                mult = int.Parse(args[1]);
            }
            else
            {
                if (args.Length != 1)
                {
                    Console.WriteLine("Knapsack problem (Branch & Bound method)");
                    Console.WriteLine("Usage: Batoh_BB.exe input_file.txt");
                    return;
                }
            }

            string line = "";
            BB b = null;
            int time;
            int instanceNr = 0;
            int totalTime = 0;


            sr = new StreamReader(args[0]);
            sw = new StreamWriter(Path.GetFileNameWithoutExtension(args[0]) + ".out.txt");
            sw.WriteLine("ID\tn\tcena\tkonfigurace\tcas");

            while ((line = sr.ReadLine()) != null)
            {
                int startTime = Environment.TickCount;
                for (int i = mult; i > 0; i--)
                {
                    b = new BB(line);
                    b.Compute();
                }
                time = Environment.TickCount - startTime;                
                sw.WriteLine("{0}\t{1}", b.ToString(), (double)time / (double)mult);
                instanceNr++;
                totalTime += time;
            }

            sw.WriteLine("Average time: {0} s", (double)totalTime / ((double)(instanceNr * mult)));

            sr.Close();
            sw.Close();
        }
    }
}
