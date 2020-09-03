#ifndef FLIGHT_H
#define FLIGHT_H

#include <boost/geometry.hpp>
#include <boost/geometry/geometries/box.hpp>
#include <boost/geometry/geometries/point_xy.hpp>

#include <cassert>
#include <vector>

#include "helpers.h"

#define COORD_LIMIT 10000
#define HEIGHT_LIMIT 100000

using namespace std;

class Flight {
public:
    Flight(int vs, vector<float> xs, vector<float> ys, vector<int> hs, bool ft = false);
    int vertices;
    vector<float> vertices_x;
    vector<float> vertices_y;
    vector<int> vertices_height;
    float x_lower, x_upper, y_lower, y_upper;
    int height_lower, height_upper;
    box bbox;
};

#endif
