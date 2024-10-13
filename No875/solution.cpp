#include <iostream>
#include <vector>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

class Solution {
private:
    int divide(int dividend, int divisor) {
        return (dividend / divisor) + ((dividend % divisor) > 0);
    }

    int spentHours(vector<int>& piles, int speed) {
        int res = 0;
        for (auto& n : piles) {
            res += divide(n, speed);
        }

        return res;
    }
public:
    int minEatingSpeed(vector<int>& piles, int h) {
        int lo = 1, hi = 1;
        for (auto& n : piles) {
            hi = max(hi, n + 1);
        }

        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (spentHours(piles, mid) <= h) {
                hi = mid;
            } else {
                lo = mid + 1;
            }
        }

        return lo;
    }
};

////////////////////////////////////////////////////////////////////////////////

int main() {
    Solution s;

    // Test case 1
    vector<int> piles1 = {3, 6, 7, 11};
    cout << s.minEatingSpeed(piles1, 8) << endl; // 4

    // Test case 2
    vector<int> piles2 = {30, 11, 23, 4, 20};
    cout << s.minEatingSpeed(piles2, 5) << endl; // 30

    return 0;
}

////////////////////////////////////////////////////////////////////////////////

// 2^31 - 1 = 2147483647
