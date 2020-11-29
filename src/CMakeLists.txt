include_directories(
		${IKFAST_PYBIND_EXTERNAL}
		${IKFAST_PYBIND_SOURCE_DIR})

add_subdirectory(kuka_kr6_r900)
add_subdirectory(abb_irb4600_40_255)
add_subdirectory(ur3)
add_subdirectory(ur5)
add_subdirectory(eth_rfl)
add_subdirectory(franka_panda)

# added by https://github.com/Simon-Steinmann
add_subdirectory(kukakr10r1100sixx)
add_subdirectory(kukakr120r2500pro)
add_subdirectory(kukakr1502)
add_subdirectory(kukakr162)
add_subdirectory(kukakr3r540)
add_subdirectory(kukakr5arc)
add_subdirectory(kukakr6r700sixx)
add_subdirectory(kukakr6r900sixx)
add_subdirectory(ur10e)
add_subdirectory(ur3e)
add_subdirectory(ur5e)
add_subdirectory(p_rob3)
add_subdirectory(puma560)

# keep adding folders here...
# add_subdirectory(abb_4600_xxx)

