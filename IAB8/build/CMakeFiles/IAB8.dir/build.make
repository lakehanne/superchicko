# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.13

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
CMAKE_COMMAND = /usr/local/Cellar/cmake/3.13.3/bin/cmake

# The command to remove a file.
RM = /usr/local/Cellar/cmake/3.13.3/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/olalekanogunmolu/Documents/superchicko/IAB8

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/olalekanogunmolu/Documents/superchicko/IAB8/build

# Include any dependencies generated for this target.
include CMakeFiles/IAB8.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/IAB8.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/IAB8.dir/flags.make

CMakeFiles/IAB8.dir/src/IAB8.cpp.o: CMakeFiles/IAB8.dir/flags.make
CMakeFiles/IAB8.dir/src/IAB8.cpp.o: ../src/IAB8.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/olalekanogunmolu/Documents/superchicko/IAB8/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/IAB8.dir/src/IAB8.cpp.o"
	/Library/Developer/CommandLineTools/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/IAB8.dir/src/IAB8.cpp.o -c /Users/olalekanogunmolu/Documents/superchicko/IAB8/src/IAB8.cpp

CMakeFiles/IAB8.dir/src/IAB8.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/IAB8.dir/src/IAB8.cpp.i"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/olalekanogunmolu/Documents/superchicko/IAB8/src/IAB8.cpp > CMakeFiles/IAB8.dir/src/IAB8.cpp.i

CMakeFiles/IAB8.dir/src/IAB8.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/IAB8.dir/src/IAB8.cpp.s"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/olalekanogunmolu/Documents/superchicko/IAB8/src/IAB8.cpp -o CMakeFiles/IAB8.dir/src/IAB8.cpp.s

# Object files for target IAB8
IAB8_OBJECTS = \
"CMakeFiles/IAB8.dir/src/IAB8.cpp.o"

# External object files for target IAB8
IAB8_EXTERNAL_OBJECTS =

IAB8: CMakeFiles/IAB8.dir/src/IAB8.cpp.o
IAB8: CMakeFiles/IAB8.dir/build.make
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaSimulationGraph.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaGuiMain.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaMiscCollision.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaPython.0.1.dylib
IAB8: /usr/local/lib/libboost_filesystem-mt.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaGuiQt.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libQGLViewer.2.7.1.dylib
IAB8: /Users/olalekanogunmolu/anaconda3/lib/libQt5OpenGL.5.9.7.dylib
IAB8: /Users/olalekanogunmolu/anaconda3/lib/libQt5Widgets.5.9.7.dylib
IAB8: /Users/olalekanogunmolu/anaconda3/lib/libQt5Gui.5.9.7.dylib
IAB8: /Users/olalekanogunmolu/anaconda3/lib/libQt5Xml.5.9.7.dylib
IAB8: /Users/olalekanogunmolu/anaconda3/lib/libQt5Core.5.9.7.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaGuiCommon.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaComponentAdvanced.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaComponentMisc.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaMisc.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaMiscEngine.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaNonUniformFem.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaMiscFem.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaMiscForceField.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaMiscMapping.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaMiscSolver.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaMiscTopology.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaComponentBase.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaComponentCommon.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaExplicitOdeSolver.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaEngine.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaComponentGeneral.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaGeneralDeformable.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaConstraint.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaImplicitOdeSolver.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaGeneralExplicitOdeSolver.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaOpenglVisual.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaUserInteraction.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaGeneralSimpleFem.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaSimpleFem.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaDenseSolver.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libnewmat.a
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaTopologyMapping.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaBoundaryCondition.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaEigen2Solver.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaGeneralTopology.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaGraphComponent.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaGeneralRigid.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaGeneralVisual.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaBaseVisual.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaGeneralAnimationLoop.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaGeneralImplicitOdeSolver.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaGeneralLinearSolver.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaBaseLinearSolver.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaGeneralObjectInteraction.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaGeneralEngine.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaGeneralMeshCollision.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaValidation.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaLoader.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaMeshCollision.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaBaseCollision.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaRigid.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaBaseMechanics.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaObjectInteraction.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaDeformable.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaBaseTopology.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaGeneralLoader.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaSimulationTree.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaSimulationCommon.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaSimulationCore.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaCore.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaDefaultType.19.06.99.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libSofaHelper.19.06.99.dylib
IAB8: /usr/lib/libiconv.dylib
IAB8: /usr/local/lib/libGLEW.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libtinyxml.2.6.2.dylib
IAB8: /usr/lib/libz.dylib
IAB8: /usr/local/lib/libboost_system-mt.dylib
IAB8: /usr/local/lib/libboost_filesystem-mt.dylib
IAB8: /usr/local/lib/libboost_locale-mt.dylib
IAB8: /usr/local/lib/libboost_program_options-mt.dylib
IAB8: /usr/local/lib/libboost_date_time-mt.dylib
IAB8: /usr/local/lib/libboost_thread-mt.dylib
IAB8: /usr/local/lib/libboost_system-mt.dylib
IAB8: /usr/local/lib/libboost_locale-mt.dylib
IAB8: /usr/local/lib/libboost_program_options-mt.dylib
IAB8: /usr/local/lib/libboost_chrono-mt.dylib
IAB8: /usr/local/lib/libboost_atomic-mt.dylib
IAB8: /usr/local/lib/libboost_thread-mt.dylib
IAB8: /usr/local/lib/libboost_date_time-mt.dylib
IAB8: /Users/olalekanogunmolu/sofa/master/build/install/lib/libgtest.dylib
IAB8: /usr/lib/libpython2.7.dylib
IAB8: /usr/local/lib/libboost_filesystem-mt.dylib
IAB8: CMakeFiles/IAB8.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/olalekanogunmolu/Documents/superchicko/IAB8/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable IAB8"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/IAB8.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/IAB8.dir/build: IAB8

.PHONY : CMakeFiles/IAB8.dir/build

CMakeFiles/IAB8.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/IAB8.dir/cmake_clean.cmake
.PHONY : CMakeFiles/IAB8.dir/clean

CMakeFiles/IAB8.dir/depend:
	cd /Users/olalekanogunmolu/Documents/superchicko/IAB8/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/olalekanogunmolu/Documents/superchicko/IAB8 /Users/olalekanogunmolu/Documents/superchicko/IAB8 /Users/olalekanogunmolu/Documents/superchicko/IAB8/build /Users/olalekanogunmolu/Documents/superchicko/IAB8/build /Users/olalekanogunmolu/Documents/superchicko/IAB8/build/CMakeFiles/IAB8.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/IAB8.dir/depend

