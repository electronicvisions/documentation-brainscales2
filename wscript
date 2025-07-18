#!/usr/bin/env python

def depends(ctx):
    # config for doxygen
    ctx('code-format')

    # Demos/Tutorial depends on everything
    ctx('much-demos-such-wow')

    # .. except jaxsnn
    ctx('jax-snn')


def options(opt):
    opt.load('doxygen')
    opt.load('python')
    opt.load('sphinx')


def configure(cfg):
    cfg.load('python')
    cfg.load('sphinx')
    cfg.check_python_module('sphinx_rtd_theme')
    cfg.check_python_module('breathe')


def build(bld):

    # All-in-one documentation build via sphinx. We depend on:
    # * doxygen-generated XML files for the projects mentioned in `depends_on`
    # * symlinks from source/X to the repos containing documentation
    bld(
        target = 'sphinx_documentation_brainscales2',
        features = 'use sphinx',
        sphinx_source = 'source',
        sphinx_output_format = 'html',
        install_path = '${PREFIX}/doc/sphinx_documentation_brainscales2',
        depends_on = ['doxygen_' + proj for proj in [
            'haldls', 'lola', 'stadls', 'fisch', 'hxcomm', 'hate', 'hxtorch',
            'grenade', 'calix']],
        use = ['pynn_brainscales2', 'pygrenade_vx', 'hxtorch', 'calix_pylib',
               'jaxsnn'],
    )


# Explicitly add build synchronization border between the sphinx build and the
# doxygen builds. This is needed as waf's doxygen & sphinx tools do not
# generate the correct outputs / inputs lists --- file in/out tracking can't
# work and the jobs would be spawned too early.
from waflib.TaskGen import feature, after_method
@feature('sphinx')
@after_method('build_sphinx')
def sphinx_tasks_depend_on_doxygen_tasks(self):
    deps = getattr(self, 'depends_on', [])
    for name in set(self.to_list(deps)):
        other = self.bld.get_tgen_by_name(name)
        other.post()
        for dep_task in other.tasks:
            for sphinx_task in self.tasks:
                sphinx_task.set_run_after(dep_task)
