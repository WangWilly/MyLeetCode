#include <iostream>
#include <vector>
#include <queue>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

class Solution {
private:
    int divideCeil(int n) {
        return (n / 3) + ((n % 3) > 0);
    }
public:
    long long maxKelements(vector<int>& nums, int k) {
        priority_queue<int> pq(nums.begin(), nums.end());

        long long res = 0;
        for (int i = 0; i < k; i++) {
            int pick = pq.top();
            res += pick;
            pq.pop();
            pq.push(divideCeil(pick));
        }

        return res;
    }
};

////////////////////////////////////////////////////////////////////////////////

int main() {
    Solution s;

    // Test case 1
    vector<int> nums1 = {10, 20, 7};
    cout << s.maxKelements(nums1, 4) << endl; // 40

    // Test case 2
    vector<int> nums2 = {1, 2, 3, 4, 5};
    cout << s.maxKelements(nums2, 5) << endl; // 16

    // Test case 3
    vector<int> nums3 = {10, 10, 10, 10, 10};
    cout << s.maxKelements(nums3, 5) << endl; // 50

    // Test case 4
    vector<int> nums4 = {1, 10, 3, 3, 3};
    cout << s.maxKelements(nums4, 3) << endl; // 17

    return 0;
}
