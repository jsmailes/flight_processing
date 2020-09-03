#ifndef PROCESSING_H
#define PROCESSING_H

#include <iostream>
#include <fstream>
#include <vector>
#include <tuple>

#include "json.hpp"
using json = nlohmann::json;

#include "polygon.h"
#include "airspace.h"
#include "flight.h"
#include "helpers.h"

using namespace std;

vector<Flight> extract_flights(string location);


/*
MultiAirspace extract_airspaces2(string location);
void extract_airspaces_new(string location, MultiAirspace &airspaces);
*/

void process_flights(vector<Flight> &flights, MultiAirspace &airspaces, vector<vector<int>> &out, bool progress = false);

#endif
