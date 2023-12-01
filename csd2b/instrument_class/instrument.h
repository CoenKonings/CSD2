#include <iostream>
#include <string>

class Instrument {
public:
    Instrument();
    Instrument(std::string sound);
    ~Instrument();
    void play();

protected:
    std::string sound;
};
