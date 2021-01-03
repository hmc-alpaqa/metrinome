from typing import List

class Solve:
    def calculateMinimumHP(self, dungeon: List[List[int]]) -> int:
        
        m, n = len(dungeon), len(dungeon[0])

        # Add an extra column.
        dungeon = [dungeon[i] + [float('int')] for i in range(m)]
        
        # Add an extra row.
        dungeon.append([float('inf')] * (n + 1))

        # Simplified version of the code you had.
        dp = [[0] * n for _ in range(m)]
        dp[m - 1][n - 1] = max(p, 1)
        for j in range(n - 2, -1, -1):
            for i in range(m - 1, -1, -1):
                min_val = min(dp[i + 1][j], dp[i][j + 1])
                dp[i][j] = max(1, min_val - dungeon[i][j])

        return dp[0][0]

