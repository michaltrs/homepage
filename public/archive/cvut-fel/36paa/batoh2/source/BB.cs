using System;
using System.Collections.Generic;
using System.Text;

namespace Batoh_BB
{
    class BB : Batoh
    {
        private int actCost;
        private int actWeigt;
        private bool[] actX;

        private bool foundSolution = false;



        public BB(string input) : base(input)
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

            // oøezávání shora (pøekroèení kapacity batohu)
            // vec se uz do batohu nevejde, nema vyznam pridavat dal + vec vyndam
            if (actWeigt < 0)
            {
                actX[index] = false;
                actWeigt += v[index];
                actCost -= c[index];
                return;
            }

            // oøezávání zdola (stávající øešení nemùže být lepší než nejlepší dosud nalezené)
            // nejvysi mozna cena teto konfigurece
            if (foundSolution)
            {
                int maxCost = 0;

                for (int i = 0; i < n; i++)
                {
                    if (i < index)
                    {
                        if (actX[i]) maxCost += c[i];
                    }
                    else
                    {
                        maxCost += c[i];
                    }                     
                }

                if (maxCost < cost)
                {
                    actX[index] = false;
                    actWeigt += v[index];
                    actCost -= c[index];
                    return;
                }
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
                foundSolution = true;
            }

            // odeberu vec index z batohu
            actX[index] = false;
            actWeigt += v[index];
            actCost -= c[index];

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
