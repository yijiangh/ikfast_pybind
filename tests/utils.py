import numpy as np

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

