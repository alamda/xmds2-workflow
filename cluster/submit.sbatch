#!/bin/bash

#SBATCH --account=pi-svaikunt
#SBATCH --time=1-12:00:00
#SBATCH --error=%j.err
#SBATCH --output=%j.out
#SBATCH --partition=svaikunt

module load singularity

singularity exec --pwd $PWD --bind $PWD /project/svaikunt/singularity_containers/xmds_sandbox.sif xmds2actin.xmds

