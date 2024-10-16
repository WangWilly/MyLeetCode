#include <iostream>
#include <string>
#include <vector>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

string organizingContainers(vector<vector<int>> container) {
    int cNum = container.size();
    
    vector<int> inSum(cNum, 0), outSum(cNum, 0);
    for (int i = 0; i < cNum; i++) {
        if (container[i].size() > cNum) {
            return "Impossible";
        }
        
        for (int t = 0; t < container[i].size(); t++) {
            outSum[i] -= container[i][t];
            inSum[t] += container[i][t];
        }
    }
    
    for (int i = 0; i < cNum; i++) {
        for (int j = 0; j <= cNum; j++) {
            if (j == cNum) {
                return "Impossible";
            }
            if (outSum[i] + inSum[j] == 0) {
                outSum[i] = 0;
                inSum[j] = 0;
                break;
            }
        }
    }
    
    return "Possible";
}

////////////////////////////////////////////////////////////////////////////////

int main() {
    // Test case 1
    vector<vector<int>> container1 = {{1, 1}, {1, 1}};
    cout << organizingContainers(container1) << endl; // Possible

    // Test case 2
    vector<vector<int>> container2 = {{0, 2}, {1, 1}};
    cout << organizingContainers(container2) << endl; // Impossible

    // Test case 3
    vector<vector<int>> container3 = {{1, 3, 1}, {2, 1, 2}, {3, 3, 3}};
    cout << organizingContainers(container3) << endl; // Impossible

    // Test case 4
    vector<vector<int>> container4 = {{0, 2, 1}, {1, 1, 1}, {2, 0, 0}};
    cout << organizingContainers(container4) << endl; // Possible

    // Test case 5
    vector<vector<int>> container5 = {{1, 0}, {0, 1}};
    cout << organizingContainers(container5) << endl; // Possible

    // Test case 6
    vector<vector<int>> container6 = {{1, 2}, {2, 1}};
    cout << organizingContainers(container6) << endl; // Possible

    // Test case 7
    vector<vector<int>> container7 = {{0, 4, 0}, {2, 0, 1}, {1, 0, 2}};
    cout << organizingContainers(container7) << endl; // Possible

    // Test case 8
    vector<vector<int>> container8 = {{1, 2, 3, 4}, {2, 1, 4, 3}, {3, 4, 2, 1}, {4, 3, 1, 2}};
    cout << organizingContainers(container8) << endl; // Possible

    // Test case 9
    vector<vector<int>> container9 = {{0, 0, 5, 0}, {4, 0, 0, 0}, {0, 2, 0, 1}, {0, 1, 0, 2}};
    cout << organizingContainers(container9) << endl; // Possible

    // Test case 10
    vector<vector<int>> container10 = {{2, 1}, {0, 0}};
    cout << organizingContainers(container10) << endl; // Impossible

    // Test case 11
    vector<vector<int>> container11 = {{2, 1}, {0, 1}};
    cout << organizingContainers(container11) << endl; // Impossible

    // Test case 12
    vector<vector<int>> container12 = {{1, 2, 3}, {3, 2, 1}, {2, 3, 1}};
    cout << organizingContainers(container12) << endl; // Impossible

    // Test case 13
    vector<vector<int>> container13 = {{1, 0, 0}, {0, 2, 0}, {0, 2, 0}};
    cout << organizingContainers(container13) << endl; // Impossible

    // Test case 14
    vector<vector<int>> container14 = {{1, 2, 1, 3}, {2, 1, 3, 1}, {1, 3, 2, 1}, {3, 2, 1, 1}};
    cout << organizingContainers(container14) << endl; // Impossible

    return 0;
}

////////////////////////////////////////////////////////////////////////////////

/**
Possible:

2
1 0
0 1

2
1 2
2 1

3
0 4 0
2 0 1
1 0 2

4
1 2 3 4
2 1 4 3
3 4 2 1
4 3 1 2

4
0 0 5 0
4 0 0 0
0 2 0 1
0 1 0 2

Impossible:

2
2 1
0 0

2
2 1
0 1

3
1 2 3
3 2 1
2 3 1

3
1 0 0
0 2 0
0 2 0

4
1 2 1 3
2 1 3 1
1 3 2 1
3 2 1 1
*/