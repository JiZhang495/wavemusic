CXX = g++
CXXFLAGS = -g -Wall -Wextra -Werror -std=c++11

all: examples/simple.cpp
	$(CXX) $(CXXFLAGS) examples/simple.cpp -o simple

clean:
	rm -f simple simple.o m.wav