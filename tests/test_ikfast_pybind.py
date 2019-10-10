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
    num_jt = len(q_guess)
    valid_sols = []
    for sol in sols:
        test_sol = np.ones(num_jt)*9999.
        for i, jt_name in enumerate(feasible_ranges.keys()):
            for add_ang in [-2.*np.pi, 0, 2.*np.pi]:
                test_ang = sol[i] + add_ang
                if test_ang <= feasible_ranges[jt_name]['upper'] and \
                   test_ang >= feasible_ranges[jt_name]['lower'] and \
                   abs(test_ang - q_guess[i]) < abs(test_sol[i] - q_guess[i]):
                    test_sol[i] = test_ang
        if np.all(test_sol != 9999.):
            valid_sols.append(test_sol)
    if len(valid_sols) == 0:
        return None
    best_sol_ind = np.argmin(np.sum((weights*(valid_sols - np.array(q_guess)))**2,1))
    return valid_sols[best_sol_ind]


def check_q(fk_fn, ik_fn, q, feasible_ranges, free_joint_ids=[], diff_tol=1e-3):
    pos, rot = fk_fn(q)
    if free_joint_ids:
        sols = ik_fn(pos, rot, [q[i] for i in free_joint_ids])
    else:
        sols = ik_fn(pos, rot)

    qsol = best_sol(sols, q, [1.]*len(q), feasible_ranges)
    if qsol is None:
        qsol = [999.]*len(q)
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
    feasible_ranges = {'robot_joint_1' :  {'lower' : -math.radians(170), 'upper' : math.radians(170)}, 
                       'robot_joint_2' :  {'lower' : -math.radians(190), 'upper' : math.radians(45)},
                       'robot_joint_3' :  {'lower' : -math.radians(120), 'upper' : math.radians(156)},
                       'robot_joint_4' :  {'lower' : -math.radians(185), 'upper' : math.radians(185)},
                       'robot_joint_5' :  {'lower' : -math.radians(120), 'upper' : math.radians(120)},
                       'robot_joint_6' :  {'lower' : -math.radians(350), 'upper' : math.radians(350)},
                      }

    print("Testing random configurations...")
    for _ in range(n_attempts):
        q = np.random.rand(n_jts)
        for i, jt_name in enumerate(feasible_ranges.keys()):
            q[i] = q[i] * (feasible_ranges[jt_name]['upper'] - feasible_ranges[jt_name]['lower']) + \
                           feasible_ranges[jt_name]['lower']
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

    feasible_ranges = {'robot_joint_1' :  {'lower' : -3.14159, 'upper' : 3.14159}, 
                       'robot_joint_2' :  {'lower' : -1.5708,  'upper' : 2.61799},
                       'robot_joint_3' :  {'lower' : -3.14159, 'upper' : 1.309},
                       'robot_joint_4' :  {'lower' : -6.98132, 'upper' : 6.98132},
                       'robot_joint_5' :  {'lower' : -2.18166, 'upper' : 2.0944},
                       'robot_joint_6' :  {'lower' : -6.98132, 'upper' : 6.98132}
                      }

    print("Testing random configurations...")
    for _ in range(n_attempts):
        q = np.random.rand(n_jts)
        for i, jt_name in enumerate(feasible_ranges.keys()):
            q[i] = q[i] * (feasible_ranges[jt_name]['upper'] - feasible_ranges[jt_name]['lower']) + \
                           feasible_ranges[jt_name]['lower']
        check_q(get_fk, get_ik, q, feasible_ranges)
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

    feasible_ranges = {'robot_joint_1' :  {'lower' : -3.14159, 'upper' : 3.14159}, 
                       'robot_joint_2' :  {'lower' : -3.14159, 'upper' : 3.14159},
                       'robot_joint_3' :  {'lower' : -3.14159 / 2, 'upper' : 3.14159 / 2},
                       'robot_joint_4' :  {'lower' : -3.14159, 'upper' : 3.14159},
                       'robot_joint_5' :  {'lower' : -3.14159, 'upper' : 3.14159},
                       'robot_joint_6' :  {'lower' : -3.14159, 'upper' : 3.14159},
                      }

    print("Testing random configurations...")
    for _ in range(n_attempts):
        q = np.random.rand(n_jts)
        for i, jt_name in enumerate(feasible_ranges.keys()):
            q[i] = q[i] * (feasible_ranges[jt_name]['upper'] - feasible_ranges[jt_name]['lower']) + \
                           feasible_ranges[jt_name]['lower']
        check_q(get_fk, get_ik, q, feasible_ranges, free_joint_ids=[5])

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


@pytest.mark.eth_rfl
def test_eth_rfl(n_attempts):
    from ikfast_eth_rfl import get_fk, get_ik, get_dof, get_free_dof
    print('*****************\n ETH_RFL ikfast_pybind test')
    n_jts = get_dof()
    n_free_jts = get_free_dof()
    # assert n_jts == 6 and n_free_jts == 1
    print('eth_rfl: \nn_jts: {}, n_free_jts: {}'.format(n_jts, n_free_jts))

    feasible_ranges = {'gantry_x_joint' :   {'lower' : 0,        'upper' : 20}, 
                       'l_gantry_y_joint' : {'lower' : 0,        'upper' : 12.673},
                       'l_gantry_z_joint' : {'lower' : 0,        'upper' : 1.227},
                       'l_robot_joint_1' :  {'lower' : -2.87979, 'upper' : 2.87979}, 
                       'l_robot_joint_2' :  {'lower' : -1.2217,  'upper' : 1.658},
                       'l_robot_joint_3' :  {'lower' : -1.0472,  'upper' : 1.1345},
                       'l_robot_joint_4' :  {'lower' : -3.49,    'upper' : 3.49},
                       'l_robot_joint_5' :  {'lower' : -2.0944,  'upper' : 2.0944},
                       'l_robot_joint_6' :  {'lower' : -6.9813,  'upper' : 6.9813},
                      }

    pos, rot = get_fk([0] * n_jts)
    assert not get_ik(pos, rot, [])
    assert not get_ik(pos, rot, [1])
    assert not get_ik(pos, rot, [1,1,1,1])

    print("Testing random configurations...")
    for _ in range(n_attempts):
        q = np.random.rand(n_jts)
        for i, jt_name in enumerate(feasible_ranges.keys()):
            q[i] = q[i] * (feasible_ranges[jt_name]['upper'] - feasible_ranges[jt_name]['lower']) + \
                           feasible_ranges[jt_name]['lower']
        check_q(get_fk, get_ik, q, feasible_ranges, free_joint_ids=[0, 1, 2])
    print("Done!")


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