#include<stdio.h>
#include<math.h>



 /* 0 - trojuhel jde sestrojit */
int jde_sestrojit ( int a, int b, int c) {
	
	if ( ((a + b) > c) && ((a + c) > b) && ((b + c) > a) ) 
		return ( 0 );
	else 	return ( 1 );
}


double obsah ( int a, int b, int c ) {
	double s;

	s = (a + b + c) / 2.;
	return ( sqrt( s *(s-a)*(s-b)*(s-c) ) );
}


int obvod ( int a, int b, int c )  {

	return ( a + b + c );
}


/* uhel alfa mezi stranou b,c -CZ v rad*/
double uhel (int a, int b, int c) {
	double cit,jm;
	
	cit = b*b + c*c - a*a;	
	jm = 2*b*c;

	return( acos(cit/jm) );
}


void printu(char* nazev, double hodnota) {
	int st, min;
	double sec,mind;

	hodnota = hodnota * 180 / M_PI;
	
	st = (int) hodnota;
	min = (int) ((hodnota - st) * 60);
	mind = (hodnota - st) * 60;
	sec = ((mind - min) * 60);

	printf("Uhel %s: %3d deg %2d'%05.2lf''\n",nazev,st,min,sec);
}


double rKveps (int a, int b, int c) {

	return (obsah(a,b,c)/(obvod(a,b,c)/2.));
}


double rKops(int a, int b, int c) {
	double cit, jm;
	
	cit = a*b*c;
	jm = 4 * obsah(a,b,c);
	
	return(cit/jm);
}


/* vyska Vc - CZ */
double vyska (int a, int b , int c) {

	return ( b * sin(uhel(a,b,c)) );
}

/* teznice Tc - CZ */
double teznice (int a, int b , int c) {

	return ( sqrt(0.5*b*b - 0.25*c*c +0.5*a*a) );
}


int main( int argc, char * argv[] )  {
	int a,b,c, i;	
	
	printf("\n");

	/* porovnani se 4, protoze nazev + 3 argumenty */
	if (argc != 4) {
		printf("Zadej velikost strany a: "); scanf("%d",&a);
		printf("Zadej velikost strany b: "); scanf("%d",&b);
		printf("Zadej velikost strany c: "); scanf("%d",&c);
	} else  {
		printf("Velikost strany a: %d\n",a = atoi(argv[1]));
		printf("Velikost strany b: %d\n",b = atoi(argv[2]));	
		printf("Velikost strany c: %d\n",c = atoi(argv[3]));
	}

	if ( jde_sestrojit(a,b,c) ) {
		printf("\nTojúhelník nelze sestrojit\n\n");
		return (255);
	}
	
	printf("\n");

	printu("alfa",uhel(a,b,c));
	printu("beta",uhel(b,c,a));
	printu("gama",uhel(c,a,b));

	printf("Obvod je: %22d.00\n",obvod(a,b,c));
	printf("Obsah je: %25.2lf\n",obsah(a,b,c));

	printf("Polomer kruznice vepsane je:  %-5.2lf\n",rKveps(a,b,c));
	printf("Polomer kruznice opsane je:   %-5.2lf\n",rKops(a,b,c));

	printf("Vyska Va:   %-5.2lf\n",vyska(b,c,a));
	printf("Vyska Vb:   %-5.2lf\n",vyska(c,a,b));
	printf("Vyska Vc:   %-5.2lf\n",vyska(a,b,c));

	printf("Teznice Ta:   %-5.2lf\n",teznice(b,c,a));
	printf("Teznice Tb:   %-5.2lf\n",teznice(c,a,b));
	printf("Teznice Tc:   %-5.2lf\n",teznice(a,b,c));
	
	printf("\n\n");

	return (0);
} 


