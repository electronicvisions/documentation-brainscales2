# Software Development


## General Aspects


(containerized_software_environment)=
### Containerized Software Environment

BrainScaleS adopted a container-based approach to software environments.
In particular, we use [apptainer](https://apptainer.org/documentation)-based containers (which the modern version of `singularity`).
In contrast to many other container ecosystems that focus on persistent services, our approach only provides a *wrapper* for the execution of commands in different environments.
This can be easily layered with SLURM-based execution on our hardware-control cluster.
E.g., to run a command inside a container on the cluster:
```
$ srun -p <PARTITION> apptainer exec <CONTAINER.IMG> <COMMAND>
```
We typically make use of apptainer's `--app <APP>` option to switch between different environments within the container.
For BrainScaleS-2 most users rely on `--app dls`, the CI tries to work on a slimmer software dependency tree available via `--app dls-core`.


### Neuromorphic Resources

We extended SLURM to support special-purpose options describing requested neuromorphic hardware resources.
To run, for example, an experiment on the single-chip lab setup (*cube*s) number 60, FPGA no. 3:
```
$ srun -p cube --wafer 60 --fpga-without-aout 3 <apptainer call> experiment.py
```


(brainscales_build_system)=
## BrainScaleS Build System

The BrainScaleS developers adopted the [waf](https://waf.io/) build system early in the development of the BrainScaleS-1 software eco-system.
In each repository `wscript` files define the configuration, build, installation and tests steps.
It uses the Python language.
In contrast to the upstream code base, we extended the tool by a cross-repo dependency tracking mechanism (see `def depends(ctx):` sections in `wscript`s).
The typical installation flow for a toplevel `X` is:
```
# for github-based builds append "--repo-db-url=https://github.com/electronicvisions/projects" to the next command
$ waf setup --project=X
$ waf configure
$ waf install
```
The first command queries a repository database (default URL hardcoded in our fork of waf) to find and *check out* `X`.
The build tool now looks for `depends()` in `X/wscript` to resolve the dependencies of `X`.
Further dependencies are found recursively.
`waf configure` and `waf build` perform configuration checks as well as build steps similar to other build systems.
Finally, `waf install` by default installs into `{bin,lib,share}/` subfolders of the toplevel workspace.


## Recommendations for Experiment Repositories

Building and executing experiments on BrainScaleS is a complex task.
Typical experiments comprise host-based control flow in C++ and Python and C++ running on the embedded processors.
The [BSS-2 Experiment Template](https://github.com/electronicvisions/template-experiment-dls) provides a template for defining and conducting experiments on the BrainScaleS-2 hardware platform.
This includes:
* Host-based experiment code written
  * in Python
  * and C++
* code running on BrainScaleS' embedded processors written in C++.
The build processes support compilation of host-code as well as the cross-compilation of embedded code.
Automatic tests can be defined and executed via a exemplary Jenkins CI setup.
In particular, the repository employs the same build and CI tools as the remaining BrainScaleS software environment.

Example:
```
$ mkdir my_experiment_workspace
$ cd my_experiment_workspace
$ git clone https://github.com/electronicvisions/template-experiment-dls my_experiment
# for github-based builds append "--repo-db-url=https://github.com/electronicvisions/projects" to the next command
$ waf setup --directory=my_workspace
```
Now continue with the steps described in {ref}`brainscales_build_system`.

## Development Environments

### CLI-based IDEs

```{todo}
Describe the visionary neovim (no emacs/etc. users anymore?) flow here :).
```

#### Emacs

To access remote files directly from your local Emacs instance you can use [`TRAMP`](https://www.gnu.org/software/tramp/).
You can use a ssh config like:
```
$ cat ~/.ssh/config | grep -A4 'Host hel'
Host hel
    HostName brainscales-r.kip.uni-heidelberg.de
    User YOUR_USERNAME
    Port 11022
    ForwardAgent yes
```
and key based authentication, for example using
```
$ ssh-copy-id hel
```
to reduce friction in using `TRAMP`. With a setup like this you can navigate to your home directory on `hel` from your local Emacs by navigating to `/ssh:hel:~/`.

The [`lsp-mode`](https://emacs-lsp.github.io/lsp-mode/page/installation/) plugin adds LSP support Emacs and can transparently work over `TRAMP` aswell.
On `hel` the containerized versions of `clangd` and `pylsp` should be used. You can configure `lsp-mode` to use these using
```
(lsp-register-client
  (make-lsp-client :new-connection (lsp-tramp-connection '("apptainer" "exec" "--app" "dls" "/containers/stable/latest" "clangd"))
                  :major-modes '(c++-mode c-mode)
                  :remote? t
                  :server-id 'clangd-remote))
(lsp-register-client
  (make-lsp-client :new-connection (lsp-tramp-connection '("apptainer" "exec" "--app" "dls" "/containers/stable/latest" "pylsp"))
                  :major-modes '(python-mode)
                  :remote? t
                  :server-id 'pyls-remote)))
```
For `TRAMP` to be able to find the `apptainer` executable one needs to configure `TRAMP` to use the same `PATH` environment variable as the login shell. This can be done using
```
(connection-local-set-profile-variables 'remote-with-apptainer-dls
                                        '((tramp-remote-path . (tramp-own-remote-path tramp-default-remote-path))))
(connection-local-set-profiles
 '(:application tramp :machine "hel") 'remote-with-apptainer-dls)
```
Depending on your ssh configuration you might need to change `"hel"` to match yours.

### GUI-based IDEs

#### VS Code

The following steps will explain how to setup `vscode` in conjunction with `ssh` to enable your local IDE to interact with a remote server (cf.  [LSP](https://en.wikipedia.org/wiki/Language_Server_Protocol)) running in a containerized environment.
Due to `vscode`'s limited configurability we *abuse* `ssh/.authorized_keys` to containerize the working environment.
Similarly, environment modules are also unsupported by `vscode`, we use `.env` files to inject the environment variables.

* See {ref}`brainscales_build_system` and {ref}`containerized_software_environment` for information about the build process and the software environment.
* Install vscode (see [here](https://code.visualstudio.com/docs/setup/setup-overview)), start it up and install the extension `Remote - SSH`.
* For `vscode` a dedicated ssh key pair is needed:
  ```
  local_machine $ ssh-keygen -t rsa
  # /YOUR_HOME/.ssh/hel_vscode.id_rsa
  # …
  ```
* Then setup your ssh client to use it:
  ```
  local_machine $ editor .ssh/config
  # …
  Host hel-vscode
          User YOUR_USERNAME
          Hostname brainscales-r.kip.uni-heidelberg.de
          Port 11022
          IdentityFile /YOUR_HOME/.ssh/hel_vscode.id_rsa
          #RequestTTY yes # ECM (2022-06-29) it seems this is not needed anymore
  # …
  ```
* Enable ssh-key-based login and adjust it to startup within the latest container environment.
  Add your public key to the file and prefix it:
  ```
  hel $ editor .ssh/authorized_keys
  #…
  command="apptainer shell --app dls /containers/stable/latest" ssh-rsa YOUR_PUBLIC_KEY_YOUR_PUBLIC_KEY
  ```
* Newer versions of `vscode` seem to play around with the PATH environment variable, so we need to fix that; append the following to your `.bashrc`:
  ```
  if [ -n "$VSCODE_IPC_HOOK_CLI" ]; then
    if [ -n "${APPTAINER_CONTAINER}" ]; then
      if [ -z "${APPTAINER_APPNAME}" ]; then
        echo "APPTAINER_APPNAME not set"
      else
        # readd to PATH, it gets somehow changed by vscode
        export PATH=/opt/spack_views/visionary-${APPTAINER_APPNAME}/bin:$PATH
        echo "added visionary-${APPTAINER_APPNAME} to PATH"
      fi
    else
      echo "remote vscode not running containerized!"
    fi
  fi
  ```
* Use the extension (`Remote-SSH: Connect to Host…`) to connect to `hel-vscode`.
* Open a new terminal and verify that it runs on the remote host within the dls app in the container.
  ```
  hel $ hostname
  helvetica.kip.uni-heidelberg.de
  hel $ pwd
  YOUR_HOME
  hel $ env | grep ^APPTAINER
  APPTAINER_NAME=latest
  APPTAINER_CONTAINER=/containers/stable/latest
  APPTAINER_APPNAME=dls
  hel $ env | grep PYTHONHOME
  PYTHONHOME=/opt/spack_views/visionary-dls
  hel $ env | grep ^LD_LIBRARY_PATH
  LD_LIBRARY_PATH=/opt/spack_views/visionary-dls/lib:/opt/spack_views/visionary-dls/lib64:/scif/apps/dls/lib::/.singularity.d/libs
  ```

To enable Python-related functionality in `vscode` the `Python` extension needs to be installed on the remote site (`hel-vscode`).
See [here](https://code.visualstudio.com/docs/languages/python) for details (please note that some plugins can be installed per site (local vs. remote), while others are global).
Currently, after installing the Python extension, a subsequent Ctrl + Shift + p to set the path to the Python interpreter ("Python: Select Interpreter") is needed;
use `/opt/spack_views/visionary-dls/bin/python3` as path to the interpreter.
To verify that it works, open a `Python` file and test some of the IDE functionality (e.g. *jump to declaration*).

For C++-related functionality, please install the `C/C++` extension (but not the whole extension pack!) and `clangd`, each on the remote site (`hel-vscode`), but not necessarily locally.
If you encounter errors regarding availablity of `clangd`, try to add `~/bin` to your PATH (e.g. via `.bash_profile`), then create a symlink from `/opt/spack_views/visionary-dls/bin/clangd` to `~/bin/clangd` and retry.
Run your waf configure and build with `bear`, e.g. `srun -p compile … -- bear waf configure && srun -p compile … -- bear -a waf install --test-execnone`.
To verify that it works, open a `C++` file and test some of the IDE functionality (e.g. hover over some type to see additional information, there should be some `clangd` action in the status bar).

Depending on the developers personal preferences, we also recommend using a proper editor interface instead of insufficient emulations.
In particular, instead of using `vscode`'s vim emulation, we recommend to directly run `neovim` using the "VSCode Neovim" extension (installed locally) together wie a locally deployed neovim.

In some cases, it might be useful to inject software from the environment and/or workspace into your `vscode` environment..
One option is to make use of [`.env`](https://code.visualstudio.com/docs/python/environments#_environment-variable-definitions-file) files (in your workspaces) to replicate `module load localdir` behavior, e.g.:
```
$ cd my_workspace
$ cat .env
PATH=/wang/environment/software/container/bss2-stack-for-nice/2021-05-25_1/bin:/opt/spack/opt/spack/linux-debian10-x86_64/gcc-8.3.0/environment-modules-4.7.1-rsm6srwhgjcrplgver43tdeujurrqyyc/bin:/opt/spack_views/visionary-dls/bin:/scif/apps/dls/bin:/scif/apps/dls:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
LD_LIBRARY_PATH=/wang/environment/software/container/bss2-stack-for-nice/2021-05-25_1/lib:/opt/spack_views/visionary-dls/lib:/opt/spack_views/visionary-dls/lib64:/scif/apps/dls/lib:/opt/spack_views/visionary-dls/lib:/opt/spack_views/visionary-dls/lib64:/scif/apps/dls/lib::/.singularity.d/libs:/.singularity.d/libs
PYTHONPATH=/wang/environment/software/container/bss2-stack-for-nice/2021-05-25_1/lib
```
The contents of the variables can be acquired by using the module system in a shell:
```
$ module load localdir
$ env | grep -E "^(|LD_LIBRARY_|PYTHON)PATH=" | tee .env
```


#### pycharm

Add `lib/` to `PYTHONPATH` and `LD_LIBRARY_PATH`, as well as `bin/` to `PATH` (e.g. by using `module load localdir`), then start the IDE locally within the container.
PyCharm also supports running the interpreter remotely, see [here](https://www.jetbrains.com/help/pycharm/configuring-remote-interpreters-via-ssh.html).
