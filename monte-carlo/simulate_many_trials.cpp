#include <iostream>
#include <vector>
#include <cstdlib>
#include <fstream>
#include <random>

using namespace std; 

int simulate() {
    std::random_device rd;
    srand(rd());
    int gridSize = 98*98; 
    vector<short> selectedCells(gridSize, 0);
    int selectedCount = 0;
    int totalTrials = 0;

    while (selectedCount < gridSize) {
        int cell = rand() % gridSize;
        if (!selectedCells[cell]) {
            selectedCount++;
        }  
        selectedCells[cell]++;
        totalTrials++;
    }

    return totalTrials;
}

int main() {
    int n = 100000;
    std::ofstream file("export.csv");
    vector<int> allSims(n, 0);
    for (int i=0; i<n; i++) { 
        int result = simulate();
        file << result << ","; 
        allSims[i]=result;
        if (i%100==0) { 
            cout << "did " << i << endl;
        }
    }
    file.close();
    return 0;
}