
from sympy import symbols
from metric import cyclomatic_complexity, npath_complexity, path_complexity, fcn_call_path_complexity, eqn_solve_tests
from core.log import Log, LogLevel


if __name__ == '__main__':
    T0, T1, V0_0, V0_1, V0_2, V0_3, V0_4, V0_5, V0_6, V0_7, V0_8, V0_9, V0_10, V0_11, V0_12, V0_13, V0_14, V0_15, V0_16, V0_17, V0_18, V0_19, V0_20, V1_0, V1_1, V1_2, V1_3, V1_4, V1_5, V1_6, V1_7, V1_8, V1_9, V1_10, V1_11, V1_12, V1_13, V1_14, V1_15, V1_16, V1_17, V1_18, V1_19, V1_20, V1_21, x = symbols('T0 T1 V0_0 V0_1 V0_2 V0_3 V0_4 V0_5 V0_6 V0_7 V0_8 V0_9 V0_10 V0_11 V0_12 V0_13 V0_14 V0_15 V0_16 V0_17 V0_18 V0_19 V0_20 V1_0 V1_1 V1_2 V1_3 V1_4 V1_5 V1_6 V1_7 V1_8 V1_9 V1_10 V1_11 V1_12 V1_13 V1_14 V1_15 V1_16 V1_17 V1_18 V1_19 V1_20 V1_21 x')

    full_sys = [-T0 + V0_0*x, -T1 + V1_0*x, -V0_0 + 2*T0*T1*x, -V1_0 + x]
    symbs = [T0, T1, V0_0, V1_0]
    print('SYSTEM', full_sys)
    log = Log(log_level=LogLevel.DEBUG)
    eqnSolverTest = eqn_solve_tests.EqnSolverTest(log)
    eqnSolverTest.fcn_call_apc(full_sys, symbs)