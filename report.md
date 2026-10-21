# CS3210 Tutorial 08 Report

## Exercise 10
* `i7-7700` has  `FrequencyMaxMHz = 4200`, `FrequencyBaseMHz = 3600`, and 8 PUs. `xs-4114` has  `FrequencyMaxMHz = 3000` and `FrequencyBaseMHz = 2200`, and 20 PUs. According to `lstopo`.
* `i7-7700` wins over `xs-4114`. `i7-7700` PUs can run faster than `xs-4114` due to higher frequency. `xs-4114` greater number of PUs don't help because only 5 processes are spawned, which both node types have more than enough PUs to map 1 process each to.
* `mixed` performs in between. While both `i7-7700` and `xs-4114` perform better than on their standalone runs, due to [less contention between the threads used for `mm-mpi` and other processes?]. However, the master thread still has to wait on the slowest `xs-4114` worker before joining, hence it finishes in between `i7-7700` and `xs-4114`.

## Exercise 11
* Only 1 node, with different number of tasks. Since `i7-7700` has 8 PUs, each PU can take 1 task each in 1st run, but not in 2nd run.
* In 2nd run, there is [more context switching in the CPUs between 8 PUs, 9 tasks, and other processes?]. This balloons the communication time between workers which causes it to run slower overall.
* `srun --ntasks=5 --nodes=1 --partition=i7-7700 ./mm-mpi 256`
  `srun --ntasks=9 --nodes=1 --overcommit --partition=i7-7700 ./mm-mpi 256`

## Exercise 12
* Check the number of PUs on the node, and limit the number of workers to be 1 less than that. 