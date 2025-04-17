#include <iostream>
#include <vector>
#include <queue>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

class Solution {
public:
    vector<int> closestPrimes(int left, int right) {
        vector<int> isPrime(right + 1, true);
        isPrime[0] = false;
        isPrime[1] = false;

        for (int i = 2; i < right; i++) {
            if (!isPrime[i]) {
                continue;
            }
            for (int j = i + i; j <= right; j += i) {
                isPrime[j] = false;
            }
        }

        vector<int> res;
        int prev = 0;
        for (int i = left; i <= right; i++) {
            if (!isPrime[i]) {
                continue;
            }

            if (!prev) {
                prev = i;
                continue;
            }

            vector<int> curr = {prev, i};
            prev = i;

            if (!res.size()) {
                res = curr;
                continue;
            }

            if (curr[1] - curr[0] >= res[1] - res[0]) {
                continue;
            }

            res = curr;
        }

        if (!res.size() || res.size() == 1) {
            return {-1, -1};
        }

        return res;
    }
};

////////////////////////////////////////////////////////////////////////////////

int main() {
    Solution s;

    // test 1
    {
        vector<int> res = s.closestPrimes(19, 31);
        cout << "test: " << res[0] << " " << res[1] << endl;
    }
}
