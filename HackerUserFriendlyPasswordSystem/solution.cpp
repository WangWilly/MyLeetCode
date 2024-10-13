#include <iostream>
#include <string>
#include <vector>
#include <unordered_set>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

class Solution {
public:
    unsigned long myPow(int base, int p, long mod) {
        unsigned long long res = 1;
        for (int i = 0; i < p; i++) {
            res = res * base;
        }
        
        return res % (unsigned long long)mod;
    }

    unordered_set<long> computeHash(long p, long mod, string plain) {
        long res = 0;
        int len = plain.size();
        for (int i = 0; i < len; i++) {
            res = (res + (((unsigned long)plain[i] * myPow(p, len - i - 1, mod)) % mod)) % mod;
        }
        
        unordered_set<long> resSet;
        resSet.insert(res);
        
        res = 0;
        for (int i = 0; i < len; i++) {
            res = (res + (((unsigned long)plain[i] * myPow(p, len - i, mod)) % mod)) % mod;
        }
        
        for (unsigned long i = 0; i < 256; i++) {
            long tmp = (((unsigned long)res + i) % mod);
            resSet.insert(tmp);
        }
        
        return resSet;
    }

    vector<int> authEvents(vector<vector<string>> events) {
        unordered_set<long> hash = {};
        unsigned long p = 131;
        unsigned long mod = 1e9 + 7;
        
        vector<int> res;
        for (auto& e : events) {
            if (e[0] == "setPassword") {
                hash = computeHash(p, mod, e[1]);
                continue;
            }
            
            res.push_back(hash.count(stol(e[1])));
        }
        
        return res;
    }
};

////////////////////////////////////////////////////////////////////////////////

int main() {
    Solution s;

    // Test case 1
    vector<vector<string>> events1 = {
        {"setPassword", "1"},
        {"setPassword", "2"},
        {"setPassword", "3"},
        {"authorize", "49"},
        {"authorize", "50"},
    };
    vector<int> res1 = s.authEvents(events1);
    for (auto& r : res1) {
        cout << r << " ";
    }
    cout << endl;
    /**
        0
        0
    */

    // Test case 2
    /**
        setPassword a
        authorize 97
        authorize 12756
        authorize 12804
        authorize 12829
        authorize 12772
        authorize 12797
        authorize 98
    */
    vector<vector<string>> events2 = {
        {"setPassword", "a"},
        {"authorize", "97"},
        {"authorize", "12756"},
        {"authorize", "12804"},
        {"authorize", "12829"},
        {"authorize", "12772"},
        {"authorize", "12797"},
        {"authorize", "98"},
    };
    vector<int> res2 = s.authEvents(events2);
    for (auto& r : res2) {
        cout << r << " ";
    }
    cout << endl;
    /**
        1
        1
        1
        1
        1
        1
        0
    */


    // Test case 3
    vector<vector<string>> events3 = {
        {"setPassword", "cAr1"},
        {"authorize", "223691457"},
        {"authorize", "303580761"},
        {"authorize", "100"},
        {"setPassword", "d"},
        {"authorize", "100"},
    };
    vector<int> res3 = s.authEvents(events3);
    for (auto& r : res3) {
        cout << r << " ";
    }
    cout << endl;
    /**
        1
        1
        0
        1
    */

    return 0;
}

////////////////////////////////////////////////////////////////////////////////

// 2^31 - 1 = 2147483647          ~ 10^9
// 2^63 - 1 = 9223372036854775807 ~ 10^18
// 1e9 + 7  = 1000000007
// 131^8    = 86730203469006241   ~ 8 * 10^16
