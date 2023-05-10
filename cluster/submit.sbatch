#!/bin/sh

#SBATCH --account=pi-svaikunt
#SBATCH --partition=svaikunt
#SBATCH --error="%j.err"
#SBATCH --output="%j.out"

singularity exec --contain --bind $HOME/.xmds --bind $PWD --pwd $PWD /project/svaikunt/singularity_containers/xmds_sandbox.sif run_xmds actin.xmds
