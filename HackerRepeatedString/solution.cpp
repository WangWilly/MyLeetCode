#include <iostream>
#include <string>
#include <vector>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

long repeatedString(string s, long n) {
    vector<long> countA(s.size(), 0);
    
    countA[0] = (s[0] == 'a');
    for (int i = 1; i < s.size(); i++) {
        countA[i] = countA[i - 1] + (s[i] == 'a');
    }
    
    long repeat = n / s.size();
    long rest = n % s.size();
    return repeat * countA.back() + (rest ? countA[rest - 1] : 0);
}

////////////////////////////////////////////////////////////////////////////////

int main() {
    // Test case 1
    cout << repeatedString("aba", 10) << endl; // 7

    // Test case 2
    cout << repeatedString("a", 1000000000000) << endl; // 1000000000000

    return 0;
}

////////////////////////////////////////////////////////////////////////////////
