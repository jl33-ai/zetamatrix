# Compiler settings - Can change to cc for C compiler
CXX=g++
CC=gcc

# Compiler flags
CXXFLAGS=-Wall -g
CFLAGS=-Wall -g

# Target executable name
TARGET=my_program

# Source files
SOURCES=simulate_matrix.cpp heatmap.c lodepng.cpp

# Object files
OBJECTS=$(SOURCES:.cpp=.o)
OBJECTS:=$(OBJECTS:.c=.o)

# Default target
all: $(TARGET)

# Link the target with object files
$(TARGET): $(OBJECTS)
	$(CXX) $(OBJECTS) -o $(TARGET)

# Compile C++ source files into object files
%.o: %.cpp
	$(CXX) -c $(CXXFLAGS) $< -o $@

# Compile C source files into object files
%.o: %.c
	$(CC) -c $(CFLAGS) $< -o $@

# Clean target
clean:
	rm -f $(OBJECTS) $(TARGET)
