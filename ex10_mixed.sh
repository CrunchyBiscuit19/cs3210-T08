#!/bin/bash
#SBATCH --job-name=ex10-mixed
#SBATCH --nodes=2
#SBATCH --ntasks=5
#SBATCH --constraint="[i7-7700*1&xs-4114*1]"
#SBATCH --time=00:30:00
#SBATCH --output=ex10_mixed_%j.out

# Exercise 10, config 3: one i7-7700 + one xs-4114 node, 5 processes,
# cyclic distribution, --cpu-bind=thread

RUNS=5
SIZE=2048
NAME=mixed
CSV=ex10_${NAME}.csv
LOGDIR=ex10_logs

cd "$SLURM_SUBMIT_DIR"
mkdir -p "$LOGDIR"
echo "config,run,rank,role,host,comm_time_s,comp_time_s,total_time_s" > "$CSV"

for run in $(seq 1 $RUNS); do
    log="$LOGDIR/${NAME}_run${run}.log"
    srun --distribution=cyclic --cpu-bind=thread ./mm-mpi $SIZE > "$log" 2>&1
    awk -v cfg="$NAME" -v run="$run" '
        /communication_time=|total time=/ {
            gsub(/=/, "= "); gsub(/[():;]/, " ")
            if ($2 == "WORKER") print cfg "," run "," $3 ",worker," $5 "," $7 "," $10 ","
            else                print cfg "," run "," $3 ",master," $5 ",,," $8
        }' "$log" | sort -t, -k3,3n >> "$CSV"
done
