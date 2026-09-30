pybind11_add_module(ikfast_irb6700_150_320
	ikfast_pybind_wrapper.cpp
	ikfast_source.cpp
	)

target_link_libraries(ikfast_irb6700_150_320 PRIVATE ${LAPACK_LIBRARIES})