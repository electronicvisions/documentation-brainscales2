# BrainScaleS-2 User Documentation

This repository builds the BrainScaleS-2 user documentation including:
* high-level user documentation
* demos and tutorials
* API reference documenation


## Build instructions

```shell
# 1) Most of the following steps will be executed within a singularity container
#    To keep the steps clutter-free, we start by defining an alias
shopt -s expand_aliases
alias c="singularity exec --app dls /containers/stable/latest"

# 2) Prepare a fresh workspace and change directory into it
mkdir workspace && cd workspace

# 3) Load waf build tool
module load waf

# 4) Setup your workspace and clone all dependencies (--clone-depth=1 to skip history)
c ./waf setup --project=documentation-brainscales2

# 5) Build the project
cat <<EOF >build.sh
./waf configure
./waf build -j1
EOF
srun -p compile -c8 c bash build.sh

# 6) Install the project to ./bin and ./lib
c ./waf install
```
