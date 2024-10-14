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

////////////////////////////////////////////////////////////////////////////////
// Time limit exceeded, but the solution is correct

/**
class Solution {
private:
    unordered_map<int, unordered_map<int, pair<vector<int>, unordered_set<int>>>> mem;

    pair<vector<int>, unordered_set<int>> rangeCompute(map<int, unordered_set<int>>& groupMap, int& g, map<int, unordered_set<int>>::iterator lo, map<int, unordered_set<int>>::reverse_iterator hi) {
        if (mem.count(lo->first) && mem[lo->first].count(hi->first)) {
            return mem[lo->first][hi->first];
        }

        if (lo->first == hi->first) {
            mem[lo->first][lo->first] = {{lo->first, lo->first}, lo->second};
            return mem[lo->first][lo->first];
        }

        pair<vector<int>, unordered_set<int>> resL;
        if (next(hi, 1) != groupMap.rend()) {
            resL = rangeCompute(groupMap, g, lo, next(hi, 1));
        }

        pair<vector<int>, unordered_set<int>> resR;
        if (next(lo, 1) != groupMap.end()) {
            resR = rangeCompute(groupMap, g, next(lo, 1), hi);
        }

        if (resL.second == resR.second && resL.second.size() == g) {
            int lenL = resL.first[1] - resL.first[0];
            int lenR = resR.first[1] - resR.first[0];
            if (lenL <= lenR) {
                mem[lo->first][hi->first] = resL;
            } else {
                mem[lo->first][hi->first] = resR;
            }
            
            return mem[lo->first][hi->first];
        }

        if (resL.second.size() == g) {
            mem[lo->first][hi->first] = resL;
            return mem[lo->first][hi->first];
        }

        if (resR.second.size() == g) {
            mem[lo->first][hi->first] = resR;
            return mem[lo->first][hi->first];
        }

        unordered_set<int> uni(resL.second.begin(), resL.second.end());
        uni.insert(resR.second.begin(), resR.second.end());
        mem[lo->first][hi->first] = {{lo->first, hi->first}, uni};
        return mem[lo->first][hi->first];
    }
public:
    vector<int> smallestRange(vector<vector<int>>& nums) {
        map<int, unordered_set<int>> groupMap;
        for (int i = 0; i < nums.size(); i++) {
            for (int j = 0; j < nums[i].size(); j++) {
                groupMap[nums[i][j]].insert(i);
            }
        }
        auto lo = groupMap.begin();
        auto hi = groupMap.rbegin();

        int g = nums.size();
        auto res = rangeCompute(groupMap, g, lo, hi);

        return res.first;
    }
};
*/
