#include <iostream>
#include <string>
#include <algorithm>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

string biggerIsGreater(string w) {
    for (int i = w.size() - 1; i >= 0; i--) {
        int sIdx = i;
        char curr = 'z';
        for (int j = i + 1; j < w.size(); j++) {
            if (w[j] > w[i] && w[j] <= curr) {
                sIdx = j;
                curr = w[j];
            }
        }
        if (sIdx == i) {
            continue;
        }
        
        swap(w[i], w[sIdx]);
        sort(w.begin()+i+1, w.end());
        return w;
    }
    
    return "no answer";
}

////////////////////////////////////////////////////////////////////////////////

int main() {
    
    // Test cases 1
    string w = "ab";
    string res = biggerIsGreater(w);
    cout << res << endl; // ba

    // Test cases 2
    w = "bb";
    res = biggerIsGreater(w);
    cout << res << endl; // no answer

    // Test cases 3
    w = "hefg";
    res = biggerIsGreater(w);
    cout << res << endl; // hegf

    // Test cases 4
    w = "dhck";
    res = biggerIsGreater(w);
    cout << res << endl; // dhkc

    // Test cases 5
    w = "dkhc";
    res = biggerIsGreater(w);
    cout << res << endl; // hcdk


    return 0;
}