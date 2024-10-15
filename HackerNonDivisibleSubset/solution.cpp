#include <iostream>
#include <vector>
#include <unordered_map>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

int nonDivisibleSubset(int k, vector<int> s) {
    unordered_map<int, int> modMap;
    for (auto& n : s) {
        modMap[n % k]++;
    }
    // cout << "modMap: ";
    // for (auto& p : modMap) {
    //     cout << p.first << ":" << p.second << " ";
    // }
    // cout << endl;

    int res = 0;
    res += (modMap[0] > 0);
    for (int i = 1; i < k / 2 + 1; i++) {
        if (i == k - i) {
            continue;
        }
        // cout << "i: " << i << " k-i: " << k-i << endl;
        // cout << "modMap[i]: " << modMap[i] << " modMap[k-i]: " << modMap[k-i] << endl;
        res += max(modMap[i], modMap[k-i]);
    }
    
    if (k % 2 == 0) {
        res += (modMap[k/2] > 0);
    }
    
    return res;
}

////////////////////////////////////////////////////////////////////////////////

int main() {
    // Test case 1
    vector<int> s1 = {1, 7, 2, 4};
    cout << nonDivisibleSubset(3, s1) << endl; // 3

    // Test case 2
    vector<int> s2 = {278, 576, 496, 727, 410, 124, 338, 149, 209, 702, 282, 718, 771, 575, 436};
    cout << nonDivisibleSubset(7, s2) << endl; // 11

    // Test case 3
    vector<int> s3 = {19, 10, 12, 10, 24, 25, 22};
    cout << nonDivisibleSubset(4, s3) << endl; // 3

    // Test case 4
    vector<int> s4 = {1, 2, 3, 4, 5};
    cout << nonDivisibleSubset(1, s4) << endl; // 1

    return 0;
}