# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/pi/dome/v0

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/pi/dome/v0/build

# Include any dependencies generated for this target.
include CMakeFiles/pyraspii.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/pyraspii.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/pyraspii.dir/flags.make

CMakeFiles/pyraspii.dir/rasp_master.cpp.o: CMakeFiles/pyraspii.dir/flags.make
CMakeFiles/pyraspii.dir/rasp_master.cpp.o: ../rasp_master.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/pi/dome/v0/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/pyraspii.dir/rasp_master.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/pyraspii.dir/rasp_master.cpp.o -c /home/pi/dome/v0/rasp_master.cpp

CMakeFiles/pyraspii.dir/rasp_master.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/pyraspii.dir/rasp_master.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/pi/dome/v0/rasp_master.cpp > CMakeFiles/pyraspii.dir/rasp_master.cpp.i

CMakeFiles/pyraspii.dir/rasp_master.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/pyraspii.dir/rasp_master.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/pi/dome/v0/rasp_master.cpp -o CMakeFiles/pyraspii.dir/rasp_master.cpp.s

# Object files for target pyraspii
pyraspii_OBJECTS = \
"CMakeFiles/pyraspii.dir/rasp_master.cpp.o"

# External object files for target pyraspii
pyraspii_EXTERNAL_OBJECTS =

pyraspii.cpython-37m-arm-linux-gnueabihf.so: CMakeFiles/pyraspii.dir/rasp_master.cpp.o
pyraspii.cpython-37m-arm-linux-gnueabihf.so: CMakeFiles/pyraspii.dir/build.make
pyraspii.cpython-37m-arm-linux-gnueabihf.so: CMakeFiles/pyraspii.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/pi/dome/v0/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX shared module pyraspii.cpython-37m-arm-linux-gnueabihf.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/pyraspii.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/pyraspii.dir/build: pyraspii.cpython-37m-arm-linux-gnueabihf.so

.PHONY : CMakeFiles/pyraspii.dir/build

CMakeFiles/pyraspii.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/pyraspii.dir/cmake_clean.cmake
.PHONY : CMakeFiles/pyraspii.dir/clean

CMakeFiles/pyraspii.dir/depend:
	cd /home/pi/dome/v0/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/pi/dome/v0 /home/pi/dome/v0 /home/pi/dome/v0/build /home/pi/dome/v0/build /home/pi/dome/v0/build/CMakeFiles/pyraspii.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/pyraspii.dir/depend

