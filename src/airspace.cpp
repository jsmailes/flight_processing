#include "airspace.h"

Airspace::Airspace(Polygon poly, int lower, int upper, int ident) {
    polygon = poly;
    lower_limit = lower;
    upper_limit = upper;
    id = ident;
}

bool Airspace::inside(float x, float y, int height) {
    return (height >= lower_limit) && (height <= upper_limit) && polygon.inside(x, y);
}

bool Airspace::inside_bbox(float x, float y, int height) {
    return (height >= lower_limit) && (height <= upper_limit) && polygon.inside_bbox(x, y);
}

bool Airspace::intersects_bbox(Flight &flight) {
    return !(lower_limit > flight.height_upper
        || upper_limit < flight.height_lower
        || polygon.x_lower > flight.x_upper
        || polygon.x_upper < flight.x_lower
        || polygon.y_upper < flight.y_lower
        || polygon.y_lower > flight.y_upper);
}


AirspaceBoost::AirspaceBoost(multi_polygon poly, int lower, int upper) {
    polygon = poly;
    lower_limit = lower;
    upper_limit = upper;
    bg::envelope(polygon, bounds);
}

AirspaceBoost::AirspaceBoost(string wkt, int lower, int upper) {
    bg::read_wkt(wkt, polygon);
    lower_limit = lower;
    upper_limit = upper;
    if (!bg::is_empty(polygon)) {
        bg::envelope(polygon, bounds);
    } else {
        bounds = box(point_xy(0,0), point_xy(0,0));
        //cout << "Empty geometry\n";
    }
    /*
    double min_x = bg::get<bg::min_corner, 0>(bounds);
    double min_y = bg::get<bg::min_corner, 1>(bounds);
    double max_x = bounds.max_corner().get<0>();
    double max_y = bounds.max_corner().get<1>();
    cout << min_x << ", " << min_y << ", " << max_x << ", " << max_y << "\n";
    */
}

bool AirspaceBoost::inside_height(int height) {
    return height >= lower_limit && height <= upper_limit;
}

bool AirspaceBoost::inside(float x, float y, int height) {
    return inside_bbox(x, y, height) && bg::within(point_xy(x, y), polygon);
}

bool AirspaceBoost::inside_bbox(float x, float y, int height) {
    return inside_height(height) && bg::within(point_xy(x, y), bounds);
}

float AirspaceBoost::distance(float x, float y, int height) {
    point_xy xy = point_xy(x, y);
    return distance(xy, height);
}

float AirspaceBoost::distance(point_xy &xy, int height) {
    float distance_xy = metre_to_ft(bg::distance(xy, polygon));

    float distance_height;
    if (inside_height(height)) {
        distance_height = 0;
    } else if (height < lower_limit) {
        distance_height = (float) (lower_limit - height);
    } else { // height > upper_limit
        distance_height = (float) (height - upper_limit);
    }
    return sqrt(pow(distance_xy, 2) + pow(distance_height, 2));
}


MultiAirspace::MultiAirspace() {

}

int MultiAirspace::add_airspace(AirspaceBoost &airspace) {
    int id = airspaces.size();
    airspaces.push_back(airspace);
    rtree.insert(make_pair(airspace.bounds, id));
    return id;
}

int MultiAirspace::add_airspaces_file(string location) {
    ifstream regions_file(location);
    json regions;
    regions_file >> regions;

    int N = regions["features"].size();
    for (int i = 0; i < N; i++) {
        string wkt = regions["features"][i]["properties"]["wkt"];
        int lower_limit = regions["features"][i]["properties"]["lower_limit"];
        int upper_limit = regions["features"][i]["properties"]["upper_limit"];

        AirspaceBoost airspace = AirspaceBoost(wkt, lower_limit, upper_limit);
        add_airspace(airspace);
    }

    return N;
}

vector<int> MultiAirspace::query_point(float x, float y, int height) {
    point_xy point = point_xy(x, y);
    //box point = box(point_xy(x, y), point_xy(x, y));

    vector<value> result_rtree;
    rtree.query(bgi::intersects(point), back_inserter(result_rtree));

    vector<int> result;
    BOOST_FOREACH(value const &v, result_rtree) {
        int id = v.second;
        if (airspaces[id].inside(x, y, height)) {
            result.push_back(id);
        }
    }

    return result;
}

vector<int> MultiAirspace::query_box(box query) {
    auto b = bgi::qbegin(rtree, bgi::intersects(query)),
        e = bgi::qend(rtree);

    auto range = boost::make_iterator_range(b, e);

    return boost::copy_range<std::vector<int>>(
            range | boost::adaptors::transformed([](value const& p) { return p.second; }));
}

vector<pair<int, float>> MultiAirspace::airspaces_near_point(float x, float y, int height, int k) {
    point_xy point = point_xy(x, y);

    vector<value> result_rtree;
    rtree.query(bgi::intersects(point), back_inserter(result_rtree));

    int n = result_rtree.size();
    result_rtree.clear();

    rtree.query(bgi::nearest(point, n+k), back_inserter(result_rtree));

    vector<pair<int, float>> result;
    BOOST_FOREACH(value const &v, result_rtree) {
        int id = v.second;
        if (!airspaces[id].inside(x, y, height)) {
            float distance = airspaces[id].distance(point, height);
            result.push_back(pair<int, float>(id, distance));
        }
    }

    sort(result.begin(), result.end(), [](const pair<int, float> &a, const pair<int, float> &b) -> bool
    {
        return a.second < b.second;
    });

    return result;
}

long unsigned int MultiAirspace::size() {
    return airspaces.size();
}

/*
void MultiAirspace::process_flight(Flight &flight, vector<vector<int>> &out) {
    int N = size();
    assert(out.size() >= N && out[0].size() >= N);

    vector<bool> *spaces1 = new vector<bool>(N);
    vector<bool> *spaces2 = new vector<bool>(N);
    fill(spaces1->begin(), spaces1->end(), false);
    fill(spaces2->begin(), spaces2->end(), false);

    for (int i = 0; i < flight.vertices; i++) {
        vector<value> result_rtree;
        rtree.query(bgi::intersects(point_xy(flight.vertices_x[i], flight.vertices_y[i])), back_inserter(result_rtree));

        BOOST_FOREACH(value const &v, result_rtree) {
            int j = v.second;
            if (airspaces[j].inside(flight.vertices_x[i], flight.vertices_y[i], flight.vertices_height[i])) {
                spaces2->at(j) = true;
                if (!spaces1->at(j)) {
                    for (int k = 0; k < N; k++) {
                        if (spaces1->at(k)) {
                            out[k][j] += 1;
                        }
                    }
                }
            }
        }
        fill(spaces1->begin(), spaces1->end(), false);
        swap(spaces1, spaces2);
    }
}
*/

void MultiAirspace::process_flight(Flight &flight, vector<vector<int>> &out) {
    int N = size();
    assert(out.size() >= N && out[0].size() >= N);

    vector<int> do_check = query_box(flight.bbox);

    vector<bool> *spaces1 = new vector<bool>(N);
    vector<bool> *spaces2 = new vector<bool>(N);
    fill(spaces1->begin(), spaces1->end(), false);
    fill(spaces2->begin(), spaces2->end(), false);

    int count;

    for (int i = 0; i < flight.vertices; i++) {
        count = 0;
        BOOST_FOREACH(int const &j, do_check) {
            if (airspaces[j].inside(flight.vertices_x[i], flight.vertices_y[i], flight.vertices_height[i])) {
                count++;
                spaces2->at(j) = true;
                if (!spaces1->at(j)) {
                    for (int k = 0; k < N; k++) {
                        if (spaces1->at(k)) {
                            out[k][j] += 1;
                        }
                    }
                }
            }
        }
        if (count > 0) {
            fill(spaces1->begin(), spaces1->end(), false);
            swap(spaces1, spaces2);
        }
        else {
        }
    }
}

vector<pair<int, int>> MultiAirspace::process_single_flight(Flight &flight) {
    int N = size();

    vector<pair<int, int>> out;

    vector<int> do_check = query_box(flight.bbox);

    vector<bool> *spaces1 = new vector<bool>(N);
    vector<bool> *spaces2 = new vector<bool>(N);
    fill(spaces1->begin(), spaces1->end(), false);
    fill(spaces2->begin(), spaces2->end(), false);

    int count;

    for (int i = 0; i < flight.vertices; i++) {
        count = 0;
        BOOST_FOREACH(int const &j, do_check) {
            if (airspaces[j].inside(flight.vertices_x[i], flight.vertices_y[i], flight.vertices_height[i])) {
                count++;
                spaces2->at(j) = true;
                if (!spaces1->at(j)) {
                    for (int k = 0; k < N; k++) {
                        if (spaces1->at(k)) {
                            out.push_back(make_pair(k, j));
                        }
                    }
                }
            }
        }
        if (count > 0) {
            fill(spaces1->begin(), spaces1->end(), false);
            swap(spaces1, spaces2);
        }
        else {
        }
    }
}
