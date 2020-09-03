#include "processing.h"


vector<Flight> extract_flights(string location) {
    ifstream flights_file(location);
    json flights_json;
    flights_file >> flights_json;

    vector<Flight> flights = vector<Flight>();

    int N = flights_json["flights"].size();
    for (int i = 0; i < N; i++) {
        vector<float> xs = vector<float>();
        vector<float> ys = vector<float>();
        vector<int> hs = vector<int>();
        
        bool broken = false;

        int M = flights_json["flights"][i].size();
        for (int j = 0; j < M; j++) {
            if (flights_json["flights"][i][j][2].is_null()) {
                broken = true;
                break;
            }

            xs.push_back(flights_json["flights"][i][j][0]);
            ys.push_back(flights_json["flights"][i][j][1]);
            hs.push_back((int) flights_json["flights"][i][j][2]);
        }

        if (!broken) {
            flights.push_back(Flight(xs.size(), xs, ys, hs));
        }
    }

    return flights;
}

/*
MultiAirspace extract_airspaces2(string location) {
    MultiAirspace airspaces;

    extract_airspaces_new(location, airspaces);

    return airspaces;
}

void extract_airspaces_new(string location, MultiAirspace &airspaces) {
    ifstream regions_file(location);
    json regions;
    regions_file >> regions;

    int N = regions["features"].size();
    for (int i = 0; i < N; i++) {
        string wkt = regions["features"][i]["properties"]["wkt"];
        int lower_limit = regions["features"][i]["properties"]["lower_limit"];
        int upper_limit = regions["features"][i]["properties"]["upper_limit"];

        AirspaceBoost airspace = AirspaceBoost(wkt, lower_limit, upper_limit);
        airspaces.add_airspace(airspace);
    }
}
*/

void process_flights(vector<Flight> &flights, MultiAirspace &airspaces, vector<vector<int>> &out, bool progress) {
    int num_flights = flights.size();
    for (int i = 0; i < num_flights; i++) {
        if (progress && i % 5 == 0) progress_bar((float) i / (float) num_flights);
        airspaces.process_flight(flights[i], out);
    }

    if (progress) {
        progress_bar(1.0);
        printf("\n");
    }
}