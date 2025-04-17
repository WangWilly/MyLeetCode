#include<string>
#include<vector>
#include<unordered_set>
#include<iostream>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

vector<vector<string>> parseCSV(string& csv) {
    vector<vector<string>> res;
    vector<string> row;

    string cell;
    for (int i = 0; i < csv.size(); i++) {
        if (csv[i] == ',') {
            row.push_back(cell);
            cell = "";
        } else if (csv[i] == '\n') {
            row.push_back(cell);
            res.push_back(row);
            row.clear();
            cell = "";
        } else {
            cell += csv[i];
        }
    }
    row.push_back(cell);
    res.push_back(row);

    return res;
}

bool isNullString(string s) {
    return s == "NULL";
}

string toCsvString(vector<vector<string>>& csv) {
    string res;
    for (int r = 0; r < csv.size(); r++) {
        for (int c = 0; c < csv[0].size(); c++) {
            res += csv[r][c];
            if (c < csv[0].size() - 1) {
                res += ",";
            }
        }
        if (r < csv.size() - 1) {
            res += "\n";
        }
    }

    return res;
}

string solution(string &S) {
    // Implement your solution here
    vector<vector<string>> csv = parseCSV(S);

    vector<vector<string>> resCsv;
    resCsv.push_back(csv[0]);
    for (int r = 1; r < csv.size(); r++) {
        int ok = true;
        for (int c = 0; c < csv[0].size(); c++) {
            if (isNullString(csv[r][c])) {
                ok = false;
                break;
            }
        }

        if (!ok) {
            continue;
        }

        resCsv.push_back(csv[r]);
    }

    return toCsvString(resCsv);
}

////////////////////////////////////////////////////////////////////////////////

int main() {
    // Test case 1
    {
        string S = "id,name,age,score\n1,Jack,NULL,12\n17,Betty,28,11";
        string res = solution(S);
        cout << res << endl;
    }

    // Test case 2
    {
        string S = "header,header\nANNUL,ANNULLED\nnull,NILL\nNULL,NULL";
        string res = solution(S);
        cout << res << endl;
    }

    // Test case 3
    {
        string S = "country,population,area\nUK,67m,242000km2";
        string res = solution(S);
        cout << res << endl;
    }

    // Test case 4
    {
        string S = "country,population,area\nUK,67m,242000km2\nNULL,67m,242000km2";
        string res = solution(S);
        cout << res << endl;
    }

    // Test case 5
    {
        string S = "country,population,area\nUK,67m,242000km2\nNULL,67m,242000km2\nUSA,NULL,242000km2";
        string res = solution(S);
        cout << res << endl;
    }

    return 0;
}


////////////////////////////////////////////////////////////////////////////////

// 2^31 - 1 = 2147483647
