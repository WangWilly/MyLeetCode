#include <iostream>
#include <vector>
#include <map>
#include <queue>
#include <unordered_set>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

class Solution {
public:
    int aMaxProfit(
        unordered_map<int, vector<int>>& toLeaf, 
        vector<int>& bLabel,
        vector<int>& amount,
        int curr, 
        int currLabel, 
        int currProfit
    ) {
        int resProfit = currProfit;
        if (bLabel[curr] == -1) {
            resProfit += amount[curr];
        } else {
            if (currLabel < bLabel[curr]) {
                resProfit += amount[curr];
            } else if (currLabel == bLabel[curr]) {
                resProfit += amount[curr] / 2;
            }
        }

        // is leaf
        if (!toLeaf.count(curr) || !toLeaf[curr].size()) {
            return resProfit;
        }

        int res = INT_MIN;
        for (auto& adj : toLeaf[curr]) {
            res = max(aMaxProfit(toLeaf, bLabel, amount, adj, currLabel + 1, resProfit), res);
        }

        return res;
    }

    int mostProfitablePath(vector<vector<int>>& edges, int bob, vector<int>& amount) {
        int n = amount.size();

        vector<vector<int>> g(n);
        for (auto& e : edges) {
            g[e[0]].push_back(e[1]);
            g[e[1]].push_back(e[0]);
        }

        vector<bool> visited(n, false);
        queue<int> traceToLeaf;
        traceToLeaf.push(0);
        unordered_map<int, vector<int>> toLeaf;
        unordered_map<int, int> toRoot;
        while (traceToLeaf.size()) {
            int curr = traceToLeaf.front();
            traceToLeaf.pop();
            visited[curr] = true;

            for (auto& adj : g[curr]) {
                if (visited[adj]) {
                    continue;
                }
                traceToLeaf.push(adj);
                toLeaf[curr].push_back(adj);
                toRoot[adj] = curr;
            }
        }

        vector<int> bLabel(n, -1);
        int currLabel = 0;
        while (true) {
            bLabel[bob] = currLabel++;

            if (bob == 0) {
                break;
            }
            bob = toRoot[bob];
        }

        return aMaxProfit(toLeaf, bLabel, amount, 0, 0, 0);
    }
};

////////////////////////////////////////////////////////////////////////////////

int main() {
    Solution sol;
    vector<vector<int>> edges = {{0, 1}, {1, 2}, {1, 3}, {3, 4}};
    int bob = 3;
    vector<int> amount = {-2, 4, 2, -4, 6};
    cout << sol.mostProfitablePath(edges, bob, amount) << endl;
    return 0;
}
