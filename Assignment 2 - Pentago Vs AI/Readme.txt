Example Performance of MiniMax and AlphaBeta Search Algorithms:

Maximum Branching Factor (b) = n_positions * n_blocks * n_directions = 36 * 4 * 2 = 288

AlphaBeta:
	Expanded Nodes:
	- Depth Limit 2 (d): 36
	- Depth Limit 3 (d): 273

	Best Case:
	- Time Complexity:  O(b^(d/2))
	- Space Complexity: O(b^(d/2))

	Worst Case:
	- Time Complexity:  O(b^d)
	- Space Complexity: O(b^d)

MiniMax:
	Expanded Nodes:
	- Depth Limit 2 (d): 36
	- Depth Limit 3 (d): 3402

	Best Case:
	- Time Complexity:  O(b^d)
	- Space Complexity: O(b^d)

	Worst Case:
	- Time Complexity:  O(b^d)
	- Space Complexity: O(b^d)

Number of Expanded nodes recorded with algorithm determining second move, after player turn '1/5 1r'