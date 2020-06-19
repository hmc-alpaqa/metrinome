"""."""
import subprocess
import re


def parse_klee_simple(klee_output):
    """."""
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
    """."""
    klee_path = "/app/build/bin/klee"
    results_dict = {}
    for preference in preferences:
        for depth in max_depths:
            for input_ in inputs:
                root_dir = f"/app/code/tests/cFiles/simpleAlgs"
                name = f"klee_{preference}_{depth}_{input_}_{function}_output"
                output_folder = f"{root_dir}/{name}".replace(" ", "_")
                cmd = f"{klee_path}-stats --table-format=simple --print-all {output_folder}"
                stats = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, check=False)
                stats_decoded = stats.stdout.decode().split("\n")
                headers = stats_decoded[0].split()[1:]
                values = map(float, stats_decoded[2].split()[1:])
                stats_dict = dict(zip(headers, values))
                klee_info_cmd = f"cat {output_folder}/info"
                klee_info = subprocess.run(klee_info_cmd, shell=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, check=False)
                klee_results = parse_klee_simple(klee_info.stdout.decode())
                stats_dict["GeneratedTests"], stats_dict["CompletedPaths"], _ = klee_results
                results_dict[(preference, depth, input_)] = stats_dict
    return results_dict


# def graph_stat_regr(function, preference, max_depths, inputs, results, field):
#     """."""
#     subprocess.run("mkdir /app/code/tests/cFiles/simpleAlgs/graphs2/", shell=True)
#     fig1, ax1 = plt.subplots()
#     depths = [float(i) for i in max_depths]
#     for input_ in inputs:
#         stats = [results[(preference, i, input_)][field] for i in max_depths]
#         ax1.plot(depths, stats, label="data")
#         for deg in [3]:
#             IB = [2.5]
#             # p, residuals, rank, singular_values, rcond = \
#             #   np.polyfit(np.array(depths), np.array(stats), deg, full=True)
#             # ax1.plot(depths, poly(depths, p, deg), label=f"degree={deg}")
#             ax1.plot(*SegmentedLinearReg(X, Y, initial_breakpoints), '-r')
#         exp_coefs, _ = curve_fit(exp_function, depths, stats)
#         ax1.plot(depths, [exp_function(d, *exp_coefs) for d in depths], label="exponential")
#     ax1.set(xlabel='depth', ylabel=field, title=function)
#     ax1.legend()
#     ax1.grid()

#     root_dir = "/app/code/tests/cFiles/simpleAlgs"
#     fig1.savefig(f"{root_dir}/graphs2/{field}_{function}.png".replace("%", "percent"))
#     plt.close(fig1)

# fields = ["ICov(%)", 'BCov(%)', "CompletedPaths", "GeneratedTests"]
# functions = ['02_fib']
# for func in functions:
#     log = Log()
#     kleeu = KleeUtils(log)
#     filename = f"/app/code/tests/cFiles/simpleAlgs/{func}.c"
#     output = kleeu.show_func_defs(filename)
#     for i in output:
#         results = generate_results(preferences, max_depths, inputs, f"{func}_{i}")
#         for field in fields:
#             graph_stat_regr(func, preferences[0], max_depths, inputs, results, field)

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
    #             ax1.plot(*SegmentedLinearReg(times, data[field], init_bps), '-r',
    #                      label="REGRESSION")
    #             ax1.set(xlabel='depth', ylabel=field, title=temp_func)
    #             ax1.legend()
    #             ax1.grid()
    #             root_dir = "/app/code/tests/cFiles/simpleAlgs"
    #             name = f"{root_dir}/graphspandas/{field}_{temp_func}.png"
    #             fig1.savefig(name.replace("%","percent"))
    #             plt.close(fig1)
    # bp = [3, 7]
    # X = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    # Y = [0, 1, 2, 3, 4, 5, 5, 5, 5, 5, 5, 4, 3, 2, 1]
    # print(SegmentedLinearReg(X, Y, bp, 2))
