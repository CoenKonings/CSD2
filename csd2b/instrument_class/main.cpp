#include "instrument.h"

int main() {
    Instrument trumpet("Bwaahp!");
    Instrument mayonnaise("No, mayonnaise is not an instrument.");
    trumpet.play();
    mayonnaise.play();

    return 0;
}
