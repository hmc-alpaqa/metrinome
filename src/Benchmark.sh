# Add paths to this list
paper_dict='{
   "1": "/app/code/experiments/icse_experiment/files/files.txt",
   "2": "/app/code/experiments/recursion/files/files.txt",
   "3": "/app/code/experiments/function_calls/benchmark/benchmarkFiles.txt",
   "4": "/app/code/tests/cFiles/C-master/CmasterFiles.txt"
   }'

# Add metrics to this list
apc_dict='"1" "2" "3" "4" "5"'

# Add papers below in chronological order :)
lolcat metrinome_ascii.txt
while :;do
   printf "PRESS THE CORRESPONDING NUMBER TO SEE THE BENCHMARKS FROM THAT PAPER.\n\
   1) ICSE 2021 PAPER\n\
   2) FormaliSE 2023 PAPER\n\
   3) ICSE 2024 POSTER\n\
   4) ISSTA 2024 PAPER\n"
   while read paper_num; do
      # check if input in the list and is an integer
      if [[ $paper_dict == *"$paper_num"* && "$paper_num" =~ ^[0-9]+$ ]]; then
         printf "WHICH METRIC WOULD YOU LIKE TO COMPUTE? \n\
   1) APC-IP: Interprocedural APC\n\
   2) NAPC-IP: Naive Interprocedural APC\n\
   3) APC-R: Recursive APC\n\
   4) NPath Complexity\n\
   5) ALL METRICS\n"
         while read apc_num; do
            if [[ $apc_dict == *"$apc_num"* && "$apc_num" =~ ^[0-9]+$ ]]; then
               break
            else
               echo "Not a valid selection! Try Again :)"
               continue
            fi
         done
      else
         echo "Not a valid paper! Try Again :)"
         continue
      fi
      break
   done

   if [[ "$apc_num" == "1" || "$apc_num" == "5" ]]; then
      python3 /app/code/experiments/function_calls/tests/test_getrgf.py $paper_num "$paper_dict"
   fi

   if [[ "$apc_num" == "2" || "$apc_num" == "5" ]]; then
      python3 /app/code/experiments/function_calls/tests/test_fcapc.py $paper_num "$paper_dict"
   fi

   if [[ "$apc_num" == "3" || "$apc_num" == "5" ]]; then
      python3 /app/code/experiments/function_calls/tests/test_rapc.py $paper_num "$paper_dict"
   fi

   if [[ "$apc_num" == "4" || "$apc_num" == "5" ]]; then
      python3 /app/code/experiments/function_calls/tests/test_npath.py $paper_num "$paper_dict"
   fi

   if [[ "$apc_num" == "5" ]]; then
      python3 /app/code/experiments/function_calls/tests/mergeData.py
   fi

   printf "\n\nPRESS 1 TO COMPUTE ANOTHER METRIC. OTHERWISE PRESS ANYTHING ELSE TO EXIT.\n"

   read choice

   if [[ $choice == "1" ]]; then
      continue
   fi
   break
done
