#ifndef PYTHON_OUT_H
#define PYTHON_OUT_H

#include <vector>
#include <iostream>

#include "processing.h"
#include "airspace.h"
#include "flight.h"
#include "polygon.h"

#include <boost/geometry.hpp>
#include <boost/python.hpp>
#include <boost/python/numpy.hpp>

namespace py = boost::python;
namespace np = boost::python::numpy;
using namespace std;


string version = "0.1.1.2";

/*
template<class T>
py::list vector_to_list(const std::vector<T>& v)
{
    py::object get_iter = py::iterator<std::vector<T> >();
    py::object iter = get_iter(v);
    py::list l(iter);
    return l;
}
*/

class AirspaceHandler {
public:
    AirspaceHandler();
    int add_airspace(string wkt, int lower, int upper);
    int add_airspaces_file(string location);
    //void add_airspaces(); TODO
    void process_flight(np::ndarray &xs, np::ndarray &ys, np::ndarray &hs);
    void process_flights_file(string location);
    py::list airspaces_at_point(float x, float y, int height);
    py::list airspaces_near_point(float x, float y, int height);
    int size();
    void reset_result();
    np::ndarray get_result();
private:
    MultiAirspace airspaces;
    vector<vector<int>> result;
    bool ready = false;
    int N;
};

#endif