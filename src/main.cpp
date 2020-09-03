#include <iostream>
#include <fstream>
#include <vector>
#include <tuple>

#include "polygon.h"
#include "airspace.h"
#include "flight.h"
#include "processing.h"


int main() {
    // Disable buffering
    setvbuf(stdout, NULL, _IONBF, 0);

    printf("Extracting airspaces... ");
    //MultiAirspace airspaces = extract_airspaces2("regions_usa_wkt.json");
    MultiAirspace airspaces;
    airspaces.add_airspaces_file("regions_usa_wkt.json");
    //extract_airspaces_new("regions_usa_wkt.json", airspaces);
    printf("Done (%lu total).\n", airspaces.size());

    printf("Extracting flights... ");
    //vector<Flight> flights = extract_flights("sample_flights_latest.json");
    vector<Flight> flights = extract_flights("1800.json");
    //vector<Flight> flights = extract_flights("sample_flights_uk.json");
    printf("Done (%lu total).\n", flights.size());

    /*
    vector<float> xs = {0,0,2,4,4};
    vector<float> ys = {0,2,4,2,0};
    Polygon p = Polygon(5, xs, ys);
    Airspace a = Airspace(p, -100, 100);

    printf("%d\n", p.vertices);

    for (int y = 9; y >= 0; y--) {
        float y_test = (((float) y) * 0.5) - 0.5;
        for (int x = 0; x < 10; x++) {
            float x_test = (((float) x) * 0.5) - 0.5;
            printf("%d", a.inside(x_test, y_test, 0));
        }
        printf("\n");
    }
    */

    /*
    int N = airspaces.size();
    int id_max = 0;
    for (int i = 0; i < airspaces.size(); i++) {
        id_max = max(id_max, airspaces[i].id);
    }
    id_max += 1;

    //int N = airspaces.size();
    vector<vector<int>> out(id_max, vector<int> (id_max, 0));

    process_flights(flights, airspaces, id_max, out, true);
    */

    int N = airspaces.size();
    vector<vector<int>> out(N, vector<int> (N, 0));

    process_flights(flights, airspaces, out, true);

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            if (out[i][j] != 0) {
                printf("%d, %d: %d\n", i, j, out[i][j]);
            }
        }
    }

    return 0;
}
