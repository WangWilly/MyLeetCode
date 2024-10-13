# Define the compiler
CXX = g++

# Define the compiler flags
CXXFLAGS = -Wall -std=c++11

# Define the build directory
BUILD_DIR = build

# Define the target executable
TARGET = $(BUILD_DIR)/solution

# Define the source files
SRCS = solution.cpp

# Define the object files
# `$(SRCS:.cpp=.o)` Replace the .cpp extension with .o
OBJS = $(addprefix $(BUILD_DIR)/, $(SRCS:.cpp=.o))

# The build target
#             v `$(OBJS)` Dependent rule: build the object files
$(TARGET): $(OBJS)
    # Link the object files into the target executable
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJS)

# Build directory creation
#                   v `%.cpp` Pattern rule: build the object files
$(BUILD_DIR)/%.o: %.cpp
    # Create the build directory if it does not exist
	@mkdir -p $(BUILD_DIR)
    # Compiles the .cpp file ($<) into an object file ($@).
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Clean the build directory
clean:
	rm -f $(BUILD_DIR)/*
