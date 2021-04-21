import pytest
import numpy as np
from utils import check_q

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
    feasible_ranges = {'robot_joint_1' :  {'lower' : -np.radians(170), 'upper' : np.radians(170)}, 
                       'robot_joint_2' :  {'lower' : -np.radians(190), 'upper' : np.radians(45)},
                       'robot_joint_3' :  {'lower' : -np.radians(120), 'upper' : np.radians(156)},
                       'robot_joint_4' :  {'lower' : -np.radians(185), 'upper' : np.radians(185)},
                       'robot_joint_5' :  {'lower' : -np.radians(120), 'upper' : np.radians(120)},
                       'robot_joint_6' :  {'lower' : -np.radians(350), 'upper' : np.radians(350)},
                      }

    print("Testing random configurations...")
    for _ in range(n_attempts):
        q = np.random.rand(n_jts)
        for i, jt_name in enumerate(feasible_ranges.keys()):
            q[i] = q[i] * (feasible_ranges[jt_name]['upper'] - feasible_ranges[jt_name]['lower']) + \
                           feasible_ranges[jt_name]['lower']
        check_q(get_fk, get_ik, q, feasible_ranges)
    print("Done!")

