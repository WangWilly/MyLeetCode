# Define the compiler
CXX = g++

# Define the compiler flags
CXXFLAGS = -Wall -std=c++11

# Define the target executable
TARGET = solution

# Define the source files
SRCS = solution.cpp

# Define the object files
OBJS = $(SRCS:.cpp=.o)

# The build target
$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJS)

# Clean the build directory
clean:
	rm -f $(TARGET) $(OBJS)
