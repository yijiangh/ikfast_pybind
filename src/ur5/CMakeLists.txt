pybind11_add_module(ikfast_ur5
	ikfast_pybind_ur5.cpp
	ur_kinematics/ur_kin.cpp
	# ikfast/ikfast61.cpp
	)

target_compile_features(ikfast_ur5 PRIVATE cxx_range_for)
