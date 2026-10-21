#!/bin/bash
#SBATCH --job-name=ex10-i7
#SBATCH --partition=i7-7700
#SBATCH --nodes=1
#SBATCH --ntasks=5
#SBATCH --time=00:30:00
#SBATCH --output=ex10_i7_%j.out

# Exercise 10, config 1: one i7-7700 node, 5 processes, --cpu-bind=thread

RUNS=5
SIZE=2048
NAME=i7
CSV="results/ex10_${NAME}.csv"
LOGDIR=ex10_logs

cd "$SLURM_SUBMIT_DIR"
mkdir -p "$LOGDIR"
echo "config,run,rank,role,node,comm_time_s,comp_time_s,total_time_s" > "$CSV"

for run in $(seq 1 $RUNS); do
    log="$LOGDIR/${NAME}_run${run}.log"
    srun --cpu-bind=thread ./mm-mpi $SIZE > "$log" 2>&1
    awk -v cfg="$NAME" -v run="$run" '
        /communication_time=|total time=/ {
            gsub(/=/, "= "); gsub(/[():;]/, " ")
            node = $5; sub(/[.].*/, "", node); sub(/.*-/, "", node)
            if ($2 == "WORKER") print cfg "," run "," $3 ",worker," node "," $7 "," $10 ","
            else                print cfg "," run "," $3 ",master," node ",,," $8
        }' "$log" | sort -t, -k3,3n >> "$CSV"
done
