using System;
using System.Collections.Generic;
using System.Text;
using System.IO;
using System.Timers;

namespace PAA_batoh1
{
    class Program
    {
        static void Main(string[] args)
        {
            // defaultni nastaveni programu
            // metoda reseni
            bool useGP = false;
            bool messureTime = false;
            int mult = 100000;

            // zpracovani argumentu
            foreach (string s in args)
            {
                if (s == "-g") useGP = true;
                if (s.Contains("-t"))
                {
                    messureTime = true;
                    string[] arr = (string[])s.Split(':');
                    if (arr.Length > 1) mult = int.Parse(arr[1]);
                }
            }


            TextReader tin = Console.In;
            string line = "";
            int time;
            Batoh b = null;

            // nemerim cas => jen vysledky
            if (!messureTime)
            {
                while ((line = tin.ReadLine()) != null)
                {
                    if (useGP)
                    {
                        b = new GreedyProof(line);
                    }
                    else
                    {
                        b = new BruteForce(line);
                    }

                    // vlastni vypocet
                    b.Compute();
                    b.printAll(true);
                }
            }
            else  // merit cas
            {                
                Console.WriteLine("cas je nutno vydelit {0}", mult);
                while ((line = tin.ReadLine()) != null)
                {
                    // rychla metoda -> musim merit opakovane aby cas byl > 16ms (rozlisovaci schopnost)
                    int startTime = Environment.TickCount;
                    for (int i = mult; i > 0; i--)
                    {
                        if (useGP)
                            b = new GreedyProof(line);
                        else
                            b = new BruteForce(line);
                        b.Compute();
                    }
                    time = Environment.TickCount - startTime;
                    b.printAll(false);
                    Console.WriteLine(" ; time: {0}", time);
                }
            }
        }
    }
}

