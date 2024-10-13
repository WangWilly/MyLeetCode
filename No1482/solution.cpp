#include <iostream>
#include <vector>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

class Solution {
private:
    bool ableToMake(vector<int>& bloomDay, int day, int m, int k) {
        int b = 0;
        int c = 0;
        for (auto& bd : bloomDay) {
            if (bd > day) {
                c = 0;
                continue;
            }

            c++;
            if (c == k) {
                b++;
                c = 0;
            }
        }

        return b >= m;
    }

public:
    int minDays(vector<int>& bloomDay, int m, int k) {
        if (bloomDay.size() < (unsigned long) m * k) {
            return -1;
        }

        int lo = 1, hi = 1;
        for (auto& n : bloomDay) {
            hi = max(hi, n + 1);
        }

        while (lo < hi) {
            int mid = (lo + hi) / 2;

            if (ableToMake(bloomDay, mid, m, k)) {
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
    vector<int> bloomDay1 = {1, 10, 3, 10, 2};
    cout << s.minDays(bloomDay1, 3, 1) << endl; // 3

    // Test case 2
    vector<int> bloomDay2 = {1, 10, 3, 10, 2};
    cout << s.minDays(bloomDay2, 3, 2) << endl; // -1

    // Test case 3
    vector<int> bloomDay3 = {7, 7, 7, 7, 12, 7, 7};
    cout << s.minDays(bloomDay3, 2, 3) << endl; // 12

    return 0;
}

////////////////////////////////////////////////////////////////////////////////

// 2^31 - 1 = 2147483647
