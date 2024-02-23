#include "geometric_random_variable.h"
#include <cstdlib>

using namespace std;

int geometricRandomVariable(unsigned int inv_p, unsigned int seed) {
    if (inv_p == 0) {
        return 0;
    }
    srand(seed); 
    int i=1;
    while (rand() % inv_p != 0) { 
        i++;
    }
    return i;
}
