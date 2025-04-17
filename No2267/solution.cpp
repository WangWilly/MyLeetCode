#include <iostream>
#include <vector>
#include <queue>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

class Solution {
public:
    bool dfs(vector<vector<char>>& grid, int currR, int currC, int stack = 0) {
        if (currR >= grid.size() || currC >= grid[0].size()) {
            return false;
        }
        stack += grid[currR][currC] == '(' ? 1 : -1;
        if (stack < 0) {
            return false;
        }
        if (currR == grid.size() - 1 && currC == grid[0].size() - 1) {
            return stack == 0;
        }

        bool rightRes = dfs(grid, currR, currC + 1, stack);
        bool downRes = dfs(grid, currR + 1, currC, stack);

        right;
        return rightRes || downRes;
    }

    bool hasValidPath(vector<vector<char>>& grid) {
        return dfs(grid, 0, 0);
    }
};

////////////////////////////////////////////////////////////////////////////////

int main() {
    Solution s;

    // Test case 1
    {
        vector<vector<char>> grid = {
            {'(', ')'},
        };
        cout << s.hasValidPath(grid) << endl;
    }

    // Test case 2
    {
        vector<vector<char>> grid = {
            {'(', ')', ')', '(', ')', ')', ')'}
        };

        cout << s.hasValidPath(grid) << endl;
    }
}
