#ifndef POLYGON_H
#define POLYGON_H

#include <algorithm>
#include <vector>
#include <cassert>

#define COORD_LIMIT 10000

using namespace std;

class Polygon {
public:
    Polygon(int vs = 0, vector<float> xs = vector<float>(), vector<float> ys = vector<float>());
    bool inside(float x, float y);
    bool inside_bbox(float x, float y);
    int vertices;
    vector<float> vertices_x;
    vector<float> vertices_y;
    float x_lower, x_upper, y_lower, y_upper;
};

// from https://wrf.ecse.rpi.edu/Research/Short_Notes/pnpoly.html
// nvert: number of vertices in the polygon (optionally repeat the first vertex at the end)
// vertx, verty: arrays containing the vertices' x and y coordinates
// testx, testy: x and y coordinates of the point to test
// bool pnpoly(int nvert, vector<float> vertx, vector<float> verty, float testx, float testy);

#endif
