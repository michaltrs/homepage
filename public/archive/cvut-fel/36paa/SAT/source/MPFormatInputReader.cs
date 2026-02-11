using System;
using System.Collections.Generic;
using System.Text;
using System.IO;

namespace SAT_SimAnneal
{
    /*
     * SAT Reader for Martin Prchlik format
     * Format description:
     * *******************
     * line     desc.
     * 1        empty
     * 2        solution (by BruteForce)
     * 3        variables_count clausules_count variables_in_clausules_count (3 for 3SAT :-))c
     * 4 - x    clausules (variable index start by 1, minus before index means negation)
     * x+1      weight for each variable
     */
    class MPFormatInputReader
    {
        private StreamReader sr;
        public int BFCost;


        public MPFormatInputReader(string file)
        {
            if (!File.Exists(file))
            {
                throw new Exception("Input file doesn't exist!");
            }

            sr = new StreamReader(file);
        }

        public SAT ReadAll()
        {
            sr.ReadLine();
            BFCost = int.Parse(sr.ReadLine());
            string[] sarr = sr.ReadLine().Split(' ');

            int varCnt = int.Parse(sarr[0]);
            int clCnt = int.Parse(sarr[1]);
            int varInClCnt = int.Parse(sarr[2]);
            
            SAT res = new SAT(varCnt, clCnt, varInClCnt);

            for (int i = 0; i < clCnt; i++)
            {
                if (sr.EndOfStream)
                {
                    throw new Exception("Unexpected end of file");
                }

                res.addClausule(i, sr.ReadLine());
            }

            res.addWeights(sr.ReadLine());

            return res;
        }
    }
}
