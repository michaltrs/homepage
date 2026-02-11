using System;
using System.Collections.Generic;
using System.Text;

namespace PAA_batoh1
{
    class BruteForce : Batoh
    {
        private int actCost;
        private int actWeigt;
        private bool[] actX;


        public BruteForce(string line) : base(line)
        {
            actX = new bool[n];
            actCost = 0;
            actWeigt = M;
        }
        
        public override int Compute()
        {
            for (int i = 0; i < n; i++)
            {
                findSolution(i);
            }
            return cost;          
        }
        


        private void findSolution(int index) 
        {
            // vlozim vec na pozici index do batohu
            actX[index] = true;
            actWeigt -= v[index];
            actCost += c[index];

            // vec se uz do batohu nevejde, nema vyznam pridavat dal + vec vyndam
            if (actWeigt < 0)
            {
                actX[index] = false;
                actWeigt += v[index];
                actCost -= c[index];
                return;
            }

            // rekurzivne hledam dalsi reseni
            for (int i = index + 1; i < n; i++)
                findSolution(i);
          
            // zkontroluju jestli jsem nasel nove nejlepsi reseni
            if (actCost >= cost)
            {
                cost = actCost;
                M = actWeigt;
                x = (bool[])actX.Clone();
            }

            // odeberu vec index z batohu
            actX[index] = false;
            actWeigt += v[index];
            actCost -= c[index];
        }
    }
}
