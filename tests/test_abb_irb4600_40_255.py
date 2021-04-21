import pytest
import numpy as np
from utils import check_q

@pytest.mark.abb_irb4600_40_255
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
        check_q(get_fk, get_ik, q, feasible_ranges, diff_tol=1e-3)
    print("Done!")