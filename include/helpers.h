#ifndef HELPERS_H
#define HELPERS_H

#define METRE_IN_FT 3.28084

#include <boost/geometry.hpp>
#include <boost/geometry/geometries/box.hpp>
#include <boost/geometry/geometries/point_xy.hpp>
#include <boost/geometry/geometries/polygon.hpp>
#include <boost/geometry/geometries/multi_polygon.hpp>
//#include <boost/geometry/strategies/spherical/distance_haversine.hpp>

#include <iostream>

namespace bg = boost::geometry;
namespace bgi = boost::geometry::index;
using namespace std;

typedef bg::model::d2::point_xy<double, bg::cs::geographic<bg::degree>> point_xy;
typedef bg::model::polygon<point_xy> polygon;
typedef bg::model::multi_polygon<polygon> multi_polygon;
typedef bg::model::box<point_xy> box;
typedef pair<box, int> value;

//typedef bg::strategy::distance::haversine<float> haversine;

// adapted from https://stackoverflow.com/questions/14539867/how-to-display-a-progress-indicator-in-pure-c-c-cout-printf
void progress_bar(float progress, int barWidth = 70);

float metre_to_ft(float metres);

#endif