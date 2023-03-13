import sympy
from sympy import symbols, sqrt
from metric import cyclomatic_complexity, npath_complexity, path_complexity, fcn_call_path_complexity, eqn_solve_tests
from core.log import Log, LogLevel

x = sympy.symbols('x')

def taylor_expansion(f, x0, n):
    """
    Compute the Taylor series expansion of function f around x0 up to order n.

    Args:
        f (Sympy function): The function to expand.
        x0 (float): The point around which to expand the function.
        n (int): The order of the expansion.

    Returns:
        A Sympy expression representing the Taylor series expansion.
    """

    taylor = 0
    for i in range(n+1):
        taylor += (f.diff(x, i).subs(x, x0)) / \
            sympy.factorial(i) * (x - x0) ** i

    coeffs_dict = taylor.as_coefficients_dict()
    # get coeffs in a list of increasing degree
    coeffs_list = [coeffs_dict.get(x**i, 0) for i in range(n+1)]
    return coeffs_list

    # return taylor

def list_symbols(full_sys):
    symbols_set = set()
    for eqn in full_sys:
        symbols_set |= set(eqn.free_symbols - {x})
    symbs = list(symbols_set)
    # ensure T0 is first symbol
    symbs.remove(T0)
    symbs.insert(0, T0)
    # ensure T1 is second symbol
    if T1 in symbs:
        symbs.remove(T1)
        symbs.insert(1, T1)
    
    return symbs

def find_taylor_coeffs():
    f = x**5 / ((x - 1) * (x**5 - 1))
    f = x**4 / ((x - 1) * (x**7 - 1))
    f = (x**4 + x**8) / ((1 - x) * (1 - x**8))
    f = 1 / (x**4 * (1-x))
    f = (-sqrt((x + 1)*(2*x**6 + 2*x**5 - 1)*(4*x**17 + 2*x**15 - 4*x**13 - 4*x**12 + 2*x**11 + 8*x**10 + x**9 - 3*x**8 - 3*x**7 + x**6 - 2*x**4 + x**3 + x**2 + x - 1))*(x - 1)**2*(x**2 + x + 1)/(2*x**15) - (x - 1)**4*(x + 1)*(x**2 + x + 1)**2*(2*x**6 + 2*x**5 - 1)/(2*x**15))/(1 - x)
    f = (-x**3 - sqrt(4*x**11 - 4*x**8 + x**6 - 2*x**3 + 1) + 1)/(2*x**6*(1 - x))


    # Compute the Taylor series expansion of f(x) around x0 = 0 up to order n = 5
    x0 = 0
    n = 15
    taylor_series = taylor_expansion(f, x0, n)
    print(taylor_series)
    quit()


if __name__ == '__main__':
    find_taylor_coeffs()

    T0, T1, V0_0, V0_1, V0_2, V0_3, V0_4, V0_5, V0_6, V0_7, V0_8, V0_9, V0_10, V0_11, V0_12, V0_13, V0_14, V0_15, V0_16, V0_17, V0_18, V0_19, V0_20, V1_0, V1_1, V1_2, V1_3, V1_4, V1_5, V1_6, V1_7, V1_8, V1_9, V1_10, V1_11, V1_12, V1_13, V1_14, V1_15, V1_16, V1_17, V1_18, V1_19, V1_20, V1_21, x = symbols('T0 T1 V0_0 V0_1 V0_2 V0_3 V0_4 V0_5 V0_6 V0_7 V0_8 V0_9 V0_10 V0_11 V0_12 V0_13 V0_14 V0_15 V0_16 V0_17 V0_18 V0_19 V0_20 V1_0 V1_1 V1_2 V1_3 V1_4 V1_5 V1_6 V1_7 V1_8 V1_9 V1_10 V1_11 V1_12 V1_13 V1_14 V1_15 V1_16 V1_17 V1_18 V1_19 V1_20 V1_21 x')

    full_sys = [-T0 + V0_0*x, -T1 + V1_0*x, T1*V0_1*x - V0_0, -V0_1 + x, -V1_0 + V1_1*x + V1_2*x, -V1_1 + x, T1*x - V1_2]
    full_sys = [-T0 + T1*x**3, -T1 + x**3 + T1*x**3]
    full_sys = [-T0 + T1**3*x**3, -T1 + x**3 + T1*x**3]
    
    # mergeSort, but it calls fact() instead of merge -> ComplexInfinity 
    full_sys = [-T0 + V0_0*x, -T1 + V1_0*x, -V0_0 + V0_1*x + x, T0**2*T1*x - V0_1, -V1_0 + V1_1*x + V1_2*x, -V1_1 + x, T1*x - V1_2]
    # symbs = [T0, T1, V0_0, V1_0]
    
    symbs = list_symbols(full_sys)

    

    print('SYMBOLS', symbs)
    print('SYSTEM', full_sys)



    log = Log(log_level=LogLevel.DEBUG)
    eqnSolverTest = eqn_solve_tests.EqnSolverTest(log)
    eqnSolverTest.fcn_call_apc(full_sys, symbs)

    