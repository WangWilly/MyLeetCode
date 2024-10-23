#include <iostream>
#include <vector>
#include <string>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

int digitLen(unsigned long x) {
    int res = 0;
    while (x > 0) {
        res++;
        x /= 10;
    }
    return res;
}

void kaprekarNumbers(int p, int q) {
    vector<int> res;
    for (unsigned long i = p; i <= q; i++) {
        int iDigits = digitLen(i);
        
        string sqStr = to_string(i * i);
        int sqDigits = sqStr.size();
        
        int rStart = 0;
        string lStr, rStr;
        if (sqDigits - iDigits >= 0) {
            lStr = string(sqStr.begin(), sqStr.begin() + sqDigits - iDigits);
            rStart = sqDigits - iDigits;
        }
        rStr = string(sqStr.begin() + rStart, sqStr.end());
        
        unsigned long l = lStr == "" ? 0 : stoul(lStr);
        unsigned long r = stoul(rStr);
        
        if (i == l + r) {
            res.push_back(i);
        }
    }
    
    string output;
    for (auto& n : res) {
        if (output.size()) {
            output.push_back(' ');
        }
        
        output = output + to_string(n);
    }
    
    output = output.size() ? output : "INVALID RANGE";
    cout << output << endl;
}

////////////////////////////////////////////////////////////////////////////////

int main() {
    
    // Test cases 1
    kaprekarNumbers(1, 100); // 1 9 45 55 99
    
    // Test cases 2
    kaprekarNumbers(100, 300); // 297
    
    // Test cases 3
    kaprekarNumbers(400, 700); // INVALID RANGE
    
    // Test cases 4
    kaprekarNumbers(1, 99999); // 1 9 45 55 99 297 703 999 2223 2728 4879 4950 5050 5292 7272 7777 9999 17344 22222 77778 82656 95121 99999
    
    return 0;
}