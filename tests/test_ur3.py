import pytest
import numpy as np
from utils import check_q

@pytest.mark.ur3
# @pytest.mark.skip(reason='The ur3 ikfast module seems to be very unstable. Ignore this while we are still debugging')
def test_ur3(n_attempts):
    from ikfast_ur3 import get_fk, get_ik, get_dof, get_free_dof
    print('*****************\n UR5 ikfast_pybind test')
    n_jts = get_dof()
    n_free_jts = get_free_dof()
    # assert n_jts == 6 and n_free_jts == 1
    print('ur5: \nn_jts: {}, n_free_jts: {}'.format(n_jts, n_free_jts))

    # print("Testing multiples of pi/2...")
    # for i1 in range(0,5):
    #     for i2 in range(0,5):
    #         for i3 in range(0,3):
    #             for i4 in range(0,5):
    #                 for i5 in range(0,5):
    #                     for i6 in range(0,5):
    #                         q = [i1*np.pi/2., i2*np.pi/2., i3*np.pi/2., 
    #                              i4*np.pi/2., i5*np.pi/2., i6*np.pi/2.]
    #                         check_q(get_fk, get_ik, q)

    feasible_ranges = {'robot_joint_1' :  {'lower' : -6.28318530718,     'upper' : 6.28318530718}, 
                       'robot_joint_2' :  {'lower' : -6.28318530718,     'upper' : 6.28318530718},
                       'robot_joint_3' :  {'lower' : -6.28318530718 / 2, 'upper' : 6.28318530718 / 2},
                       'robot_joint_4' :  {'lower' : -6.28318530718,     'upper' : 6.28318530718},
                       'robot_joint_5' :  {'lower' : -6.28318530718,     'upper' : 6.28318530718},
                       'robot_joint_6' :  {'lower' : -6.28318530718,     'upper' : 6.28318530718},
                      }

    print("Testing random configurations...")
    for _ in range(n_attempts):
        q = np.random.rand(n_jts)
        for i, jt_name in enumerate(feasible_ranges.keys()):
            q[i] = q[i] * (feasible_ranges[jt_name]['upper'] - feasible_ranges[jt_name]['lower']) + \
                           feasible_ranges[jt_name]['lower']
        check_q(get_fk, get_ik, q, feasible_ranges, free_joint_ids=[5])
    print("Done!")

