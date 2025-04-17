#include<string>
#include<vector>
#include<unordered_set>
#include<iostream>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

int solution(string &S) {
    unordered_map<char, int> lastSeen;

    int res = 0;
    int lastEnd = -1;
    for (int i = 0; i < S.size(); i++) {
        if (!lastSeen.count(S[i]) || lastSeen[S[i]] == -1) {
            lastSeen[S[i]] = i;
            continue;
        }

        if (lastEnd > lastSeen[S[i]]) {
            lastSeen[S[i]] = i;
            continue;
        }

        lastSeen[S[i]] = -1;
        res++;
        lastEnd = i;
    }

    return res;
}

////////////////////////////////////////////////////////////////////////////////

int main() {
    // Test case 1
    {
        string S = "abac";
        cout << solution(S) << endl;
    }

    // Test case 2
    {
        string S = "aaaa";
        cout << solution(S) << endl;
    }

    // Test case 3
    {
        string S = "abaca";
        cout << solution(S) << endl;
    }

    // Test case 4
    {
        string S = "abacaba";
        cout << solution(S) << endl;
    }

    // Test case 5
    {
        string S = "abacabadabacaba";
        cout << solution(S) << endl;
    }

    

    return 0;
}


////////////////////////////////////////////////////////////////////////////////

// 2^31 - 1 = 2147483647
