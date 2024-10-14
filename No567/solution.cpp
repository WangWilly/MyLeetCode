#include <iostream>
#include <unordered_map>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

class Solution {
public:
    bool compareMap(unordered_map<char, int>& s1Map, unordered_map<char, int>& s2Map) {
        for (auto& pair : s2Map) {
            if (s1Map[pair.first] != pair.second) {
                return false;
            }
        }

        return true;
    }

    bool checkInclusion(string s1, string s2) {
        unordered_map<char, int> s1Map;

        for (auto& c : s1) {
            s1Map[c]++;
        }

        unordered_map<char, int> s2Map;
        for (int hi = 0, lo = 0; hi < s2.size(); hi++) {
            if (hi - lo + 1 < s1.size()) {
                s2Map[s2[hi]]++;
                continue;
            }

            s2Map[s2[hi]]++;
            if (compareMap(s1Map, s2Map)) {
                return true;
            }

            s2Map[s2[lo++]]--;
        }

        return false;
    }
};

////////////////////////////////////////////////////////////////////////////////

int main() {
    Solution s;

    // Test case 1
    cout << s.checkInclusion("ab", "eidbaooo") << endl; // 1

    // Test case 2
    cout << s.checkInclusion("ab", "eidboaoo") << endl; // 0

    return 0;
}

////////////////////////////////////////////////////////////////////////////////
