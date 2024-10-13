#include <iostream>
#include <vector>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

class Solution {
public:
    int findKthPositive(vector<int>& arr, int k) {
        int len = arr.size();
        if (arr.back() - len == 0) {
            return arr.back() + k;
        }
        arr.insert(arr.begin(), 0);

        int lo = -1, hi = len; // (]
        while (lo < hi) {
            int mid = (lo + hi + 1) / 2;
            if (arr[mid] - (mid) < k) {
                lo = mid;
            } else {
                hi = mid - 1;
            }
        }

        return arr[hi] + (k - (arr[hi] - hi));
    }
};

////////////////////////////////////////////////////////////////////////////////

int main() {
    Solution s;

    // Test case 1
    vector<int> arr1 = {2, 3, 4, 7, 11};
    cout << s.findKthPositive(arr1, 5) << endl; // 9

    // Test case 2
    vector<int> arr2 = {1, 2, 3, 4};
    cout << s.findKthPositive(arr2, 2) << endl; // 6

    return 0;
}
