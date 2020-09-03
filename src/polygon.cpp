#include "polygon.h"

Polygon::Polygon(int vs, vector<float> xs, vector<float> ys) {
    assert(xs.size() == vs && ys.size() == vs);

    vertices = vs;
    vertices_x = xs;
    vertices_y = ys;

    x_lower = COORD_LIMIT;
    y_lower = COORD_LIMIT;
    x_upper = -COORD_LIMIT;
    y_upper = -COORD_LIMIT;
    for (int i = 0; i < vs; i++) {
        x_lower = min(x_lower, vertices_x[i]);
        y_lower = min(y_lower, vertices_y[i]);
        x_upper = max(x_upper, vertices_x[i]);
        y_upper = max(y_upper, vertices_y[i]);
    }
}

bool Polygon::inside(float x, float y) {
    //return inside_bbox(x, y) && pnpoly(vertices, vertices_x, vertices_y, x, y);
    if (!inside_bbox(x, y)) return false;

    int i, j = 0;
    bool c = false;
    for (i = 0, j = vertices-1; i < vertices; j = i++) {
        if ( ((vertices_y[i]>y) != (vertices_y[j]>y)) &&
             (x < (vertices_x[j]-vertices_x[i]) * (y-vertices_y[i]) / (vertices_y[j]-vertices_y[i]) + vertices_x[i]) )
            c = !c;
    }
    return c;
}

bool Polygon::inside_bbox(float x, float y) {
    return (x >= x_lower) && (x <= x_upper) && (y >= y_lower) && (y <= y_upper);
}

/*
bool pnpoly(int nvert, vector<float> vertx, vector<float> verty, float testx, float testy) {
    int i, j = 0;
    bool c = false;
    for (i = 0, j = nvert-1; i < nvert; j = i++) {
        if ( ((verty[i]>testy) != (verty[j]>testy)) &&
             (testx < (vertx[j]-vertx[i]) * (testy-verty[i]) / (verty[j]-verty[i]) + vertx[i]) )
            c = !c;
    }
    return c;
}
*/