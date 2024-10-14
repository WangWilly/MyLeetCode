#include <iostream>
#include <vector>
#include <map>
#include <queue>
#include <unordered_set>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

class Solution {
public:
    int smallestChair(vector<vector<int>>& times, int targetFriend) {
        // w/ addi slot to keep the ori idx
        for (int i = 0; i < times.size(); i++) {
            times[i].push_back(i);
        }
        sort(times.begin(), times.end());

        map<int, vector<int>> timeMap;
        for (auto& info : times) {
            int shifted = info[2] + 1;
            timeMap[info[0]].push_back(shifted);
            timeMap[info[1]].push_back(-shifted);
        }
        for (auto& pair : timeMap) {
            sort(pair.second.begin(), pair.second.end());
        }

        vector<int> res(times.size(), 0);
        priority_queue<int, vector<int>, greater<int>> pq;
        int currPtr = 0;
        for (auto& pair : timeMap) {
            for (auto& shifted : pair.second) {
                int idx = abs(shifted) - 1;
                if (shifted < 0) {
                    pq.push(res[idx]);
                    continue;
                }

                if (pq.size()) {
                    res[idx] = pq.top();
                    pq.pop();
                    continue;
                }

                res[idx] = currPtr++;
            }
        }

        return res[targetFriend];
    }
};

////////////////////////////////////////////////////////////////////////////////

int main() {
    Solution s;

    // Test case 1
    vector<vector<int>> times1 = {{1, 4}, {2, 3}, {4, 6}};
    cout << s.smallestChair(times1, 1) << endl; // 1

    // Test case 2
    vector<vector<int>> times2 = {{3, 10}, {1, 5}, {2, 6}};
    cout << s.smallestChair(times2, 0) << endl; // 2

    // Test case 3
    vector<vector<int>> times3 = {
        {33889, 98676}, // 0
        {80071, 89737}, // 1
        {44118, 52565}, // 2  v
        {52992, 84310}, // 3  v
        {78492, 88209}, // 4
        {21695, 67063}, // 5  v
        {84622, 95452}, // 6  <=
        {98048, 98856}, // 7
        {98411, 99433}, // 8
        {55333, 56548}, // 9  v
        {65375, 88566}, // 10
        {55011, 62821}, // 11 v
        {48548, 48656}, // 12 v
        {87396, 94825}, // 13
        {55273, 81868}, // 14 v
        {75629, 91467}, // 15
    };
    cout << s.smallestChair(times3, 6) << endl; // 2
    // {21695, 67063} -> {33889, 98676} -> {44118, 52565} -> {48548, 48656} -> {52992, 84310} -> {55011, 62821} -> {55273, 81868} -> {55333, 56548} -> {65375, 88566} -> {75629, 91467} -> {78492, 88209} -> {80071, 89737} -> {84622, 95452}
    //        0                 1                 2                 3                 3                 2                 4                 5
    //GT      0                 1                 2                 3                 2                 3

    // Test case 4
    vector<vector<int>> times4 = {
        {18, 19}, // 0
        {10, 11}, // 1
        {21, 22}, // 2
        {5, 6},   // 3
        {2, 3},   // 4
        {6, 7},   // 5
        {43, 44}, // 6
        {48, 49}, // 7
        {53, 54}, // 8
        {12, 13}, // 9
        {20, 21}, // 10
        {34, 35}, // 11
        {17, 18}, // 12
        {1, 2},   // 13
        {35, 36}, // 14
        {16, 17}, // 15
        {9, 10},  // 16
        {14, 15}, // 17
        {25, 26}, // 18
        {37, 38}, // 19
        {30, 31}, // 20
        {50, 51}, // 21
        {22, 23}, // 22
        {3, 4},   // 23
        {27, 28}, // 24
        {29, 30}, // 25
        {33, 34}, // 26
        {39, 40}, // 27
        {49, 50}, // 28
        {15, 16}, // 29
        {4, 5},   // 30
        {46, 47}, // 31
        {51, 52}, // 32
        {32, 33}, // 33
        {11, 12}, // 34
        {28, 29}, // 35
        {47, 48}, // 36
        {36, 37}, // 37
        {40, 41}, // 38
        {42, 43}, // 39
        {52, 53}, // 40
        {41, 42}, // 41
        {31, 32}, // 42
        {23, 24}, // 43
        {8, 9},   // 44
        {19, 20}, // 45
        {24, 25}, // 46
        {26, 27}, // 47
        {45, 46}, // 48
        {44, 45}, // 49
        {7, 8},   // 50
        {13, 14}, // 51
        {38, 39}, // 52
    };
    cout << s.smallestChair(times4, 0) << endl; // 0


    return 0;
}
