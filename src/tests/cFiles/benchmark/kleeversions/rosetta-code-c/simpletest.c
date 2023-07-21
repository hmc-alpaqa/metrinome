int calc(int n, int m)
{
  int q = 0;
  int p = 1;
	for (int k = m; k <= n; k++) {
		q = q+k;
		if (q < 15){
      p = p+q;
    }

  }
  return p-q;
}
