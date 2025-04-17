#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <unordered_map>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

bool isValidStr(string s) {
    stack<char> stk;
    unordered_map<char, char> leftRightPair = {
        {'>', '<'}, {')', '('}, {']', '['}, {'}', '{'}
    };

    for (auto& c : s) {
        if (!leftRightPair.count(c)) {
            stk.push(c);
            continue;
        }
        if (!stk.size()) {
            return false;
        }

        if (leftRightPair[c] != stk.top()) {
            return false;
        }
        stk.pop();
    }

    return !stk.size();
}

int main() {
    cout << "test: " << isValidStr("<>") << ", actual:" << true << endl;

    cout << "test: " << isValidStr(")(") << ", actual:" << false << endl;

    cout << "test: " << isValidStr("()[]{}<>") << ", actual:" << true << endl;

    cout << "test: " << isValidStr("([<)]") << ", actual:" << false << endl;

    cout << "test: " << isValidStr("{[]}((<>)[{}]{})<>") << ", actual:" << true << endl;

    cout << "test: " << isValidStr("{()[]{>") << ", actual:" << false << endl;

    return 0;
}
