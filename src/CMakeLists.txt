include_directories(
		${IKFAST_PYBIND_EXTERNAL}
		${IKFAST_PYBIND_SOURCE_DIR})

add_subdirectory(kuka_kr6_r900)
add_subdirectory(abb_irb4600_40_255)
add_subdirectory(ur3)
add_subdirectory(ur5)

# keep adding folders here...
# add_subdirectory(abb_4600_xxx)
