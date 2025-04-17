#include <iostream>
#include <vector>
#include <unordered_set>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

class Solution {
public:
    vector<int> resultsArray(vector<int>& nums, int k) {
        unordered_set<int> bugs;
        int curr = 0;
        for (int i = 0; i < k; i++) {
            if (nums[i] <= curr) {
                bugs.insert(i - 1);
            }

            curr = nums[i];
        }

        vector<int> res;
        if (bugs.size() == 0) {
            res.push_back(curr);
        } else {
            res.push_back(-1);
        }

        for (int i = k; i < nums.size(); i++) {
            if (nums[i] <= curr) {
                bugs.insert(i - 1);
            }

            curr = nums[i];
            bugs.erase(i - k);

            if (bugs.size() == 0) {
                res.push_back(curr);
            } else {
                res.push_back(-1);
            }
        }

        return res;
    }
};

////////////////////////////////////////////////////////////////////////////////

int main() {
    Solution s;

    // Test case 1
    {
        vector<int> nums = {1, 2, 3, 4, 3, 2, 5};
        int k = 3;
        vector<int> res = s.resultsArray(nums, k);
        for (int i = 0; i < res.size(); i++) {
            cout << res[i] << " ";
        }
        cout << endl;
    }

    // Test case 2
    {
        vector<int> nums = {2, 2, 2, 2, 2};
        int k = 4;
        vector<int> res = s.resultsArray(nums, k);
        for (int i = 0; i < res.size(); i++) {
            cout << res[i] << " ";
        }
        cout << endl;
    }

    // Test case 3
    {
        vector<int> nums = {3, 2, 3, 2, 3, 2};
        int k = 2;
        vector<int> res = s.resultsArray(nums, k);
        for (int i = 0; i < res.size(); i++) {
            cout << res[i] << " ";
        }
        cout << endl;
    }

    return 0;
}
