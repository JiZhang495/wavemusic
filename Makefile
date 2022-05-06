CXX = g++
CXXFLAGS = -Wall -Wextra -Werror -std=c++11 -O2

ifdef DEBUG
CXXFLAGS += -DDEBUG
endif

.PHONY: refresh clean

refresh: clean simple

simple: simple.o sigen.o
	$(CXX) simple.o sigen.o -o simple

simple.o: src/simple.cpp
	$(CXX) $(CXXFLAGS) -c src/simple.cpp -o simple.o

sigen.o: src/sigen.cpp
	$(CXX) $(CXXFLAGS) -c src/sigen.cpp -o sigen.o

clean:
	rm -f simple m.wav *.o
