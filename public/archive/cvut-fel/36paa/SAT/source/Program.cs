using System;
using System.Collections.Generic;
using System.Text;
using System.IO;

namespace SAT_SimAnneal
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length != 1)
            {
                Console.WriteLine("Bad parameters count.\nUsage: SAT input.txt");
                return;
            }

            string[] dirs = Directory.GetFiles(args[0]);

            //string fileName = dirs[0];
            int k_repeat = 5;
            double T0_k = 0.1;
            //int Tf = 1;
            double dT = 0.9;
            double equ_k = 1;

            SimAnneal SA = null;                      

            Console.WriteLine("T0\tTf\tdT\tequ\trep\tinst\tNF\ttime\tAvgErr\tBestErr");


            for (int Tf = 1; Tf <= 10; Tf++)
            {
                int cost = int.MinValue, bestCost = int.MinValue;
                int time_start = 0, time_stop = 0;
                double relErr = 0, bestRelErr = 0;
                double bre_total = 0;
                int stat_nf = 0;
                int time_total = 0;
                bool solFound = false;

                foreach (string fileName in dirs)
                {
                    solFound = false;
                    for (int i = 0; i < k_repeat; i++)
                    {
                        SA = new SimAnneal(fileName, T0_k, Tf, dT, equ_k);
                        time_start = Environment.TickCount;
                        cost = SA.Compute();
                        time_stop = Environment.TickCount;
                        time_total += (time_stop - time_start);

                        if (SA.ToString() != "NF")
                        {
                            solFound = true;
                            if (cost > bestCost)
                            {
                                bestCost = cost;
                                bestRelErr = SA.getRelErr();
                            }
                            relErr += SA.getRelErr();
                        }                        
                    }

                    if (!solFound)
                        stat_nf++;
                    else
                        bre_total += bestRelErr;

                    bestCost = 0;
                    
                }

                Console.Write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t",
                    T0_k,
                    Tf,
                    dT.ToString("0.000"),
                    equ_k,
                    k_repeat,
                    dirs.Length,
                    ((double)stat_nf / (double)(k_repeat * dirs.Length)).ToString("0.000"),
                    ((double)time_total / (double)(k_repeat * dirs.Length)).ToString("0.0")
                );

                if (stat_nf == (k_repeat * dirs.Length))
                    Console.WriteLine("---\t---");
                else
                    Console.WriteLine("{0}\t{1}",
                        (relErr / (double)((k_repeat * dirs.Length) - stat_nf)).ToString("0.000"),
                        (bre_total / ((double)(dirs.Length - stat_nf))).ToString("0.000")
                    );

            }
            //Console.WriteLine(SA);
            //Console.ReadKey();

        }
    }
}
