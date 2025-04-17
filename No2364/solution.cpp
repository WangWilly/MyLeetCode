#include <iostream>
#include <vector>
#include <map>
#include <queue>
#include <unordered_set>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

class Solution {
public:
    long long countBadPairs(vector<int>& nums) {
        map<int, unordered_set<int>> numIdxs;

        long long res = 0;
        for (int i = 0; i < nums.size(); i++) {
            auto it = numIdxs.lower_bound(nums[i]);
            if (it == numIdxs.end()) {
                numIdxs[nums[i]].insert(i);
                continue;
            }
            it = prev(it);
            for (;; it = prev(it)) {
                cout << "i: " << i << " it->first: " << (*it).first << " it->second: ";
                for (auto idx : (*it).second) {
                    cout << idx << " ";
                }
                cout << "n: " << i - (nums[i] - (*it).first) << endl;
                // bool have = (((*it).second.count(i - (nums[i] - (*it).first))));
                // cout << "have: " << have << endl;
                // res += have;
                if (it == numIdxs.begin()) {
                    break;
                }
                cout << "continue" << endl;
            }
            // numIdxs[nums[i]].insert(i);
        }

        return res;
    }
};

////////////////////////////////////////////////////////////////////////////////

int main() {
    Solution sol;
    vector<int> nums;

    nums = {4, 1, 3, 3};
    cout << sol.countBadPairs(nums) << endl;
};
