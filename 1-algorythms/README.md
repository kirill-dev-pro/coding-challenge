# Alg excercise:

Have the function `get_lcs(arr)` take the array of integers stored in arr and return the length of the longest consecutive subsequence (LCS). An LCS is a sub-array of the original array where the numbers are in sorted order, from lowest to highest, and are in a consecutive, increasing order. The sequence does not need to be contiguous (monotonically increasing) and there can be several different subsequences.

Create a comprehensive list of unit tests to cover this functionality.

Here are few examples to illustrate the logic of LCS:

```
For input [], it should return 0
For input [0], it should return 1
For input [0, 1, 2, 3, 4], it should return 5, which is the length of array, since the whole array is an LCS
For input [3, 10, 1000], it should return 3, which is the length of array, since whole array is an LCS (just not monotonic)
For input [4, 3, 2, 1, 0], it should return 1, as there are no multi-element LCS sequences, because whole array is descending sequence
For input [1000, 10, 3], it should return 1, as there are no multi-element LCS sequences, because whole array is descending sequence (just not monotonic)
For input [1, 1, 1, 1], it should return 4, as in this assignment, 'increasing' means 'greater or equal'
For input [1, 1, 1, 1, 0], it should return 4 again, as length of [1, 1, 1, 1] is greater than length of [0]
For input [4, 3, 8, 1, 2, 6, 100, 9], it should return 4, as length of [1, 2, 6, 100] is greater than length of [3, 8]
For input [-10, -10, -9, -10, 1000], it should return 3, as length of [-10,-10,-9] is greater than length of [-10, 1000]
```
