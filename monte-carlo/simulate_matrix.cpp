#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime> 
#include <random>
#include "lodepng.h"
#include "heatmap.h"
#include <string>

using namespace std; 

int simulate(int rate) {
    // create the heatmap
    static const size_t w = 98, h = 98;
    heatmap_t* hm = heatmap_new(w, h);

    srand(time(0));
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

        if (totalTrials%rate==0) { 
            heatmap_add_point(hm, cell/98, cell%98);
            // create image
            std::vector<unsigned char> image(w*h*4);
            heatmap_render_default_to(hm, &image[0]);

            // finally, we use the fantastic lodepng library to save it as an image.
            if (unsigned error = lodepng::encode("heatmaps/heatmap_" + std::to_string(totalTrials/rate) + ".png", image, w, h)) {
                std::cerr << "encoder error " << error << ": "<< lodepng_error_text(error) << std::endl;
                return 1;
            }
        }
    }
    
    /*
    for (int i=0; i<selectedCells.size(); i++) {
        if (i>0 and i%98==0) {
            cout << endl;
        } 
        cout << selectedCells[i] << "\t";
    }
    */



    // print results
    cout << "\nTotal trials:" << totalTrials << endl;

    return totalTrials;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " rate" << std::endl;
        return 1;
    }

    int rate = std::atoi(argv[1]);

    simulate();
    return 0;
}