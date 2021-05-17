#!/usr/bin/env python
from os.path import join
from waflib.extras.symwaf2ic import get_toplevel_path

def depends(ctx):
    # config for doxygen
    ctx('code-format')

    # Demos/Tutorial depends on everything
    ctx('much-demos-such-wow')


def options(opt):
    opt.load('doxygen')
    opt.load('python')
    opt.load('sphinx')


def configure(cfg):
    cfg.load('python')
    cfg.load('sphinx')
    cfg.check_python_module('sphinx_rtd_theme')
    cfg.check_python_module('myst_parser')
    cfg.check_python_module('breathe')


def build(bld):

    # build the in-code/API docs
    for proj in ['haldls', 'lola', 'stadls', 'fisch', 'hxcomm']:
        tgen = bld.get_tgen_by_name(f'doxygen_{proj}')
        tgen.post()

    # all-in build

    # sphinx-build

