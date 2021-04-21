import pytest
import numpy as np
from utils import check_q

@pytest.mark.franka
def test_franka_panda(n_attempts):
    from ikfast_franka_panda import get_fk, get_ik, get_dof, get_free_dof
    print('*****************\n franka_panda ikfast_pybind test')
    n_jts = get_dof()
    n_free_jts = get_free_dof()
    # assert n_jts == 6 and n_free_jts == 1
    print('franka_panda: \nn_jts: {}, n_free_jts: {}'.format(n_jts, n_free_jts))

    feasible_ranges = {
                       'robot_joint_1' :  {'lower' : -2.8973, 'upper' : 2.8973}, 
                       'robot_joint_2' :  {'lower' : -1.7628, 'upper' : 1.7628},
                       'robot_joint_3' :  {'lower' : -2.8973, 'upper' : 2.8973},
                       'robot_joint_4' :  {'lower' : -3.0718, 'upper' : -0.0698},
                       'robot_joint_5' :  {'lower' : -2.8973, 'upper' : 2.8973},
                       'robot_joint_6' :  {'lower' : -0.0175, 'upper' : 3.7525},
                       'robot_joint_7' :  {'lower' : -2.8973, 'upper' : 2.8973},
                      }

    pos, rot = get_fk([0] * n_jts)
    assert not get_ik(pos, rot, [])
    assert not get_ik(pos, rot, [1,1])
    assert not get_ik(pos, rot, [1,1,1,1])

    print("Testing random configurations...")
    for _ in range(n_attempts):
        q = np.random.rand(n_jts)
        for i, jt_name in enumerate(feasible_ranges.keys()):
            q[i] = q[i] * (feasible_ranges[jt_name]['upper'] - feasible_ranges[jt_name]['lower']) + \
                           feasible_ranges[jt_name]['lower']
        check_q(get_fk, get_ik, q, feasible_ranges, free_joint_ids=[6])
    print("Done!")