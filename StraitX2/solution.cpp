#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <unordered_map>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

void genStrs(vector<string>& ans, int currLeft, int currRight, int tar, string currStr) {
    if (currRight == tar) {
        ans.push_back(currStr);
        return;
    }

    if (currLeft < tar) {
        genStrs(ans, currLeft + 1, currRight, tar, currStr + "(");
    }
    if (currRight < currLeft) {
        genStrs(ans, currLeft, currRight + 1, tar, currStr + ")");
    }
}

int main() {
    vector<string> ans;
    genStrs(ans, 0, 0, 3, "");
    cout << "ans: ";
    for (auto& s : ans) {
        cout << s << ",";
    }
    cout << endl;

    return 0;
}
