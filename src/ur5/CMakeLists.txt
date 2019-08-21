pybind11_add_module(ikfast_ur5
	ikfast_pybind_ur5.cpp
	# ur_kinematics_updated/ur_kin.cpp
	ur_kinematics/ur_kin.cpp
	)
# target_compile_features(ikfast_ur5 PRIVATE cxx_range_for)