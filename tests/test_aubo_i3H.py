import os
import pytest
import numpy as np
from utils import check_q, DATA_DIR
from ikfast_aubo_i3H import get_fk, get_ik, get_num_dofs, get_free_dofs
from compas.robots import RobotModel

_NEUTRAL = np.array([-0.03, 0.46, 1.01, 0.92, 0.10, 0.00])


def test_aubo_i3H(n_attempts, capsys):
    print('*****************\n aubo_i3H ikfast_pybind test')
    n_jts = get_num_dofs()
    free_jts = get_free_dofs()
    # assert n_jts == 6 and n_free_jts == 1
    with capsys.disabled():
        print('aubo_i3H: \nn_jts: {}, n_free_jts: {}'.format(n_jts, len(free_jts)))

    urdf_path = os.path.join(DATA_DIR, 'aubo_i3H.urdf')
    robot_model = RobotModel.from_urdf_file(urdf_path)
    feasible_ranges = {}
    for joint in robot_model.joints:
        # add joint limits if it is not fixed
        if joint.limit and joint.limit.lower is not None and joint.limit.upper is not None:
            feasible_ranges[joint.name] = {'lower': joint.limit.lower, 'upper': joint.limit.upper}
    assert len(feasible_ranges) == n_jts

    assert len(_NEUTRAL) == n_jts
    for i, jt_name in enumerate(feasible_ranges.keys()):
        assert feasible_ranges[jt_name]['lower'] <= _NEUTRAL[i] <= feasible_ranges[jt_name]['upper']

    print("Testing neutral configuration...")
    assert check_q(get_fk, get_ik, _NEUTRAL, feasible_ranges, free_joint_ids=free_jts)

    print("Testing random configurations...")
    n_success = 0
    for _ in range(n_attempts):
        q = np.random.rand(n_jts)
        for i, jt_name in enumerate(feasible_ranges.keys()):
            q[i] = q[i] * (feasible_ranges[jt_name]['upper'] - feasible_ranges[jt_name]['lower']) + \
                           feasible_ranges[jt_name]['lower']
        success = check_q(get_fk, get_ik, q, feasible_ranges, free_joint_ids=free_jts)
        n_success += int(success)
    print("Success rate: {}".format(n_success/n_attempts))
    print("Done!")
