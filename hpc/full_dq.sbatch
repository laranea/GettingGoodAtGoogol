#!/bin/bash

#SBATCH --job-name=dq
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=2
#SBATCH --mem=32GB
#SBATCH --time=8:00:00
#SBATCH --output=slurm_dq_%j.out
#SBATCH --mail-type=END
#SBATCH --mail-user=ehd255@nyu.edu

module purge
module load python3/intel/3.6.3
source /home/ehd255/pyenv/py3.6.3/bin/activate

python /home/ehd255/DeepGoogol/train_dq.py \
    --device cuda \
    --net basic \
    --net_params 2_128_0.0 \
    --batch_size 256 \
    --target_update 100 \
    --optimizer rmsprop \
    --loss huber \
    --mem_size 1000 \
    --p_to_s stateMax \
    --gamma 0.9 \
    --epsilon 0.1 \
    --eps_decay .00001 \
    --s_cost 0 \
    --v_fn vIdx \
    --lo 1 \
    --hi 100000 \
    --n_idx 50 \
    --replace False \
    --reward_fn topN \
    --reward 10_10_11 \
    --n_games 100000 \
    --n_print 10000 \
    --delay 0 \
    --lo_eval 1 \
    --hi_eval 100000 \
    --n_idx_eval 50 \
    --replace_eval False \
    --reward_fn_eval scalar \
    --reward_eval 1_1 \
    --n_games_eval 10000 \
    --n_print_eval 1000 \
    --delay_eval 0 \
    --file_path /home/ehd255/DeepGoogol/results/dqa.pkl \
    --sc_file_path /home/ehd255/DeepGoogol/results/dqa_sc.pkl
