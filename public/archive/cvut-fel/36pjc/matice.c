/* program matice - napsal Michal Trs

   vstup - stdin
   vystup - stdout

  stderr 0 - OK
	 1 - chyba na vstupu
	 2 - singularni matice

*/



#include <stdlib.h>
#include <string.h>

#define EPSILON 0.01

int size;
double **matrix, **matrixI = NULL, **matrixE = NULL;
double d; /* determinant vstupni matice */

int getMatrix(void) /* 0 - vstup ok, 1 - spatny pocet radku, 2 - malo sloupcu*/
{
  char *s,tmpcnt[100], tmp[100];
  double d;  
  int i,j,count=1;

  if (!gets(tmp)) return (1); /*nactu prvni radku*/
  strcpy(tmpcnt,tmp);
    
  s = strtok(tmpcnt,","); /*vezmu prvni polozku, proto count = 1*/
  
  while (strtok(NULL,",") != NULL) /*pocitam kolik mam vyhradit pameti*/
    count++;

  /*alokace 2D pole*/
  matrix = (double**) malloc( count*sizeof(double*) );

  for (i=0; i < count; i++)
   matrix[i] = (double*) malloc( count*sizeof(double) );
   

  for (i=0; i < count; i++)
    {
      s = strtok(tmp,",");      
      
      for (j=0; j < (count); j++)
      {
        matrix[i][j] = atof(s);
        if ( (count-1) != j ) if ((s = strtok(NULL,",")) == NULL) { /*nacteni dalsi polozky na radku */
           for (i = 0; i < size; i++) free (matrix[i]);
           free(matrix);
           return (2);   
        }
      }
      
      if ( (count-1) != i ) gets(tmp) ;
      if (!strcmp(tmp,"")) { /*nacteni dalsiho radku*/
           for (i = 0; i < size; i++) free (matrix[i]);
           free(matrix);
           return (1);
      }
    }
  size = count;
  return (0);
}

int allocMatIE(void) 
{
  int i;

  matrixI = (double**) malloc(size * sizeof(double*));
  matrixE = (double**) malloc(size * sizeof(double*));
  for (i=0; i < size; i++) {
    matrixI[i] = (double*) malloc(size * sizeof(double));
    matrixE[i] = (double*) malloc(size * sizeof(double));
  }
}


int freeMatrix(void)
{
  int i;
  
  for (i = 0; i < size; i++) {
    free (matrix[i]);
    free (matrixI[i]);
    free (matrixE[i]);
  }  
  free (matrix);
  free (matrixE);
  free (matrixI);
  matrix = NULL;    
  matrixE = NULL;    
  matrixI = NULL;    
  size = 0;  
  return (0);
}

void printm(int size, double **matrix) 
{
  int i,j;  
  for (i=0; i < size; i++) {
    for (j=0; j < size; j++)
      printf("%-7.2lf\t",matrix[i][j]);
    printf("\n");
  }
}


int multiply(void)
{
  int i,j,k;
  double sum;  
  
  for(i=0; i < size; i++) /*posun po radcich*/
    for(j=0; j < size; j++) { /*posun po sloupcich v matice I a E*/
      sum = 0.0;
      for(k=0; k < size; k++)
        sum += matrix[i][k] * matrixI[k][j];      
      matrixE[i][j] = sum;
    }    
}


double det(double **mat, int s) {
     double **subDet, sum=0, zn;
     int i,m,r,sl;
     
     if ( s == 1 ) 
        return (mat[0][0]); 
     else if ( s == 2 ) {
          return ( (mat[0][0] * mat [1][1]) - (mat[0][1] * mat[1][0]) );
     } 
     else { /*rekurze*/
          
          /*alokace pole pro subdeterminant*/
          subDet = (double**) malloc((s-1) * sizeof(double*));
          for (m = 0; m < (s-1); m++) subDet[m] = (double*) malloc((s-1) * sizeof(double));          

          for (i = 0; i < s; i++) { /*pro kazdou radku det, spocitel subdet*/
                       
              /* naplneni matice */
              for (r = 0; r < s; r++) {         
                  if ( r == i ) continue; /* tento radek vyskrtnu */
          
                  for (sl = 1; sl < s; sl++) {
                  
                      if ( r < i ) subDet[r][sl-1] = mat[r][sl];
                      else subDet[r-1][sl-1] = mat[r][sl];
                  }
              }
              
              zn = ( i % 2 ) ? -1.0 : 1.0;
              sum += mat[i][0] * zn * det(subDet,s-1);
                       
          }
              
          /* uvolneni pameti po subdet */
          for (m = 0; m < (s-1); m++) free (subDet[m]);
          free(subDet);
          
          return (sum);
     }
}



void InvMatrix(void) 
{
     double **dop, zn;
     int i,j,m,r,sl;
     
     if (size == 1) { 
              matrixI[0][0] = 1/matrix[0][0];
              return ;
     }

     /*alokace pole pro doplnky*/
     dop = (double**) malloc((size-1) * sizeof(double*));
     for (m = 0; m < (size-1); m++) dop[m] = (double*) malloc((size-1) * sizeof(double));          

     for (i = 0; i < size; i++)  /*pro kazdou radku a sloupec det, spocitam subdet*/
          for (j = 0; j < size; j++)    {
              
              /* naplneni matice */
              for (r = 0; r < size; r++) {         
                  if ( r == i ) continue; /* tento radek vyskrtnu */
          
                  for (sl = 0; sl < size; sl++) {
                      if ( sl == j ) continue; /*tento sloupec vyskrtnu */
                      
                      if ( (r<i) && (sl<j) ) dop[r][sl] = matrix[r][sl];
                      else if ( (r<i) && (sl>j) ) dop[r][sl-1] = matrix[r][sl];
                      else if ( (r>i) && (sl<j) ) dop[r-1][sl] = matrix[r][sl];                      
                      else dop[r-1][sl-1] = matrix[r][sl];
                  }
              }
              
              /* vlastni vypocet */
              zn = ( (i+j) % 2 ) ? -1.0 : 1.0;
              matrixI[j][i] =  zn / d * det(dop,size-1);
                       
          }
              
     /* uvolneni pameti po subdet */
     for (m = 0; m < (size-1); m++) free(dop[m]);
     free(dop);


}


void help(void)
{
  printf("\nProgram slouzi k vypoctu inversni matice\n");
	printf("Autor programu: Michal Trs, trsm12@fel.cvut.cz, ICQ: 121560538\n\n");
	printf("Zadana matice musi byt ctvercova\n");
	printf("jako odelovac pouzijte , (carku)\n");
}


int main (int argc, char * argv[]) /* vraci 0-OK, 1-chyba na vstupu, 2-singularni matice*/
{
 int stat = 0;

  if (argc > 1) 
    if (  (!strcmp(argv[1],"-h")) || (!strcmp(argv[1],"--help")) ) {
      help();
      return (1);
    }
     
  stat = getMatrix();
  if (stat != 0 ) { /*nacteni matice*/
    printf("Chyba v zadani. Pro napovedu pouzijte -h\n");
    return(1);
  }
  allocMatIE(); /*alokace pameti pro matici I a E*/
  
  d = det(matrix,size);    
  if ( (d < EPSILON) && (d > -EPSILON) ) {
    printf("Zadana matice je singularni. Inversni matice neexistuje\n");
    return (2);
  } 
      
  InvMatrix();
  printf("\nInversni matice:\n");
  printm(size,matrixI);
  
  multiply();
  printf("\nKontrolni matice:\n");
  printm(size,matrixE);
  printf("\n");
      
  freeMatrix(); /*uvolnim pamet od vsech matic*/
  return (0);
}
