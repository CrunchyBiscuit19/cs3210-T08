#!/bin/bash
#SBATCH --job-name=ex11-n9
#SBATCH --partition=i7-7700
#SBATCH --nodes=1
#SBATCH --ntasks=9
#SBATCH --overcommit
#SBATCH --time=00:30:00
#SBATCH --output=ex11_n9_%j.out

# Exercise 11, config 2: srun -n9 -N1 --overcommit -p i7-7700 ./mm-mpi 256

RUNS=5
SIZE=256
NAME=n9
CSV="results/ex11_${NAME}.csv"
LOGDIR=ex11_logs

cd "$SLURM_SUBMIT_DIR"
mkdir -p "$LOGDIR"
echo "config,run,rank,role,host,comm_time_s,comp_time_s,total_time_s" > "$CSV"

for run in $(seq 1 $RUNS); do
    log="$LOGDIR/${NAME}_run${run}.log"
    srun -n9 -N1 --overcommit ./mm-mpi $SIZE > "$log" 2>&1
    awk -v cfg="$NAME" -v run="$run" '
        /communication_time=|total time=/ {
            gsub(/=/, "= "); gsub(/[():;]/, " ")
            if ($2 == "WORKER") print cfg "," run "," $3 ",worker," $5 "," $7 "," $10 ","
            else                print cfg "," run "," $3 ",master," $5 ",,," $8
        }' "$log" | sort -t, -k3,3n >> "$CSV"
done
