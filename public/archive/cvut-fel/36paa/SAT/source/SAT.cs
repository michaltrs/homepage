using System;
using System.Collections.Generic;
using System.Text;

namespace SAT_SimAnneal
{
    /*
     * represent SAT (3SAT data structure)
     */
    class SAT
    {
        public enum t_setx {F, T, Rnd}

        private int[,] formule;
        private int[] w; // weights
        public bool[] x; // configuration

        public int actualGrant;
        public int var_count;
        private int cl_count;
        private int varcl_count;
        public int maxW = 0;


        public SAT(int var_count, int cl_count, int varcl_count)
        {
            formule = new int[cl_count,varcl_count];
            w = new int[var_count];
            x = new bool[var_count];

            this.var_count = var_count;
            this.cl_count = cl_count;
            this.varcl_count = varcl_count;
        }


        public void addClausule(int index, string line)
        {
            if (index > formule.GetLength(0))
            {
                throw new Exception("Index out of range");
            }            

            string[] lnArr = line.Split(' ');

            for (int i = 0; i < lnArr.Length; i++)
            {
                formule[index, i] = int.Parse(lnArr[i]);
            }
        }


        public void addClausule(int clIndex, int posInCl, int value)
        {
            if ((clIndex > formule.GetLength(0)) || posInCl > formule.GetLength(1))
            {
                throw new Exception("Index out of range");
            }

            formule[clIndex - 1, posInCl - 1] = value;
        }


        public void addWeights(string line)
        {
            string[] strArr = line.Trim().Split(' ');

            for (int i = 0; i < strArr.Length; i++)
            {
                w[i] = int.Parse(strArr[i]);
                if (w[i] > maxW)
                {
                    maxW = w[i];
                }
            }

            actualGrant = getGrant();
        }


        private int getCost()
        {
            int res = 0;

            for (int i = 0; i < var_count; i++)
            {
                if (x[i])
                    res += w[i];
            }

            return res;
        }


        private int getCost(bool[] x)
        {
            int res = 0;

            for (int i = 0; i < var_count; i++)
            {
                if (x[i])
                    res += w[i];
            }

            return res;
        }


        // cenova funkce
        public int getGrant()
        {
            int res = getCost();

            for (int i = 0; i < cl_count; i++)
            {
                bool cs = false;

                for (int j = 0; j < varcl_count; j++)
                {
                    int index = formule[i, j];

                    if (index < 0)
                        cs |= !x[-index - 1];
                    else
                        cs |= x[index - 1];
                }

                if (!cs)
                    res -= maxW;
            }
            return res;
        }


        // cenova funkce
        public int getGrant(bool[] x)
        {
            int res = getCost(x);

            for (int i = 0; i < cl_count; i++)
            {
                bool cs = false;

                for (int j = 0; j < varcl_count; j++)
                {
                    int index = formule[i, j];

                    if (index < 0)
                        cs |= !x[-index - 1];
                    else
                        cs |= x[index - 1];
                }

                if (!cs)
                    res -= maxW;
            }
            return res;
        }


        public bool isSolution()
        {
            for (int i = 0; i < cl_count; i++)
            {
                bool cs = false;

                for (int j = 0; j < varcl_count; j++)
                {
                    int index = formule[i, j];

                    if (index < 0)
                        cs |= !x[-index-1];
                    else
                        cs |= x[index-1];
                }

                if (!cs)
                    return false;
            }
            return true;
        }


        public int[] getWeights()
        {
            return (int[]) w.Clone();
        }

        public void setX(t_setx type)
        {
            Random rnd = new Random();

            switch (type)
            {
                case t_setx.T:
                    for (int i = 0; i < x.Length; i++)
                    {
                        x[i] = true;
                    }
                    break;

                case t_setx.F:
                    for (int i = 0; i < x.Length; i++)
                    {
                        x[i] = false;
                    }
                    break;

                case t_setx.Rnd:
                    
                    for (int i = 0; i < x.Length; i++)
                    {
                        x[i] = (rnd.NextDouble() > 0.5) ? true : false;
                    }
                    break;
            }
        }
       
    }
}
