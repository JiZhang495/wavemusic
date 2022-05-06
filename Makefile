CXX = g++
CXXFLAGS = -Wall -Wextra -Werror -std=c++11

.PHONY: all clean

all: simple dsimple

simple: src/simple.cpp
	$(CXX) $(CXXFLAGS) -O2 src/simple.cpp -o simple

dsimple: src/simple.cpp
	$(CXX) $(CXXFLAGS) -D DEBUG src/simple.cpp -o dsimple

clean:
	rm -f simple dsimple simple.o m.wav
