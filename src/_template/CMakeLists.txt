pybind11_add_module(ikfast_[put_extension]
	ikfast_pybind_wrapper.cpp
	ikfast_source.cpp
	)

target_link_libraries(ikfast_[put_extension] PRIVATE ${LAPACK_LIBRARIES})