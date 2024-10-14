#include <iostream>
#include <vector>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

class Solution {
public:
    void pendPermu(vector<vector<int>>& res, vector<int>& nums, vector<bool>& visited, vector<int>& curr) {
        if (curr.size() == nums.size()) {
            res.push_back(curr);
            return;
        }

        int len = nums.size();
        for (int i = 0; i < len; i++) {
            if (visited[i]) {
                continue;
            }
            visited[i]=true;
            curr.push_back(nums[i]);
            pendPermu(res, nums, visited, curr);
            visited[i]=false;
            curr.pop_back();
        }
    }

    vector<vector<int>> permute(vector<int>& nums) {
        vector<vector<int>> res;
        vector<bool> visited(nums.size(), false);
        vector<int> curr;

        pendPermu(res, nums, visited, curr);

        return res;
    }
};

////////////////////////////////////////////////////////////////////////////////

int main() {
    Solution s;

    // Test case 1
    vector<int> nums1 = {1, 2, 3};
    vector<vector<int>> res1 = s.permute(nums1);
    for (auto& r : res1) {
        for (auto& n : r) {
            cout << n << " ";
        }
        cout << endl;
    }
    // [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

    // Test case 2
    vector<int> nums2 = {0, 1};
    vector<vector<int>> res2 = s.permute(nums2);
    for (auto& r : res2) {
        for (auto& n : r) {
            cout << n << " ";
        }
        cout << endl;
    }
    // [[0,1],[1,0]]

    // Test case 3
    vector<int> nums3 = {1};
    vector<vector<int>> res3 = s.permute(nums3);
    for (auto& r : res3) {
        for (auto& n : r) {
            cout << n << " ";
        }
        cout << endl;
    }
    // [[1]]

    return 0;
}

////////////////////////////////////////////////////////////////////////////////
