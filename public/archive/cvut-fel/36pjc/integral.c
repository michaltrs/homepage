/* PJC - uloha3 
   resini ulohy: http://moon.felk.cvut.cz/~xvagner/pjc/du/du10.html
   Zadani neni zcela zrejme, jestli se ma zadavat velikost kroku, nebo pocet kroku jak je videt v priklade
   Implementoval jsem funkci ktere se zada pocet kroku
   funkce pro reseni urciteho integralu numerickou metodou a testovaci program
   Michal Trs, trsm1@fel.cvut.cz
*/


double kubic(double x) {return x*x*x;}

typedef enum {DOLNI_MEZ, HORNI_MEZ, LICHOBEZNIK} tAPRM;



double numint(double dm, double hm, int kroku, double (*func)(double), tAPRM typ) {
    double sum=0 ,i, krok, y1,y2;
    
    if (dm>hm) {i=dm;dm=hm;hm=i;}
    krok = (hm-dm) / kroku;
        
    for (i=dm; i<hm; i+=krok) {
        y1 = func(i);
        y2 = func(i+krok);
        switch (typ) {
             case DOLNI_MEZ:   sum += krok * ((y1<y2) ? y1 : y2);
                               break;
             case HORNI_MEZ:   sum += krok * ((y1<y2) ? y2 : y1);
                               break;
             case LICHOBEZNIK: sum += krok * ((y1<y2) ? y1 : y2) /* mensi obdelnik */
                                   + ((y1-y2) * ((y1>y2) ? 1.0 : -1.0) * krok * 0.5); /* trojuhulnik */
                               break;        
        }
    }
    
    return sum;
}




int main(int argc, char *argv[]) {
       double dm, hm, sh, res;
       int kroku;
       
       
        /* Vypis napovedy. */
        if ( (argc>=2) &&   ( (!strcmp(argv[1], "-h")) || (!strcmp(argv[1], "--help")) ) ) {
           printf("funkce pro reseni urciteho integralu numerickou metodou + testovaci program\n");
           printf("vstupni hodnoty se zadavaji z klavesnice\n");
           printf("Vypracoval Michal Trs");
           return 0; 
        }

       
        printf("Dolni mez: ");scanf("%lf",&dm);
        printf("Horni mez: ");scanf("%lf",&hm);    
        printf("Pocet kroku: ");scanf("%d",&kroku);
        printf("Spravna hodnota: ");scanf("%lf",&sh);
  
//         dm=-5;       
//         hm=5;
//         kroku=100;
//         sh=37500;     
       
       
       printf("Dolni odhad: %.2f, chyba: %5.2f%%\n",res=numint(dm,hm,kroku,kubic,DOLNI_MEZ),((res > sh) ? res-sh : sh-res) / sh * 100);
       printf("Horni odhad: %.2f, chyba: %5.2f%%\n",res=numint(dm,hm,kroku,kubic,HORNI_MEZ),((res > sh) ? res-sh : sh-res) / sh * 100);
       printf("Lichobeznikova metoda: %.2f, chyba: %5.2f%%\n",res=numint(dm,hm,kroku,kubic,LICHOBEZNIK),((res > sh) ? res-sh : sh-res) / sh * 100);
       
     return 0; 
} 
