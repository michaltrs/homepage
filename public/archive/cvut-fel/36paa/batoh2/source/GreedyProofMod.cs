using System;
using System.Collections.Generic;
using System.Text;

namespace Batoh_KH
{
    class GreedyProofMod : Batoh
    {       

        private int[] pos;



        public GreedyProofMod(string line) : base(line)
        {
            pos = new int[n];

            for (int i = 0; i < n; i++)
            {
                pos[i] = i;
            }
        }



        private void SortPriceWeight()
        {
            float[] cv = new float[n];            

            for (int i = 0; i < n; i++)
            {
                cv[i] = c[i] / (float) v[i];
            }
               
            Array.Sort(cv, pos);           
        }


        public override int Compute()
        {
            SortPriceWeight();

            int bestCost = 0;
            int bestCostPos = 0;
            int maxM = M;

            for (int i = n-1; i >= 0; i--)
            {
                if (v[pos[i]] <= M)  // vejde se do batohu
                {
                    x[pos[i]] = true;
                    cost += c[pos[i]];
                    M -= v[pos[i]]; 
                }
                else
                {
                    x[pos[i]] = false;
                }

                // hledam nejcenejsi vec
                if (maxM >= v[i] && bestCost < c[i]) 
                {
                    bestCost = c[i];
                    bestCostPos = i;
                }
            }

            // test zda je lepsi 1 nejcenejsi vec nebo GP
            if (bestCost > cost)
            {
                for (int i = 0; i < x.Length; i++)
                {
                    if (i == bestCostPos)
                        x[i] = true;
                    else
                        x[i] = false;
                }
                
                cost = bestCost;
            }
            return cost;
        }


        public override string ToString()
        {
            string res = String.Format("{0}\t{1}\t{2}\t", ID, n, cost);
            for (int i = 0; i < n; i++)
            {
                if (x[i])
                    res += "1 ";
                else
                    res += "0 ";
            }

            return res;
        }    
    }
}
