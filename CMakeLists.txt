cmake_minimum_required(VERSION 3.10)
project(cpp-flights)
set(CMAKE_CXX_STANDARD 14)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

set(CMAKE_CXX_FLAGS_DEBUG "-g")
set(CMAKE_CXX_FLAGS_RELEASE "-O3")

find_package(PythonLibs 3 REQUIRED)
message("Include dirs of Python: " ${PYTHON_INCLUDE_DIR} )
message("Libs of Python: " ${PYTHON_LIBRARIES} )
find_package(Boost COMPONENTS numpy37 python37 REQUIRED)
message("Include dirs of Boost: " ${Boost_INCLUDE_DIR} )
message("Library dirs of Boost: " ${Boost_LIBRARY_DIRS} )
message("Libs of Boost: " ${Boost_LIBRARIES} )

include_directories(${Boost_INCLUDE_DIR} ${PYTHON_INCLUDE_DIR})
link_directories(${Boost_LIBRARY_DIRS} ${PYTHON_LIBRARIES})

include_directories(include)

set(SOURCES src/airspace.cpp src/flight.cpp src/helpers.cpp src/polygon.cpp src/processing.cpp)

add_executable(main src/main.cpp ${SOURCES})
target_link_libraries(main ${Boost_LIBRARIES})

python_add_module(process_flights src/python_out.cpp ${SOURCES})
# TODO figure out what keywords we actually need here
target_include_directories(process_flights PUBLIC ${Boost_INCLUDE_DIR} PUBLIC ${PYTHON_INCLUDE_DIR})
target_link_libraries(process_flights ${Boost_LIBRARIES})
target_link_libraries(process_flights boost_numpy37 boost_python37)

set(CMAKE_SHARED_MODULE_PREFIX "")
