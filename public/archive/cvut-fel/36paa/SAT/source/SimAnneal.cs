//#define PRINT_WALK

using System;
using System.Collections.Generic;
using System.Text;
using System.IO;


namespace SAT_SimAnneal
{

    class SimAnneal
    {
        double dT;
        double T0;
        double Tf;
        double equilibrium;

        MPFormatInputReader ir;
        SAT si;

        int bestGrant = int.MinValue;        
        bool[] best;
        Random rng;
        int[] w; // weights of each variable

        bool solutionFound = false;
        int solutionCost;
        bool[] solutionConf;


        public void SetParam(double T0_k, int Tf, double dT, double equ_k)
        {
            this.dT = dT;
            this.T0 = T0_k * si.var_count * si.maxW;
            this.Tf = Tf;
            this.equilibrium = equ_k * si.var_count;
        }


        public SimAnneal(string fileName) : this(fileName, 1,1,0.98,1)
        {
        }


        public SimAnneal(string fileName, double T0_k, int Tf, double dT, double equ_k)
        {
            rng = new Random();
            ir = new MPFormatInputReader(fileName);
            si = ir.ReadAll();
            w = si.getWeights();
            si.setX(SAT.t_setx.F);

            SetParam(T0_k, Tf, dT, equ_k);
        }


        public int Compute()
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
                    si.x = TryState(si.x, T);

                    si.actualGrant = si.getGrant();

                    if (si.actualGrant > bestGrant)
                    {
                        bestGrant = si.actualGrant;
                        best = (bool[])si.x.Clone();                        
                    }

                    if (si.isSolution())
                    {
                        solutionFound = true;
                        solutionCost = si.actualGrant;
                        solutionConf = (bool[])si.x.Clone();
                    }

#if PRINT_WALK
                    sw.WriteLine("{0}\t{1}", step++, si.getGrant());
#endif
                }

                T *= dT; // Cool

            }

#if PRINT_WALK
            sw.Close();
#endif

            return solutionCost;
        }


        private bool[] TryState(bool[] state, double T)
        {
            int sigma;

            // generate new state
            bool[] newState = (bool[])state.Clone();
            int pos = rng.Next(state.Length);
            newState[pos] = !newState[pos];

            int ncg = si.getGrant(newState);                  

            sigma = si.actualGrant - ncg;

            // is better?
            if (sigma < 0)
                return newState;

            // is worst
            if (rng.NextDouble() < Math.Exp(-sigma / T))
                return newState;
            else
                return state;
        }


        public override string ToString()
        {
            // print parameters
            // return String.Format("T0 = {0}, Tf = {1}, dT = {2}, equ = {3}", T0.ToString("0.##"), Tf, dT, equilibrium);

            string res;

            // print best solution
            if (solutionFound)
            {
                res = "Variable conf.:";

                for (int i = 0; i < solutionConf.Length; i++)
                    res += solutionConf[i] ? " T" : " F";

                res += Environment.NewLine;
                res += String.Format("Cost: {0}", solutionCost);

                double relerr = (double)(ir.BFCost - solutionCost) / (double)ir.BFCost * 100;

                res += Environment.NewLine;
                res += String.Format("From Best: {0} ({1}%)", ir.BFCost - solutionCost, relerr.ToString("0.##"));
            }
            else
            {
                res = "NF";
            }

            return res;            
        }


        public double getRelErr()
        {
            return (double)(ir.BFCost - solutionCost) / (double)ir.BFCost;
        }

    }
}
