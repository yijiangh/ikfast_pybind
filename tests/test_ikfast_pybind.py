from __future__ import print_function

import pytest
import numpy as np
from numpy.testing import assert_equal, assert_almost_equal
EPS = 1e-6

def test_kuka_kr6_r900():
    from ikfast_kuka_kr6_r900 import get_fk, get_ik, get_dof, get_free_dof
    print('*****************')
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

    # Test inverse kinematics: get joint angles from end effector pose
    print("Testing inverse kinematics:")
    jt_sols = get_ik(pos, rot)
    n_sols = len(jt_sols)
    print("%d solutions found:" % (n_sols))

    for jt_conf in jt_sols:
        assert len(jt_conf) == n_jts
        # print(jt_conf)

    # Check cycle-consistency of forward and inverse kinematics
    assert(np.any([np.sum(np.abs(np.asarray(jt_conf)
                                 - np.asarray(given_jt_conf))) < EPS
                   for jt_conf in jt_sols]
                  ))


def test_abb_irb4600_40_255():
    from ikfast_abb_irb4600_40_255 import get_fk, get_ik, get_dof, get_free_dof
    print('*****************')
    n_jts = get_dof()
    n_free_jts = get_free_dof()
    assert n_jts == 6 and n_free_jts == 0
    print('abb_irb4600_40_255: \nn_jts: {}, n_free_jts: {}'.format(n_jts, n_free_jts))

    # Test forward kinematics: get end effector pose from joint angles
    print("Testing forward kinematics:")
    given_jt_conf = [0.08, -1.57, 1.74, 0.08, 0.17, -0.08] # in radians
    # given_jt_conf = [0, 0, 0, 0, 0, 0] # in radians
    pos, rot = get_fk(given_jt_conf)
    print('jt_conf: {}'.format(given_jt_conf))
    print('ee pos: {}, rot: {}'.format(pos, rot))

    # Test inverse kinematics: get joint angles from end effector pose
    print("Testing inverse kinematics:")
    jt_sols = get_ik(pos, rot)
    n_sols = len(jt_sols)
    print("%d solutions found:" % (n_sols))

    for jt_conf in jt_sols:
        assert len(jt_conf) == n_jts
        print(jt_conf)

    # Check cycle-consistency of forward and inverse kinematics
    # assert(np.any([np.sum(np.abs(np.asarray(jt_conf)
    #                              - np.asarray(given_jt_conf))) < EPS
    #                for jt_conf in jt_sols]
    #               ))


def test_ur5():
    from ikfast_ur5 import get_fk, get_ik, get_dof, get_free_dof
    print('*****************')
    n_jts = get_dof()
    n_free_jts = get_free_dof()
    # assert n_jts == 6 and n_free_jts == 1
    print('ur5: \nn_jts: {}, n_free_jts: {}'.format(n_jts, n_free_jts))

    # Test forward kinematics: get end effector pose from joint angles
    print("Testing forward kinematics:")
    given_jt_conf = [-3.1, -1.6, 1.6, -1.6, -1.6, 0.] # in radians
    pos, rot = get_fk(given_jt_conf)
    print('jt_conf: {}'.format(given_jt_conf))
    print('ee pos: {}, rot: {}'.format(pos, rot))

    # Test inverse kinematics: get joint angles from end effector pose
    print("Testing inverse kinematics:")
    jt_sols = get_ik(pos, rot)
    n_sols = len(jt_sols)
    print("%d solutions found:" % (n_sols))

    for jt_conf in jt_sols:
        assert len(jt_conf) == n_jts
        print(jt_conf)

    # Check cycle-consistency of forward and inverse kinematics
    # assert(np.any([np.sum(np.abs(np.asarray(jt_conf)
    #                              - np.asarray(given_jt_conf))) < EPS
    #                for jt_conf in jt_sols]
    #               ))
