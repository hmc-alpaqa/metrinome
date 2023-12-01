def main() -> None:

    klee_path = "/app/build/bin/klee" # location of the klee command
    src_filepath = "/app/code/tests/cFiles/benchmark/kleeversions/kleetest_summer2023/cFiles/" # location of source files to run klee on, end with a slash
    filepath = "/app/code/tests/cFiles/benchmark/kleeversions/kleetest_fall2023/" # directory to create (if it doesn't exist) and put all results/created files in
                                                                        # both filepaths needs to end with a slash
    # src_filepath = "/app/code/tests/cFiles/fse_2020_benchmark/"
    # filepath =   "/app/code/tests/cFiles/fse_2020_benchmark/kleetest/"
    klee_params_lambda = lambda output, var, filepath: f" --output-dir={output} --max-depth={var} {filepath}"
    # klee_params_lambda = lambda output, var, filepath: f" --output-dir={output} --max-time={var}min --watchdog {filepath}"
    # f" --output-dir={output} --max-depth={var} {filepath}"
    # --dump-states-on-halt=false --max-time=5min
    # lambda function to generate klee commands
    # should take in an outpute filepath, a number to vary, and an input filepath
    # shouldn't actually contain the call to klee

    xlabel = "max depth" # label for the x-axis (parameter that is being varied)


    # pregenerated = ['lina_bac_sub', 'lina_cmp', 'lina_cofactor', 'lina_comp_transpose', 'lina_conjugate', 'lina_cramer',
    # 'lina_create_dvector', 'lina_createvector', 'lina_crossProduct', 'lina_determinant', 'lina_disp_cmpMat', 'lina_disp_floatMat',
    # 'lina_disp_intMat', 'lina_dotProduct', 'lina_for_sub', 'lina_has_converged', 'lina_ishermitian', 'lina_lup_sol', 'lina_matrix_inverse',
    # 'lina_matrix_multiplication', 'lina_max', 'lina_print_dVector', 'lina_printVector', 'lina_Read_cmpMat', 'lina_Read_intMat', 'lina_Read_Vector',
    # 'lina_rpm', 'lina_scalarTripleProduct', 'lina_scale', 'lina_transpose', 'lina_vect_mat_multiplication', 'lina_vectorTripleProduct']
    pregenerated = []

    file_generation_function = lambda src_filepath, file_path, file_name: list(zip(generate_files(src_filepath, file_path, file_name, False) if file_name not in pregenerated else generate_files_premade(src_filepath, file_path, file_name)))
    # file_generation_function = lambda src_filepath, file_path, file_name: list(zip(generate_files(src_filepath, file_path, file_name, False), generate_files(src_filepath, file_path, file_name, True)))
    # should be a callable object that takes in a source folder, output folder, and file name
    # returns a tuple of names for files, if each was compiled differently (ie optimized vs normal) and also compiles/generates the necessary files for klee


# 'lina_bac_sub', 'lina_cmp', 'lina_cofactor', 'lina_comp_transpose', 'lina_conjugate', 'lina_cramer',
# 'lina_create_dvector', 'lina_createvector', 'lina_crossProduct', 'lina_determinant', 'lina_disp_cmpMat', 'lina_disp_floatMat',
# 'lina_disp_intMat', 'lina_dotProduct', 'lina_for_sub', 'lina_has_converged', 'lina_ishermitian', 'lina_lup_sol', 'lina_matrix_inverse',
# 'lina_matrix_multiplication', 'lina_max', 'lina_print_dVector', 'lina_printVector', 'lina_Read_cmpMat', 'lina_Read_intMat', 'lina_Read_Vector',
# 'lina_rpm', 'lina_scalarTripleProduct', 'lina_scale', 'lina_transpose', 'lina_vect_mat_multiplication', 'lina_vectorTripleProduct',
# 'recursive_func', 'merge_sort', 'quick-sort',
    # functions = ['digital-root-multiplicative-digital-root', 'parsing-rpn-calculator-algorithm-2', 'arrays-10', 'chinese-remainder-theorem', 'multifactorial', 'combinations-1', 'spiral-matrix-2', 'non-continuous-subsequences-3', 'mutual-recursion', 'huffman-coding-2', 'ulam-spiral--for-primes--2', 'quickselect-algorithm', '24-game', 'combinations-with-repetitions', 'binary-search', 'abc-problem', 'iterated-digits-squaring-2', 'n-queens-problem-1', 'power-set', 'zebra-puzzle-1', 'percolation-site-percolation-2', 'reverse-words-in-a-string', 'greatest-common-divisor-2', 'ackermann-function-1', 'happy-numbers-1', 'catalan-numbers-1', 'permutation-test-1', 'heronian-triangles', 'factorial-3', 'factorial-5', 'factorial-4', 'towers-of-hanoi-1', 'long-multiplication-1', 'permutations-by-swapping', 'balanced-ternary', 'call-an-object-method', 'truncatable-primes-3', 'pascals-triangle-2', 'permutations-derangements', 'matrix-arithmetic-1', 'topswops-1', 'sorting-algorithms-stooge-sort', 'hailstone-sequence-2', 'sorting-algorithms-radix-sort', 'stern-brocot-sequence-1', 'visualize-a-tree', 'dinesmans-multiple-dwelling-problem', 'sorting-algorithms-quicksort-1', 'sorting-algorithms-quicksort-2', 'sierpinski-carpet-3', 'find-limit-of-recursion-2', 'find-limit-of-recursion-1', 'palindrome-detection-3', 'ordered-partitions-2', 'sudoku', 'fibonacci-sequence-1', 'levenshtein-distance-1']
    # functions = ['lina_determinant']
    functions = ['partition']
    # functions = ['even_odd']


    labels = ["normal"] # the labels for the different "compilation methods"

    # xaxis = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15','20','25','50','100','500','1000'] # for even_odd
    # xaxis = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15','20','25','50','100','500','1000'] # for factorial
    #xaxis = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15'] #for quicksort
    # xaxis = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15','20','25','27','28','29','30','33',"35",'36'] #for fib_rec_wrapper
    # xaxis = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13','14','15','20','25','30','35','40','50','100','150'] #for binary search
    xaxis = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15','16','17'] #for partition
    # xaxis = ['20','21','22','23','24','30','50']
    # xaxis = ['1', '2', '3', '200']
    timeout = 1000 #timeout
    fields = ["ICov(%)", 'BCov(%)', "CompletedPaths", "GeneratedTests", "RealTime", "UserTime",
              "SysTime", "PythonTime"] # all klee output fields that we are interested in
    remove = True # whether klee files should be deleted after the important data is collected. Usually set to True

    prepare(klee_path, src_filepath, filepath, file_generation_function, functions, klee_params_lambda, xlabel, labels, xaxis, fields, remove, timeout) #run the experiment




if __name__ == "__main__":
    main()






#JUNK
    # xaxis = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14',
    #               '15', '16', '17', '18', '19', '20', '30', '40', '50', '60', '70', '80', '90',
    #               '100'] # all possible values for the input variable
    # xaxis = ['1', '2', '5']

    # STUFF THAT DOESNT WORK FROM THE STUFF ELI SENT ME functions = ['k-d-tree', 'currying', 'tic-tac-toe', 'parsing-rpn-to-infix-conversion', 'parse-an-ip-address-1', 'walk-a-directory-recursively-1', ]

# working : ['9-billion-names-of-god-the-integer', '24-game-solve', '24-game', 'abc-problem', 'ackermann-function-1', 'ackermann-function-2',
# # 'aks-test-for-primes', 'aliquot-sequence-classifications-1', 'aliquot-sequence-classifications-2', 'almost-prime', 'anagrams-2',
# # 'arbitrary-precision-integers--included--3-strexp', 'arbitrary-precision-integers--included--3-strmult']
# ['arena-storage-pool-7_add_mem_entry', 'arena-storage-pool-7_remove_mem_entry', 'arena-storage-pool-7_customFree', 'arena-storage-pool-7_customMalloc']



    # to look at later: 'anagrams-1', 'anagrams-deranged-anagrams', 'animate-a-pendulum', 'animation', 'anonymous-recursion'
    # 'apply-a-callback-to-an-array-2',
    # 'arithmetic-complex-2', 'arithmetic-geometric-mean-1', 'arithmetic-geometric-mean-2', 'arithmetic-geometric-mean-calculate-pi', 'arithmetic-rational',
    # 'array-concatenation', 'arrays-10', 'simpletest']
    # functions = ['simpletest']
    # functions = []

    # functions = ['test-01', 'test-02', 'test-03', 'test-04', 'test-05', 'test-06', 'test-07', 'test-08', 'test-09', 'test-10', 'test-11',
    # 'test-12', 'test-20-un-inlined', 'test-21-un-inlined', 'test-22-un-inlined', 'test-23-un-inlined', 'test-24-un-inlined', 'test-25-un-inlined',
    # 'test-30-un-inlined', 'test-31-un-inlined', 'test-32-un-inlined', 'test-33-un-inlined', 'test-34-un-inlined', 'test-35-un-inlined',
    # 'test-36-un-inlined', 'test-37-un-inlined', 'test-38-un-inlined', 'test-39-un-inlined', 'test-40-un-inlined'] # all the functions to run klee experiments on
    # functions = ['02_fib_no_helper', '04_mincoins_no_helper', '05_nCr_no_helper', '07_bubblesort_no_helper', '08_selectionsort_no_helper',
    # '09_insertionsort_no_helper', '11_deletevowels_no_helper', '12_deleteword_no_helper', '14_sortascending_no_helper', '15_maxarray_no_helper',
    # '16_printprimes_no_helper', '17_printarmstrongs_no_helper', '18_binarymultiply_no_helper',
    # '19_binarytogray_no_helper', '22_edit_dist_no_helper', '23_mergesort_no_helper', '24_longest_common_increasing_subsequence_no_helper']
    # functions = ['08_selectionsort_no_helper', 'selectionsort']
    # functions = ['selectionsort']
    # functions = ['04_mincoins_no_helper']
    # functions = ['06_binarysearch_no_helper']
    # functions = ['18_binarymultiply_no_helper']

    # pregenerated = ['9-billion-names-of-god-the-integer', 'arbitrary-precision-integers--included--3-strexp', 'arbitrary-precision-integers--included--3-strmult',
    # 'arena-storage-pool-7_add_mem_entry', 'arena-storage-pool-7_remove_mem_entry', 'arena-storage-pool-7_customFree', 'arena-storage-pool-7_customMalloc',
    # 'active-object_update', 'active-object_tick', 'active-object_set_input', 'active-object_new_integ', 'active-object_sine']
