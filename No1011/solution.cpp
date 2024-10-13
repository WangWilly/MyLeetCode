#include <iostream>
#include <vector>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

class Solution {
private:
    int shipDays(vector<int>& weights, int cap) {
        int curr = 0;
        int res = 0;

        for (auto& w : weights) {
            if (curr + w > cap) {
                curr = w;
                res++;
                continue;
            }
            curr += w;
        }

        return res + (curr > 0);
    }
public:
    int shipWithinDays(vector<int>& weights, int days) {
        int lo = 0, hi = 0;
        for (auto& w : weights) {
            lo = max(lo, w);
            hi += w;
        }

        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (shipDays(weights, mid) > days) {
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
    vector<int> weights1 = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    cout << s.shipWithinDays(weights1, 5) << endl; // 15

    // Test case 2
    vector<int> weights2 = {3, 2, 2, 4, 1, 4};
    cout << s.shipWithinDays(weights2, 3) << endl; // 6

    // Test case 3
    vector<int> weights3 = {1, 2, 3, 1, 1};
    cout << s.shipWithinDays(weights3, 4) << endl; // 3

    return 0;
}

////////////////////////////////////////////////////////////////////////////////

// 2^31 - 1 = 2147483647
