#include "40_floyd-warshall_algorithm.c"

int main() {
  /* Let us create the following weighted graph
          10
     (0)------->(3)
      |         /|\
    5 |          |
      |          | 1
     \|/         |
     (1)------->(2)
          3           */
  int graph[V][V] = {
      {0, 5, INF, 10}, {INF, 0, 3, INF}, {INF, INF, 0, 1}, {INF, INF, INF, 0}};

  // Print the solution
  floydWarshall(graph);
  return 0;
}