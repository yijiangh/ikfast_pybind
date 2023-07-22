pybind11_add_module(ikfast_abb_crb15000_5_95
	ikfast_pybind_wrapper.cpp
	ikfast_source.cpp
	)

target_link_libraries(ikfast_abb_crb15000_5_95 PRIVATE ${LAPACK_LIBRARIES})