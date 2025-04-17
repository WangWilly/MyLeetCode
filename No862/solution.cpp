#include <iostream>
#include <vector>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

class Solution {
public:
    bool hasSubArrVal(vector<int>& acc, int winLen, int k) {
        for (int i = winLen - 1; i < acc.size(); i++) {
            int val = 0;
            if (i - winLen == -1) {
                val = acc[i];
            } else {
                val = acc[i] - acc[i - winLen];
            }

            if (val >= k) {
                return true;
            }
        }

        return false;
    }

    int shortestSubarray(vector<int>& nums, int k) {
        int res = -1;

        vector<int> acc(nums.size(), 0);
        for (int i = 0, curr = 0; i < nums.size(); i++) {
            curr += nums[i];
            acc[i] = curr;
        }

        int l = 1, r = nums.size();
        while (l < r) {
            int mid = (l + r) / 2;
            cout << "l: " << l << ", r: " << r << ", mid: " << mid << endl;
            if (hasSubArrVal(acc, mid, k)) {
                res = mid;
                r = mid;
                continue;
            }

            l = mid + 1;
        }

        if (hasSubArrVal(acc, l, k)) {
            return l;
        }

        return res;
    }
};

////////////////////////////////////////////////////////////////////////////////

int main() {
    Solution s;

    // // Test case 1
    // {
    //     vector<int> nums = {1};
    //     int k = 1;
    //     cout << s.shortestSubarray(nums, k) << endl;
    // }

    // // Test case 2
    // {
    //     vector<int> nums = {1, 2};
    //     int k = 4;
    //     cout << s.shortestSubarray(nums, k) << endl;
    // }

    // // Test case 3
    // {
    //     vector<int> nums = {2, -1, 2};
    //     int k = 3;
    //     cout << s.shortestSubarray(nums, k) << endl;
    // }

    // Test case 4
    {
        vector<int> nums = {44, -25, 75, -50, -38, -42, -32, -6, -40, -47};
        int k = 19;
        cout << s.shortestSubarray(nums, k) << endl;
    }
}

////////////////////////////////////////////////////////////////////////////////

// 2^31 - 1 = 2147483647
