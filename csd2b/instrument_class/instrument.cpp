#include "instrument.h"

// Constructor.
Instrument::Instrument(std::string sound) : sound(sound){}

// Delegating constructor.
Instrument::Instrument() : Instrument("Bwaahp"){}

// Destructor.
Instrument::~Instrument(){}

void Instrument::play() {
    std::cout << this->sound << "\n";
}
