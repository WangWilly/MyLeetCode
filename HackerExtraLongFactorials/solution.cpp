#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

class BigInt {
public:
    vector<int> nums;

    BigInt(vector<int> insert) {
        nums = insert;
    }

    BigInt(int n) {
        nums = {n};
    }
    
    BigInt() {
        nums = {0};
    }
    
    bool allZero(vector<int>& arr) {
        for(auto& n : arr) {
            if (n != 0) {
                return false;
            }
        }
        
        return true;
    }
    
    vector<int> add(vector<int> a, vector<int> b) {
        if (a.size() > b.size()) {
            return add(b, a);
        }
        
        a.insert(a.begin(), b.size() - a.size(), 0);
        
        vector<int> res, carry;
        for (int i = 0; i < a.size(); i++) {
            res.push_back((a[i] + b[i]) % 10);
            carry.push_back((a[i] + b[i]) / 10);
        }
        carry.push_back(0);
        
        if (allZero(carry)) {
            return res;
        }
        return add(res, carry);
    }
    
    BigInt times(BigInt t) {
        vector<int> res;
        
        for (int i = nums.size() - 1; i >= 0; i--) {
            vector<int> curr = {}, carry = {0};
            for (int j = t.nums.size() - 1; j >= 0; j--) {
                carry.push_back(nums[i] * t.nums[j] / 10);
                curr.push_back(nums[i] * t.nums[j] % 10);
            }
            reverse(curr.begin(), curr.end());
            reverse(carry.begin(), carry.end());
            vector<int> tmp = add(curr, carry);
            tmp.insert(tmp.end(), nums.size() - 1 - i, 0);
            res = add(res, tmp);
        }
        
        return res;
    }
    
    void print() {
        vectorPrint(nums);
    }

    void vectorPrint(vector<int>& v) {
        int i = 0;
        for (; i < v.size(); i++) {
            if (v[i] != 0) {
                break;
            }
        }
        for (; i < v.size(); i++) {
            cout << v[i];
        }
        cout << endl;
    }
};

void extraLongFactorials(int n) {
    BigInt res(1);
    
    for (int i = n; i >= 1; i--) {
        res = res.times(BigInt(i));
    }
    
    res.print();
}

////////////////////////////////////////////////////////////////////////////////

int main() {
    // Test case 1
    extraLongFactorials(25); // 15511210043330985984000000

    // Test case 2
    extraLongFactorials(45); // 119622220865480194561963161495657715064383733760000000000

    // Test case 3
    extraLongFactorials(4); // 24

    return 0;
}
