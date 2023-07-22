import os
import pytest
import numpy as np
from utils import check_q, DATA_DIR
from ikfast_abb_crb15000_5_95 import get_fk, get_ik, get_num_dofs, get_free_dofs
from compas.robots import RobotModel

def test_abb_crb15000_5_95(n_attempts):
    print('*****************\n abb_crb15000_5_95 ikfast_pybind test')
    n_jts = get_num_dofs()
    free_jts = get_free_dofs()
    # assert n_jts == 6 and n_free_jts == 1
    print('abb_crb15000_5_95: \nn_jts: {}, n_free_jts: {}'.format(n_jts, len(free_jts)))
 
    urdf_path = os.path.join(DATA_DIR, 'abb_crb15000_5_95.urdf')
    robot_model = RobotModel.from_urdf_file(urdf_path)
    feasible_ranges = {}
    for joint in robot_model.iter_joints():
        # add joint limits if it is not fixed
        if joint.limit.lower is not None and joint.limit.upper is not None:
            feasible_ranges[joint.name] = {'lower': joint.limit.lower, 'upper': joint.limit.upper}

    print("Testing random configurations...")
    for _ in range(n_attempts):
        q = np.random.rand(n_jts)
        for i, jt_name in enumerate(feasible_ranges.keys()):
            q[i] = q[i] * (feasible_ranges[jt_name]['upper'] - feasible_ranges[jt_name]['lower']) + \
                           feasible_ranges[jt_name]['lower']
        check_q(get_fk, get_ik, q, feasible_ranges, free_joint_ids=free_jts)
    print("Done!")