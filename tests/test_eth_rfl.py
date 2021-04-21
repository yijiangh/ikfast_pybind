import pytest
import numpy as np
from utils import check_q

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