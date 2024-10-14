#include <algorithm>
#include <iostream>
#include <unordered_map>
#include <vector>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

class Solution {
public:
    vector<int> smallestRange(vector<vector<int>>& nums) {
        vector<vector<int>> groupRec;
        for (int i = 0; i < nums.size(); i++) {
            for (auto& n : nums[i]) {
                groupRec.push_back({n, i});
            }
        }

        sort(groupRec.begin(), groupRec.end());
        unordered_map<int, int> groupCount;
        groupCount[groupRec[0][1]]++;
        int i = 0, j = 0;
        vector<int> res = {-100000, 100000};

        while (j < groupRec.size()) {
            int g = 0;
            for (auto& p : groupCount) {
                g += (p.second > 0);
            }

            if (g < nums.size()) {
                if (j + 1 == groupRec.size()) {
                    break;
                }

                j++;
                groupCount[groupRec[j][1]]++;
                continue;
            }

            if (res[1] - res[0] > groupRec[j][0] - groupRec[i][0]) {
                res[1] = groupRec[j][0];
                res[0] = groupRec[i][0];
            }

            groupCount[groupRec[i][1]]--;
            i++;
        }

        return res;
    }
};

////////////////////////////////////////////////////////////////////////////////

int main() {
    Solution s;

    // Test case 1
    vector<vector<int>> nums1 = {
        {4, 10, 15, 24, 26},
        {0, 9, 12, 20},
        {5, 18, 22, 30},
    };
    vector<int> res1 = s.smallestRange(nums1);
    for (auto& r : res1) {
        cout << r << " ";
    }
    cout << endl;
    // 20 24

    // Test case 2
    vector<vector<int>> nums2 = {
        {1, 2, 3},
        {1, 2, 3},
        {1, 2, 3},
    };
    vector<int> res2 = s.smallestRange(nums2);
    for (auto& r : res2) {
        cout << r << " ";
    }
    cout << endl;
    // 1 1

    return 0;
}

////////////////////////////////////////////////////////////////////////////////

// 2^31 - 1 = 2147483647
