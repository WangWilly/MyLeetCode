#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

int findRank(vector<pair<int,int>>& records, int score) {
    int lo = -1, hi = records.size() - 1; // (lo, hi]
    
    while (lo < hi) {
        int mid = (lo + hi + 1) / 2; // upper shifting
        if (records[mid].first > score) {
            lo = mid;
        } else {
            hi = mid - 1;
        }
    }
    
    return lo;
}

vector<int> climbingLeaderboard(vector<int> ranked, vector<int> player) {
    sort(ranked.begin(), ranked.end());
    reverse(ranked.begin(), ranked.end());
    
    vector<pair<int,int>> records;
    int currR = 1;
    for (auto& r : ranked) {
        if (records.size() && records.back().first == r) {
            continue;
        }
        
        records.push_back({r, currR++});
    }
    
    vector<int> res;
    for (auto& p : player) {
        int f = findRank(records, p);
        
        if (f == -1) {
            res.push_back(1);
            continue;
        }
        
        if (f < records.size()) {
            res.push_back(records[f].first == p ? records[f].second : records[f].second+1);
            continue;
        }
    }
    
    return res;
}

////////////////////////////////////////////////////////////////////////////////

int main() {
    // Test case 1
    vector<int> ranked1 = {100, 90, 90, 80};
    vector<int> player1 = {70, 80, 105};
    vector<int> res1 = climbingLeaderboard(ranked1, player1);
    for (auto& r : res1) {
        cout << r << " ";
    }
    cout << endl;
    // 4 3 1

    // Test case 2
    vector<int> ranked2 = {100, 100, 50, 40, 40, 20, 10};
    vector<int> player2 = {5, 25, 50, 120};
    vector<int> res2 = climbingLeaderboard(ranked2, player2);
    for (auto& r : res2) {
        cout << r << " ";
    }
    cout << endl;
    // 6 4 2 1

    // Test case 3
    vector<int> ranked3 = {100, 90, 90, 80, 75, 60};
    vector<int> player3 = {50, 65, 77, 90, 102};
    vector<int> res3 = climbingLeaderboard(ranked3, player3);
    for (auto& r : res3) {
        cout << r << " ";
    }
    cout << endl;
    // 6 5 4 2 1

    return 0;
}