#include <iostream>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

class Solution {
private:
    long compute(int len, int idx, int num) {
        long res = 0;
        int lo = max(0, num - idx);
        res += long(num + lo) * long(num - lo + 1) / 2;
        int hi = max(0, num - (len - 1 - idx));
        res += long(num + hi) * long(num - hi + 1) / 2;

        return res - num;
    }

public:
    int maxValue(int n, int index, int maxSum) {
        maxSum -= n;

        int lo = 0, hi = maxSum; // the range (lo, hi] of the search domain
        while (lo < hi) {
            int mid = long(lo + hi + 1) / 2; // 1 for up shifting; normaly the result from divide is down shift
            long val = compute(n, index, mid); // the sum of the array

            if (val <= maxSum) { // maybe the answer, but we greedy
                lo = mid;
            } else {
                hi = mid - 1;
            }
        }

        return lo + 1;
    }
};

////////////////////////////////////////////////////////////////////////////////

int main() {
    Solution s;

    // Test case 1
    cout << s.maxValue(4, 2, 6) << endl; // 2

    // Test case 2
    cout << s.maxValue(6, 1, 10) << endl; // 3

    // Test case 3
    cout << s.maxValue(4, 0, 4) << endl; // 1

    // Test case 4
    cout << s.maxValue(6, 2, 931384943) << endl; // 155230825

    return 0;
}

////////////////////////////////////////////////////////////////////////////////

// 2^31 - 1 = 2147483647
