CXX=g++
CXXFLAGS=-Wall -std=c++14
LDFLAGS=
SOURCE= instrument.o main.o

instrument: $(SOURCE)
	$(CXX) -o $@ $(SOURCE) $(LDFLAGS)

.cpp.o:
	$(CXX) -c $(CXXFLAGS) $<

clean:
	rm -f instrument *.o
