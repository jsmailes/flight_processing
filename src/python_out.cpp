#include "python_out.h"

AirspaceHandler::AirspaceHandler() {
}

int AirspaceHandler::size() {
    return airspaces.size();
}

void AirspaceHandler::reset_result() {
    N = airspaces.size();
    result = vector<vector<int>>(N, vector<int>(N, 0));

    ready = true;
}

int AirspaceHandler::add_airspace(string wkt, int lower_limit, int upper_limit) {
    if (ready) {
        printf("Error: All airspaces must be added before processing begins.\n");
        return -1;
    }

    AirspaceBoost airspace(wkt, lower_limit, upper_limit);
    return airspaces.add_airspace(airspace);
}

int AirspaceHandler::add_airspaces_file(string location) {
    if (ready) {
        printf("Error: All airspaces must be added before processing begins.\n");
        return -1;
    }

    return airspaces.add_airspaces_file(location);
}

py::list AirspaceHandler::process_single_flight(np::ndarray &xs, np::ndarray &ys, np::ndarray &hs) {
    py::list py_output;

    int n = xs.shape(0);
    if (ys.shape(0) != n || hs.shape(0) != n) {
        printf("Error: Mismatch in array lengths.\n");
        return py_output;
    }
    if (xs.get_dtype() != np::dtype::get_builtin<double>()
    || ys.get_dtype() != np::dtype::get_builtin<double>()
    || hs.get_dtype() != np::dtype::get_builtin<double>()) {
        printf("Error: incorrect array type.\n");
        return py_output;
    }

    double* xs_ptr = reinterpret_cast<double*>(xs.get_data());
    double* ys_ptr = reinterpret_cast<double*>(ys.get_data());
    double* hs_ptr = reinterpret_cast<double*>(hs.get_data());
    vector<float> v_xs(n);
    vector<float> v_ys(n);
    vector<int> v_hs(n);

    for (int i = 0; i < n; i++) {
        v_xs[i] = (float) (*(xs_ptr + i));
        v_ys[i] = (float) (*(ys_ptr + i));
        v_hs[i] = metre_to_ft(rint(*(hs_ptr + i)));
    }

    Flight flight(v_xs.size(), v_xs, v_ys, v_hs);
    //vector<pair<int, int>> output;
    vector<pair<int, int>> output = airspaces.process_single_flight(flight);

    for (int i = 0; i < output.size(); i++) {
        py::list output_i;
        output_i.append(output[i].first);
        output_i.append(output[i].second);
        py_output.append(output_i);
    }

    return py_output;
}

void AirspaceHandler::process_flight(np::ndarray &xs, np::ndarray &ys, np::ndarray &hs) {
    if (!ready) {
        reset_result();
    }

    int n = xs.shape(0);
    if (ys.shape(0) != n || hs.shape(0) != n) {
        printf("Error: Mismatch in array lengths.\n");
        return;
    }
    if (xs.get_dtype() != np::dtype::get_builtin<double>()
    || ys.get_dtype() != np::dtype::get_builtin<double>()
    || hs.get_dtype() != np::dtype::get_builtin<double>()) {
        printf("Error: incorrect array type.\n");
        return;
    }

    double* xs_ptr = reinterpret_cast<double*>(xs.get_data());
    double* ys_ptr = reinterpret_cast<double*>(ys.get_data());
    double* hs_ptr = reinterpret_cast<double*>(hs.get_data());
    vector<float> v_xs(n);
    vector<float> v_ys(n);
    vector<int> v_hs(n);

    for (int i = 0; i < n; i++) {
        v_xs[i] = (float) (*(xs_ptr + i));
        v_ys[i] = (float) (*(ys_ptr + i));
        v_hs[i] = metre_to_ft(rint(*(hs_ptr + i)));
    }

    Flight flight(v_xs.size(), v_xs, v_ys, v_hs);
    airspaces.process_flight(flight, result);

    //assert(flight.shape(1) == 3);
    //assert(flight.get_dtype() == np::dtype::get_builtin<double>());

    //int stride0 = flight.strides(0);
    //int stride1 = flight.strides(1);
}

void AirspaceHandler::process_flights_file(string location) {
    if (!ready) {
        reset_result();
    }

    vector<Flight> flights = extract_flights(location);
    process_flights(flights, airspaces, result);
}

py::list AirspaceHandler::airspaces_at_point(float x, float y, int height, bool ft) {
    if (!ready) {
        reset_result();
    }

    float height2 = (float) height;
    if (!ft) {
        height2 = metre_to_ft(height2);
    }

    vector<int> output = airspaces.query_point(x, y, height2);

    py::list py_output;

    for (int i = 0; i < output.size(); i++) {
        py_output.append(output[i]);
    }

    return py_output;
}

py::list AirspaceHandler::airspaces_near_point(float x, float y, int height, bool ft) {
    if (!ready) {
        reset_result();
    }

    float height2 = (float) height;
    if (!ft) {
        height2 = metre_to_ft(height2);
    }

    vector<pair<int, float>> output = airspaces.airspaces_near_point(x, y, height2);

    py::list py_output;

    for (int i = 0; i < output.size(); i++) {
        py_output.append(py::make_tuple(output[i].first, output[i].second));
    }

    return py_output;

    //return vector_to_list(output);
}

float AirspaceHandler::distance_to_airspace(float x, float y, int height, int id) {
    return airspaces.distance_to_airspace(x, y, height, id);
}

np::ndarray AirspaceHandler::get_result() {
    if (!ready) {
        printf("Error: Processing has not yet begun.\n");
        return np::zeros(py::make_tuple(0,0), np::dtype::get_builtin<int>());
    }

    /*
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            result[i][j] = i*N+j+1;
            printf("%i ", result[i][j]);
        }
        printf("\n");
    }
    */

    py::tuple shape = py::make_tuple(N, N);
    //py::tuple strides = py::make_tuple(N * sizeof(int), sizeof(int));
    np::dtype dtype = np::dtype::get_builtin<int>();
    //np::ndarray output = np::from_data(&result[0][0], dtype, shape, strides, py::object());
    //return output.copy();

    np::ndarray output = np::zeros(shape, dtype);

    PyObject* pobj = output.ptr();
    Py_buffer pybuf;
    PyObject_GetBuffer(pobj, &pybuf, PyBUF_SIMPLE);
    void *buf = pybuf.buf;
    int *p = (int*)buf;
    Py_XDECREF(pobj);

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            p[i*N+j] = result[i][j];
        }
    }

    return output;
}

/*
py::object get_flight() {
    py::object traffic = py::import("traffic.data");
    py::object flights = traffic.attr("opensky").attr("history");
    return flights;
}
*/

BOOST_PYTHON_MODULE(process_flights)
{
    np::initialize();

    //py::scope().attr("version") = version;;

    // Add regular functions to the module.
    //py::def("get_flight", get_flight);

    // Expose class
    py::class_<AirspaceHandler>("AirspaceHandler")
        .def("add_airspace", &AirspaceHandler::add_airspace)
        .def("add_airspaces_file", &AirspaceHandler::add_airspaces_file)
        .def("process_single_flight", &AirspaceHandler::process_single_flight)
        .def("process_flight", &AirspaceHandler::process_flight)
        .def("process_flights_file", &AirspaceHandler::process_flights_file)
        .def("airspaces_at_point", &AirspaceHandler::airspaces_at_point)
        .def("airspaces_near_point", &AirspaceHandler::airspaces_near_point)
        .def("distance_to_airspace", &AirspaceHandler::distance_to_airspace)
        .def("reset_result", &AirspaceHandler::reset_result)
        .def("get_result", &AirspaceHandler::get_result)
        .def("size", &AirspaceHandler::size)
        ;
}