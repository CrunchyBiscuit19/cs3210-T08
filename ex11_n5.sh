#!/bin/bash
#SBATCH --job-name=ex11-n5
#SBATCH --partition=i7-7700
#SBATCH --nodes=1
#SBATCH --ntasks=5
#SBATCH --time=00:30:00
#SBATCH --output=ex11_n5_%j.out

# Exercise 11, config 1: srun -n5 -N1 -p i7-7700 ./mm-mpi 256

RUNS=5
SIZE=256
NAME=n5
CSV=ex11_${NAME}.csv
LOGDIR=ex11_logs

cd "$SLURM_SUBMIT_DIR"
mkdir -p "$LOGDIR"
echo "config,run,rank,role,host,comm_time_s,comp_time_s,total_time_s" > "$CSV"

for run in $(seq 1 $RUNS); do
    log="$LOGDIR/${NAME}_run${run}.log"
    srun -n5 -N1 ./mm-mpi $SIZE > "$log" 2>&1
    awk -v cfg="$NAME" -v run="$run" '
        /communication_time=|total time=/ {
            gsub(/=/, "= "); gsub(/[():;]/, " ")
            if ($2 == "WORKER") print cfg "," run "," $3 ",worker," $5 "," $7 "," $10 ","
            else                print cfg "," run "," $3 ",master," $5 ",,," $8
        }' "$log" | sort -t, -k3,3n >> "$CSV"
done
