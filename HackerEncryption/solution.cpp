# include <iostream>
# include <cmath>
# include <string>
# include <vector>

using namespace std;

////////////////////////////////////////////////////////////////////////////////

pair<int, int> chooseRowsAndCols(int sSize) {
    int rows = sqrt(sSize);
    if (rows * rows == sSize) {
        return {rows, rows};
    }
    int cols = rows + 1;
    if (rows * cols < sSize) {
        rows++;
    }
    return {rows, cols};
}

string encryption(string s) {
    // auto [rows, cols] = chooseRowsAndCols(s.size());
    pair<int, int> rc = chooseRowsAndCols(s.size());
    int rows = rc.first;
    int cols = rc.second;
    
    vector<string> resArr;
    for (int r = 0; r < rows; r++) {
        resArr.push_back(string(s.begin()+cols*r, s.begin()+cols*(r+1)));
    }
    
    string res;
    for(int c = 0; c < cols; c++) {
        for (int r = 0; r*cols+c < s.size(); r++) {
            res.push_back(resArr[r][c]);
        }
        res.push_back(' ');
    }
    return res;
}

////////////////////////////////////////////////////////////////////////////////

int main() {
    // Test case 1
    cout << encryption("haveaniceday") << endl; // hae and via ecy

    // Test case 2
    cout << encryption("feedthedog") << endl; // fto ehg ee dd

    // Test case 3
    cout << encryption("chillout") << endl; // clu hlt io

    // Test case 4
    cout << encryption("ifmanwasmeanttostayonthegroundgodwouldhavegivenusroots") << endl; // imtgdvs fearwer mayoogo anouuio ntnnlvt wttddes aohghn sseoau

    return 0;
}

////////////////////////////////////////////////////////////////////////////////
