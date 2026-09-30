import pytest
import numpy as np
from utils import check_q
from ikfast_irb6700_150_320 import get_fk, get_ik, get_num_dofs, get_free_dofs


@pytest.mark.irb6700_150_320
def test_irb6700_150_320(n_attempts):
    print('*****************\n IRB6700_150_320 ikfast_pybind test')
    n_jts = get_num_dofs()
    free_jts = get_free_dofs()
    assert n_jts == 6 and free_jts == []
    print('irb6700_150_320: \nn_jts: {}, free_jts: {}'.format(n_jts, free_jts))

    # this module's get_ik takes the free-joint values even when there are none
    def ik_fn(pos, rot):
        return get_ik(pos, rot, [])

    # from birr_irb6700_150_320_1.urdf; the wrist keeps the URDF range, not the datasheet's
    feasible_ranges = {'robot_joint_1' :  {'lower' : -2.96706, 'upper' : 2.96706},
                       'robot_joint_2' :  {'lower' : -1.13446, 'upper' : 1.48353},
                       'robot_joint_3' :  {'lower' : -3.14159, 'upper' : 1.22173},
                       'robot_joint_4' :  {'lower' : -5.23599, 'upper' : 5.23599},
                       'robot_joint_5' :  {'lower' : -2.26893, 'upper' : 2.26893},
                       'robot_joint_6' :  {'lower' : -6.28319, 'upper' : 6.28319},
                      }

    print("Testing random configurations...")
    np.random.seed(42)
    for _ in range(n_attempts):
        q = np.random.rand(n_jts)
        for i, jt_name in enumerate(feasible_ranges.keys()):
            q[i] = q[i] * (feasible_ranges[jt_name]['upper'] - feasible_ranges[jt_name]['lower']) + \
                           feasible_ranges[jt_name]['lower']
        check_q(get_fk, ik_fn, q, feasible_ranges)

        # every returned branch must reproduce the queried pose, not just the nearest one
        pos, rot = get_fk(q)
        sols = ik_fn(pos, rot)
        assert sols, 'no IK solution for a configuration produced by FK: {}'.format(q)
        for sol in sols:
            sol_pos, sol_rot = get_fk(sol)
            assert np.allclose(sol_pos, pos, atol=1e-6)
            assert np.allclose(sol_rot, rot, atol=1e-6)

    print("Done!")
