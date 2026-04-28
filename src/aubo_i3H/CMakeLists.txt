pybind11_add_module(ikfast_aubo_i3H
	ikfast_pybind_wrapper.cpp
	ikfast_source.cpp
	)

target_link_libraries(ikfast_aubo_i3H PRIVATE ${LAPACK_LIBRARIES})