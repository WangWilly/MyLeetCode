#include <iostream>
#include <vector>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

class Solution {
private:
    int divide(int dividend, int divisor) {
        return (dividend / divisor) + ((dividend % divisor) > 0);
    }

    int sumDivide(vector<int>& nums, int divisor) {
        int res = 0;
        for (auto& n : nums) {
            res += divide(n, divisor);
        }

        return res;
    }
public:
    int smallestDivisor(vector<int>& nums, int threshold) {
        int lo = 1, hi = 1;
        for (auto& n : nums) {
            hi = max(hi, n + 1);
        }

        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (sumDivide(nums, mid) > threshold) {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }

        return lo;
    }
};

////////////////////////////////////////////////////////////////////////////////

int main() {
    Solution s;

    // Test case 1
    vector<int> nums1 = {1, 2, 5, 9};
    cout << s.smallestDivisor(nums1, 6) << endl; // 5

    // Test case 2
    vector<int> nums2 = {44, 22, 33, 11, 1};
    cout << s.smallestDivisor(nums2, 5) << endl; // 44

    return 0;
}

////////////////////////////////////////////////////////////////////////////////

// 2^31 - 1 = 2147483647
