 #define PRINT_WALK

using System;
using System.Collections.Generic;
using System.Text;
using System.IO;


namespace Batoh_SimAnneal
{

    class SimAnneal : Batoh
    {
        double dT;
        double T0;
        double Tf;
        double equilibrium;


        int bestCost;
        bool[] best;
        Random rng;


        public void SetParam()
        {
            dT = 0.98;
            SetT0();
            Tf = 5;
            equilibrium = n;
        }
        

        public SimAnneal(string line)
            : base(line)
        {
            rng = new Random();
            SetParam();                      
        }


        public SimAnneal(string line, bool[] x)
            : base(line)
        {
            rng = new Random();
            SetParam();

            this.x = x;
            bestCost = ComputeCost(x);
            best = (bool[])x.Clone();            
        }



        public override int Compute()
        {
            #if PRINT_WALK
            StreamWriter sw = new StreamWriter("progress.txt");
            int step = 0;
            #endif

            double T = T0;

            while (T >= Tf)     // Frozen?
            {
                // Equilibrium ?
                for (int i = 0; i < equilibrium; i++)
                {
                    x = TryState(x,T);

                    if (IsBetter(x))
                    {
                        bestCost = ComputeCost(x);
                        best = (bool[])x.Clone();
                    }

                    #if PRINT_WALK
                    sw.WriteLine("{0}\t{1}", step++, ComputeCost(x));
                    #endif
                }

                T *= dT; // Cool
                
            }

            #if PRINT_WALK
            sw.Close();
            #endif

            return bestCost;
        }


        private bool[] TryState(bool[] state, double T)
        {
            bool[] newState;
            int sigma;

            do  // generate 1 acceptable state
            {
                int pos = rng.Next(state.Length);
                newState = (bool[])state.Clone();
                newState[pos] = !newState[pos];
            } while (!IsSolution(newState));

            if (IsBetter(newState))
            {
                return newState;
            }

            sigma = ComputeCost(state) - ComputeCost(newState);   

            if (rng.NextDouble() < Math.Exp(-sigma / T))
            {
                return newState;
            }
            else
            {
                return state;
            }

        }


        private int ComputeCost(bool[] state)
        {
            int res = 0;

            for (int i = 0; i < state.Length; i++)
            {
                if (state[i]) res += this.c[i];
            }

            return res;
        }

        private bool IsBetter(bool[] state)
        {
            return ComputeCost(state) > bestCost;
        }

        private bool IsSolution(bool[] state)
        {
            int w = 0;

            for (int i = 0; i < state.Length; i++)
            {
                if (state[i]) w += this.v[i];
            }

            return w <= M;
        }


        private void SetT0()
        {
            // M * suma(ceny) / (N * suma(vahy))

            int sumac = 0;
            int sumav = 0;

            for (int i = 0; i < c.Length; i++)
			{
                sumac += c[i];
                sumav += v[i];
			}

            T0 = (double)(this.M * sumac) / (double)(this.n * sumav);
        }

        public override string ToString()
        {
            // print parameters
            return String.Format("T0 = {0}, Tf = {1}, dT = {2}, equ = {3}", T0.ToString("0.##"), Tf, dT, equilibrium);
        }

    }
}
