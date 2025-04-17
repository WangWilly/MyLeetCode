#include <iostream>
#include <vector>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

class Solution {
public:
    void removeFun(stack<pair<int, int>>& posAdvStack, vector<bool>& labelS, string& part) {
        if (posAdvStack.size() && part.size() - 1 == posAdvStack.top().second) {
            for (int c = 0; c < part.size(); c++) {
                labelS[posAdvStack.top().first] = false;
                posAdvStack.pop();
            }
            cout << "removeFun" << endl;
        }
    }
    string removeOccurrences(string s, string part) {
        char curr = part[0], currIdx = 0;
        vector<int> posArr(part.size(), 0);
        for (int i = 1; i < part.size(); i++) {
            while (part[i] != curr && currIdx != 0) {
                currIdx = posArr[currIdx];
                curr = part[currIdx];
            }

            if (part[i] == curr && i != part.size() - 1) {
                posArr[i + 1] = currIdx + 1;
            }
        }

        ////////////////////////////////////////////////////////////////////////
        stack<pair<int, int>> posAdvStack;

        vector<bool> labelS(s.size(), true);
        auto printLabelS = [&](vector<bool>& labelS) {
            for (int i = 0; i < labelS.size(); i++) {
                cout << labelS[i] << " ";
            }
            cout << endl;
        };
        auto hasNext = [&](char& c, int idx) {
            while (idx) {
                if (c == part[idx]) {
                    return idx;
                }
                idx = posArr[idx];
            }
            return 0;
        };
        for (int i = 0; i < s.size(); i++) {
            if (
                s[i] != part[0] && 
                !(posAdvStack.size() && hasNext(s[i], posAdvStack.top().second + 1))
            ) {
                posAdvStack = stack<pair<int, int>>();
                continue;
            }

            int idx = posAdvStack.size() ? hasNext(s[i], posAdvStack.top().second + 1) : 0;
            if (idx) {
                cout << "push" << endl;
                cout << i << " " << idx << endl;
                posAdvStack.push({i, idx});
                removeFun(posAdvStack, labelS, part);
                continue;
            }

            if (s[i] == part[0]) {
                cout << "push" << endl;
                cout << i << " " << 0 << endl;
                posAdvStack.push({i, 0});
                removeFun(posAdvStack, labelS, part);
                continue;
            }
        }

        string res;
        for (int i = 0; i < s.size(); i++) {
            if (!labelS[i]) {
                continue;
            }
            res += s[i];
        }

        return res;
    }
};

////////////////////////////////////////////////////////////////////////////////

int main() {
    Solution s;

    cout << 
    s.removeOccurrences(
        "bipfqtluhgrzcufxmbhhdvcdyhbipfqtluhgrzcufxmbhhdvcdyhookwqbvlialefmubkumdkyffoqkjqgrbukmugldaabipfqtluhgrzcufxmbhhdvcdyhookwqbvlialefmubkumdbipfqtluhgrzcufxmbhhdvcdyhookwqbvlialefmubkumdkyffoqkjqgrbukmugldaabigtnvonqnwsvsieckyffoqkjqgrbukmugldaabigtnvonqnwsvsiecbigtnvonqnwsvsiecookwqbvlialefmubkumdkyffoqkjqgrbukmugldaabigtnvonbipfqtluhgrzcufxmbhhdvcdyhookwqbvlialefmubipfqtluhgrzcufxmbhhdvcdyhookwqbvlialefmubkbipfqtluhgrzcufxmbhhdvcdyhookwqbvlialefmubkumdkyffoqkjqgrbukmugldaabigtnvonqnwsvsiecumdkyffoqkjqgrbukmugldaabigtnvonqnwsvsiecbkumdkyffoqkjqgrbukmugldaabigbipfqtluhgrzcufxmbhhdvcdyhookwqbvlialefmubkumdkyffoqkjqgrbukmugldaabigtnvonqnwsvsiectnvonqnwsvsiecqnwsvsiecccuncvgyragnodjhijwgnmahtqpxqijkiwvadraqqvokx",
        "bipfqtluhgrzcufxmbhhdvcdyhookwqbvlialefmubkumdkyffoqkjqgrbukmugldaabigtnvonqnwsvsiec"
    ) <<
    endl;
}
