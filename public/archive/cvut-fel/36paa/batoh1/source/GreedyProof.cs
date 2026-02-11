using System;
using System.Collections.Generic;
using System.Text;

namespace PAA_batoh1
{
    class GreedyProof : Batoh
    {       

        private int[] pos;



        public GreedyProof(string line) : base(line)
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
            }
            return cost;
        }

    }
}
