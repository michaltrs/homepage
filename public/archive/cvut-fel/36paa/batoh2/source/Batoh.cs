using System;
using System.Collections.Generic;
using System.Text;

namespace Batoh_BB
{
    abstract class Batoh
    {        
        // input
        public int ID;
        public int n;
        protected int M;
        protected int[] v;
        protected int[] c;

        // output
        protected bool[] x;
        protected int cost = 0;


        public Batoh(string line)
        {
            string[] items = line.Split(' ');

            ID = int.Parse(items[0]);
            n = int.Parse(items[1]);
            M = int.Parse(items[2]);
            v = new int[n];
            c = new int[n];
            x = new bool[n];

            int pos = 3;
            for (int i = 0; i < n; i++)
            {
                v[i] = int.Parse(items[pos++]);
                c[i] = int.Parse(items[pos++]);
            }
        }
       

        public void printAll(bool eol)
        {            
            Console.Write(ID.ToString() + " " + n.ToString() + " " + cost.ToString());
            
            for (int i = 0; i < n; i++)
            {
                if (x[i]) Console.Write(" 1");
                else Console.Write(" 0");
            }

            if (eol) Console.WriteLine(); 
        }
        

        public abstract int Compute();

    }
}
