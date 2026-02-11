using System;
using System.Collections.Generic;
using System.Text;

namespace Batoh_Dyn
{

    // Podle kapacity batohu
    class Dyn : Batoh
    {
        private int[,] B;


        public Dyn(string input)
            : base(input)
        {
            // B = new int[n, M];
            B = (int[,]) Array.CreateInstance(typeof(int),n+1,M+1);
        }


        private void init()
        {
            for (int w = 0; w <= M; w++)
            {
                B[0,w] = 0;
            }

            for (int i = 0; i <= n; i++)
            {
                B[i, 0] = 0;
            }


            for (int i = 1; i <= n; i++)
            {
                for (int w = 1; w <= M; w++)
                {
                    if (v[i-1] <= w) // item i can be part of the solution
                    {
                        if (c[i-1] + B[i - 1, w - v[i-1]] > B[i - 1, w])
                        {
                            B[i, w] = c[i-1] + B[i - 1, w - v[i-1]];
                        }
                        else
                        {
                            B[i, w] = B[i - 1, w];
                        }
                    }
                    else
                    {
                        B[i, w] = B[i - 1, w]; // wi > w
                    }
                }
            }            
        }



        public override int Compute()
        {
            init();

            // zjistim vyslednou konfiguraci
            int pd = M;

            for (int i = n; i > 0; i--)
            {
                if (B[i, pd] == B[i-1, pd])
                {
                    x[i-1] = false;
                }
                else
                {
                    x[i-1] = true;
                    pd -= v[i - 1];
                }                
            }

            return B[n, M];

        }
   

        public override string ToString()
        {
            string res = String.Format("{0}\t{1}\t{2}\t", ID, n, B[n, M]);
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
