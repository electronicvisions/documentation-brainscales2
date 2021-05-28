# Software Development


## Development Environments

### CLI-based IDEs

```{todo}
Describe the visionary neovim (no emacs/etc. users anymore?) flow here :).
```

### GUI-based IDEs

#### VS Code

The following steps will explain how to setup `vscode` in conjunction with `ssh` to enable your local IDE to interact with a remote server (cf.  [LSP](https://en.wikipedia.org/wiki/Language_Server_Protocol)) running in a containerized environment.
Due to `vscode`'s limited configurability we *abuse* `ssh/.authorized_keys` to containerize the working environment.
Similarly, environment modules are also unsupported by `vscode`, we use `.env` files to inject the environment variables.

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
          RequestTTY yes
  # …
  ```
* Enable ssh-key-based login and adjust it to startup within the latest container environment.
  Add your public key to the file and prefix it:
  ```
  hel $ editor .ssh/authorized_keys
  #…
  command="singularity shell --app dls /containers/stable/latest" ssh-rsa YOUR_PUBLIC_KEY_YOUR_PUBLIC_KEY
  ```
* Use the extension (`Remote-SSH: Connect to Host…`) to connect to `hel-vscode`.
* Open a new terminal and verify that it runs on the remote host within the dls app in the container.
  ```
  hel $ hostname
  helvetica.kip.uni-heidelberg.de
  hel $ pwd
  YOUR_HOME
  hel $ env | grep ^SINGULARITY
  SINGULARITY_NAME=latest
  SINGULARITY_CONTAINER=/containers/stable/latest
  SINGULARITY_APPNAME=dls
  ```

To enable Python-related functionality in `vscode` the `Python` extension needs to be installed on the remote site.
See [here](https://code.visualstudio.com/docs/languages/python) for details (please note that some plugins can be installed per site (local vs. remote), wihle others are global).
To verify that it works, open a `Python` file and test some of the IDE functionality (e.g. *jump to declaration*).
It might be useful to inject software from the environment and/or workspace into your `vscode` environment..
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
