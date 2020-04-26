int if_loop_func (int i) {

   int n[ 10 ]; 
   int j;
 
           
   for ( i = 0; i < 10; i++ ) {
      n[ i ] = i + 100;
      if(n[i] == 111) {
         return 3;
      } 
   }
   
   for (j = 4; j < 10; j++ ) {
      if (n[j] % j == 0) {
         return 43;
      }
   }
   return i;
}