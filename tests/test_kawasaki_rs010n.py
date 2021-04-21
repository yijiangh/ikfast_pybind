import pytest
import numpy as np
from ikfast_kawasaki_rs010n import get_fk, get_ik, get_dof, get_free_dof
from utils import check_q

@pytest.mark.kawasaki_rs010n
def test_kawasaki_rs010n(n_attempts):
    print('*****************\n ABB_IRB4600_40_255 ikfast_pybind test')
    n_jts = get_dof()
    n_free_jts = get_free_dof()
    assert n_jts == 6 and n_free_jts == 0
    print('kawasaki_rs010n: \nn_jts: {}, n_free_jts: {}'.format(n_jts, n_free_jts))

    feasible_ranges = {'robot_joint_1' :  {'lower' : -3.141, 'upper' : 3.14159}, 
                       'robot_joint_2' :  {'lower' : -1.833,   'upper' : 2.531},
                       'robot_joint_3' :  {'lower' : -2.845,   'upper' : 2.618},
                       'robot_joint_4' :  {'lower' : -4.712,   'upper' : 4.712},
                       'robot_joint_5' :  {'lower' : -2.531,   'upper' : 2.531},
                       'robot_joint_6' :  {'lower' : -6.283,   'upper' : 6.283}
                      }

    print("Testing random configurations...")
    for _ in range(n_attempts):
        q = np.random.rand(n_jts)
        for i, jt_name in enumerate(feasible_ranges.keys()):
            q[i] = q[i] * (feasible_ranges[jt_name]['upper'] - feasible_ranges[jt_name]['lower']) + \
                           feasible_ranges[jt_name]['lower']
        check_q(get_fk, get_ik, q, feasible_ranges)
    print("Done!")