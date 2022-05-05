CXX = g++
CXXFLAGS = -g -Wall -Wextra -Werror -std=c++11

all: src/simple.cpp
	$(CXX) $(CXXFLAGS) src/simple.cpp -o simple

clean:
	rm -f simple simple.o m.wav