from klee_algs import *
import numpy as np
from numpy.linalg import lstsq
from scipy.optimize import curve_fit


fields = ["ICov(%)",'BCov(%)',"CompletedPaths","GeneratedTests"]
functions = ['02_fib']

def poly(input, coef, deg):
    return [sum([k*(i**j) for j,k in zip(list(range(deg+1))[::-1], coef)]) for i in input]

def exp_function(x, a, b, c):
    return a * np.exp(-b * x) + c



ramp = lambda u: np.maximum( u, 0 )
step = lambda u: ( u > 0 ).astype(float)

def SegmentedLinearReg( X, Y, breakpoints ):
    nIterationMax = 50

    breakpoints = np.sort( np.array(breakpoints) )

    dt = np.min( np.diff(X) )
    ones = np.ones_like(X)

    for i in range( nIterationMax ):
        # Linear regression:  solve A*p = Y
        Rk = [ramp( X - xk ) for xk in breakpoints ]
        Sk = [step( X - xk ) for xk in breakpoints ]
        A = np.array([ ones, X ] + Rk + Sk )
        p =  lstsq(A.transpose(), Y, rcond=None)[0]

        # Parameters identification:
        a, b = p[0:2]
        ck = p[ 2:2+len(breakpoints) ]
        dk = p[ 2+len(breakpoints): ]

        # Estimation of the next break-points:
        newBreakpoints = breakpoints - dk/ck

        # Stop condition
        if np.max(np.abs(newBreakpoints - breakpoints)) < dt/5:
            break

        breakpoints = newBreakpoints
    else:
        print( 'maximum iteration reached' )

    # Compute the final segmented fit:
    Xsolution = np.insert( np.append( breakpoints, max(X) ), 0, min(X) )
    ones =  np.ones_like(Xsolution)
    Rk = [ c*ramp( Xsolution - x0 ) for x0, c in zip(breakpoints, ck) ]

    Ysolution = a*ones + b*Xsolution + np.sum( Rk, axis=0 )

    return Xsolution, Ysolution

def parse_klee_simple(klee_output):
    string_one = "generated tests = "
    string_two = "completed paths = "
    string_three = "total instructions = "

    generated_tests_index    = klee_output.index(string_one) + len(string_one)
    completed_paths_index    = klee_output.index(string_two) + len(string_two)
    total_instructions_index = klee_output.index(string_three) + len(string_three)

    number_regex = re.compile("[0-9]+")

    tests_match = number_regex.match(klee_output[generated_tests_index:])
    paths_match = number_regex.match(klee_output[completed_paths_index:])
    insts_match = number_regex.match(klee_output[total_instructions_index:])

    if tests_match is not None:
        tests = int(tests_match.group())
    if paths_match is not None:
        paths = int(paths_match.group())
    if insts_match is not None:
        insts = int(insts_match.group())
    return tests, paths, insts

def generate_results(preferences, max_depths, inputs, function):
    klee_path = "/app/build/bin/klee"
    results_dict = {}
    for preference in preferences:
        for depth in max_depths:
            for input in inputs:
                output_folder = f"/app/code/tests/cFiles/simpleAlgs/klee_{preference}_{depth}_{input}_{function}_output".replace(" ","_")
                cmd = f"{klee_path}-stats --table-format=simple --print-all {output_folder}"
                stats = subprocess.run(cmd, shell=True, stdout=PIPE, stderr=PIPE)
                stats_decoded = stats.stdout.decode().split("\n")
                headers = stats_decoded[0].split()[1:]
                values = map(lambda x: float(x), stats_decoded[2].split()[1:])
                stats_dict = dict(zip(headers, values))
                klee_info_cmd = f"cat {output_folder}/info"
                klee_info = subprocess.run(klee_info_cmd, shell=True, stdout=PIPE, stderr=PIPE)
                klee_results = parse_klee_simple(klee_info.stdout.decode())
                stats_dict["GeneratedTests"], stats_dict["CompletedPaths"], _ = klee_results
                results_dict[(preference, depth, input)] = stats_dict
    return results_dict


def graph_stat_regr(function, preference, max_depths, inputs, results, field):
    subprocess.run("mkdir /app/code/tests/cFiles/simpleAlgs/graphs2/", shell=True)
    fig1, ax1 = plt.subplots()
    depths = [float(i) for i in max_depths]
    for input in inputs:
        stats = [results[(preference,i,input)][field] for i in max_depths]
        ax1.plot(depths, stats, label = "data")
        for deg in [3]:
            IB = [2.5]
            # p, residuals, rank, singular_values, rcond = np.polyfit(np.array(depths), np.array(stats), deg, full=True)
            # ax1.plot(depths, poly(depths, p, deg), label=f"degree={deg}")
            ax1.plot(*SegmentedLinearReg( X, Y, initialBreakpoints ), '-r' )
        exp_coefs, _ = curve_fit(exp_function, depths, stats)
        ax1.plot(depths, [exp_function(d, *exp_coefs) for d in depths], label="exponential")
    ax1.set(xlabel='depth', ylabel=field, title=function)
    ax1.legend()
    ax1.grid()

    fig1.savefig(f"/app/code/tests/cFiles/simpleAlgs/graphs2/{field}_{func}.png".replace("%","percent"))
    plt.close(fig1)



for func in functions:
    log = Log()
    kleeu = KleeUtils(log)
    filename = f"/app/code/tests/cFiles/simpleAlgs/{func}.c"
    output = kleeu.show_func_defs(filename)
    for i in output:
        results = generate_results(preferences, max_depths, inputs, f"{func}_{i}")
        for field in fields:
            graph_stat_regr(func, preferences[0],max_depths, inputs, results, field)


    # for f in functions:
    #     for field in fields:
    #         generate_graphs(f, field)
    # for f in functions:
    #     for sz in array_sizes:
    #         for field in fields:
    #             temp_func = f+str(sz)
    #             fig1, ax1 = plt.subplots()
    #             data = pd.read_csv(f"/app/code/tests/cFiles/simpleAlgs/frames/{temp_func}.csv")
    #             times = [float(i.split()[2]) for i in data.iloc[:,0]]
    #             init_bps = [3]
    #             ax1.plot(times, data[field], label = "OG")
    #             ax1.plot(*SegmentedLinearReg(times, data[field], init_bps), '-r', label="REGRESSION")
    #             ax1.set(xlabel='depth', ylabel=field, title=temp_func)
    #             ax1.legend()
    #             ax1.grid()
    #             fig1.savefig(f"/app/code/tests/cFiles/simpleAlgs/graphspandas/{field}_{temp_func}.png".replace("%","percent"))
    #             plt.close(fig1)
    # bp = [3, 7]
    # X = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    # Y = [0, 1, 2, 3, 4, 5, 5, 5, 5, 5, 5, 4, 3, 2, 1]
    # print(SegmentedLinearReg(X, Y, bp, 2))
