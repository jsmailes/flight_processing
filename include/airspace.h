#ifndef AIRSPACE_H
#define AIRSPACE_H

//#define EARTH_RADIUS_FT 20902260

#include <boost/geometry.hpp>
#include <boost/geometry/index/rtree.hpp>
#include <boost/geometry/algorithms/distance.hpp>
#include <boost/foreach.hpp>
#include <boost/range/adaptor/transformed.hpp>

#include <cmath>
#include <cassert>
#include <fstream>
#include <utility>

#include <nlohmann/json.hpp>
using json = nlohmann::json;

#include "polygon.h"
#include "flight.h"
#include "helpers.h"

using namespace std;


class Airspace {
public:
    Airspace(Polygon polygon, int lower, int upper, int ident);
    bool inside(float x, float y, int height);
    bool inside_bbox(float x, float y, int height);
    bool intersects_bbox(Flight &flight);
    int id;
    Polygon polygon;
    int lower_limit, upper_limit;
};

class AirspaceBoost {
public:
    AirspaceBoost(multi_polygon shape, int lower, int upper);
    AirspaceBoost(string wkt, int lower, int upper);
    bool inside(float x, float y, int height);
    bool inside_bbox(float x, float y, int height);
    float distance(float x, float y, int height);
    float distance(point_xy &xy, int height);
    multi_polygon polygon;
    int lower_limit, upper_limit;
    box bounds;
private:
    bool inside_height(int height);
};

class MultiAirspace {
public:
    MultiAirspace();
    int add_airspace(AirspaceBoost &airspace);
    int add_airspaces_file(string location);
    vector<int> query_point(float x, float y, int height);
    vector<int> query_box(box query);
    vector<pair<int, float>> airspaces_near_point(float x, float y, int height, int k=5);
    long unsigned int size();
    void process_flight(Flight &flight, vector<vector<int>> &out);
    vector<pair<int, int>> process_single_flight(Flight &flight);
private:
    vector<AirspaceBoost> airspaces;
    bgi::rtree<value, bgi::rstar<16>> rtree;
};

#endif
