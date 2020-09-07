#include "flight.h"

Flight::Flight(int vs, vector<float> xs, vector<float> ys, vector<int> hs, bool ft) {
    assert(xs.size() == vs && ys.size() == vs && hs.size() == vs);

    vertices = vs;
    vertices_x = xs;
    vertices_y = ys;

    if (!ft) {
        vector<int> hs2;
        for (int i = 0; i < hs.size(); i++) {
            hs2.push_back(metre_to_ft(hs[i]));
        }
        vertices_height = hs2;
    } else {
        vertices_height = hs;
    }

    x_lower = COORD_LIMIT;
    y_lower = COORD_LIMIT;
    x_upper = -COORD_LIMIT;
    y_upper = -COORD_LIMIT;
    height_lower = HEIGHT_LIMIT;
    height_upper = -HEIGHT_LIMIT;
    for (int i = 0; i < vs; i++) {
        x_lower = min(x_lower, vertices_x[i]);
        y_lower = min(y_lower, vertices_y[i]);
        height_lower = min(height_lower, vertices_height[i]);
        x_upper = max(x_upper, vertices_x[i]);
        y_upper = max(y_upper, vertices_y[i]);
        height_upper = max(height_upper, vertices_height[i]);
    }
    bbox = box(point_xy(x_lower, y_lower), point_xy(x_upper, y_upper));
}