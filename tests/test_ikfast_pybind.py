from __future__ import print_function

import pytest
import math
import numpy as np
from numpy.testing import assert_equal, assert_almost_equal


@pytest.fixture
def n_attempts():
    return 10000


def best_sol(sols, q_guess, weights, feasible_ranges):
    """get the best solution based on UR's joint domain value and weighted joint diff
    modified from :
    https://github.com/ros-industrial/universal_robot/blob/kinetic-devel/ur_kinematics/src/ur_kinematics/test_analytical_ik.py

    """
    valid_sols = []
    for sol in sols:
        test_sol = np.ones(6)*9999.
        for i in range(6):
            for add_ang in [-2.*np.pi, 0, 2.*np.pi]:
                test_ang = sol[i] + add_ang
                if test_ang <= feasible_ranges[i]['upper'] and \
                   test_ang >= feasible_ranges[i]['lower'] and \
                   abs(test_ang - q_guess[i]) < abs(test_sol[i] - q_guess[i]):
                    test_sol[i] = test_ang
        if np.all(test_sol != 9999.):
            valid_sols.append(test_sol)
    if len(valid_sols) == 0:
        return None
    best_sol_ind = np.argmin(np.sum((weights*(valid_sols - np.array(q_guess)))**2,1))
    return valid_sols[best_sol_ind]


def check_q(fk_fn, ik_fn, q, feasible_ranges, free_joint_id=None, diff_tol=1e-3):
    pos, rot = fk_fn(q)
    if free_joint_id:
        sols = ik_fn(pos, rot, q[free_joint_id])
    else:
        sols = ik_fn(pos, rot)

    qsol = best_sol(sols, q, [1.]*6, feasible_ranges)
    if qsol is None:
        qsol = [999.]*6
    diff = np.sum(np.abs(np.array(qsol) - q))
    if diff > diff_tol:
        print(np.array(sols))
        print('Best q:', qsol)
        print('Actual:', np.array(q))
        print('Diff L1 norm:', diff)
        print('Diff:  ', q - qsol)
        print('Difdiv:', (q - qsol)/np.pi)
        # if raw_input() == 'q':
        #     sys.exit()
        assert False


@pytest.mark.kuka
def test_kuka_kr6_r900(n_attempts):
    from ikfast_kuka_kr6_r900 import get_fk, get_ik, get_dof, get_free_dof
    print('*****************\n KUKA_KR6_R900 ikfast_pybind test')
    n_jts = get_dof()
    n_free_jts = get_free_dof()
    assert n_jts == 6 and n_free_jts == 0
    print('kuka_kr6_r900: \nn_jts: {}, n_free_jts: {}'.format(n_jts, n_free_jts))

    # Test forward kinematics: get end effector pose from joint angles
    print("Testing forward kinematics:")
    given_jt_conf = [0.08, -1.57, 1.74, 0.08, 0.17, -0.08] # in radians
    pos, rot = get_fk(given_jt_conf)
    print('jt_conf: {}'.format(given_jt_conf))
    print('ee pos: {}, rot: {}'.format(pos, rot))

    # https://github.com/ros-industrial/kuka_experimental/blob/indigo-devel/kuka_kr6_support/urdf/kr6r900sixx_macro.xacro
    feasible_ranges = [{'lower' : -math.radians(170), 'upper' : math.radians(170)}, 
                       {'lower' : -math.radians(190), 'upper' : math.radians(45)},
                       {'lower' : -math.radians(120), 'upper' : math.radians(156)},
                       {'lower' : -math.radians(185), 'upper' : math.radians(185)},
                       {'lower' : -math.radians(120), 'upper' : math.radians(120)},
                       {'lower' : -math.radians(350), 'upper' : math.radians(350)},
                      ]

    print("Testing random configurations...")
    for _ in range(n_attempts):
        q = np.random.rand(6)
        for i in range(6):
            q[i] = q[i] * (feasible_ranges[i]['upper'] - feasible_ranges[i]['lower']) + \
                   feasible_ranges[i]['lower']
        check_q(get_fk, get_ik, q, feasible_ranges)
    print("Done!")


@pytest.mark.abb
@pytest.mark.skip(reason='This ikfast cpp module need to be regenerated.')
def test_abb_irb4600_40_255(n_attempts):
    from ikfast_abb_irb4600_40_255 import get_fk, get_ik, get_dof, get_free_dof
    print('*****************\n ABB_IRB4600_40_255 ikfast_pybind test')
    n_jts = get_dof()
    n_free_jts = get_free_dof()
    assert n_jts == 6 and n_free_jts == 0
    print('abb_irb4600_40_255: \nn_jts: {}, n_free_jts: {}'.format(n_jts, n_free_jts))

    feasible_ranges = [{'lower' : -3.14159, 'upper' : 3.14159}, 
                       {'lower' : -1.5708,  'upper' : 2.61799},
                       {'lower' : -3.14159, 'upper' : 1.309},
                       {'lower' : -6.98132, 'upper' : 6.98132},
                       {'lower' : -2.18166, 'upper' : 2.0944},
                       {'lower' : -6.98132, 'upper' : 6.98132}
                      ]

    print("Testing random configurations...")
    for _ in range(n_attempts):
        q = np.random.rand(6)
        for i in range(6):
            q[i] = q[i] * (feasible_ranges[i]['upper'] - feasible_ranges[i]['lower']) + \
                   feasible_ranges[i]['lower']
        check_q(get_fk, get_ik, q, feasible_ranges, diff_tol=0.01)
    print("Done!")


@pytest.mark.ur5
@pytest.mark.skip(reason='The ur5 ikfast module seems to be very unstable. Ignore this while we are still debugging')
def test_ur5(n_attempts):
    from ikfast_ur5 import get_fk, get_ik, get_dof, get_free_dof
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

    feasible_ranges = [{'lower' : -3.14159, 'upper' : 3.14159}, 
                       {'lower' : -3.14159, 'upper' : 3.14159},
                       {'lower' : -3.14159 / 2, 'upper' : 3.14159 / 2},
                       {'lower' : -3.14159, 'upper' : 3.14159},
                       {'lower' : -3.14159, 'upper' : 3.14159},
                       {'lower' : -3.14159, 'upper' : 3.14159},
                      ]

    print("Testing random configurations...")
    for _ in range(n_attempts):
        q = np.random.rand(6)
        for i in range(6):
            q[i] = q[i] * (feasible_ranges[i]['upper'] - feasible_ranges[i]['lower']) + \
                   feasible_ranges[i]['lower']
        check_q(get_fk, get_ik, q, feasible_ranges, free_joint_id=5)
    print("Done!")


@pytest.mark.ur3
@pytest.mark.skip(reason='The ur3 ikfast module seems to be very unstable. Ignore this while we are still debugging')
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

    feasible_ranges = [{'lower' : -6.28318530718,     'upper' : 6.28318530718}, 
                       {'lower' : -6.28318530718,     'upper' : 6.28318530718},
                       {'lower' : -6.28318530718 / 2, 'upper' : 6.28318530718 / 2},
                       {'lower' : -6.28318530718,     'upper' : 6.28318530718},
                       {'lower' : -6.28318530718,     'upper' : 6.28318530718},
                       {'lower' : -6.28318530718,     'upper' : 6.28318530718},
                      ]

    print("Testing random configurations...")
    for _ in range(n_attempts):
        q = np.random.rand(6)
        for i in range(6):
            q[i] = q[i] * (feasible_ranges[i]['upper'] - feasible_ranges[i]['lower']) + \
                   feasible_ranges[i]['lower']
        check_q(get_fk, get_ik, q, feasible_ranges, free_joint_id=5)
    print("Done!")