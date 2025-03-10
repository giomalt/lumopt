# Continuous adjoint optimization wrapper for Lumerical
LumOpt fork. Original package:
https://github.com/chriskeraly/LumOpt

This fork modifies the original code as:
- imports `lumapi` diffrently (see `replace_import.py`)
- updates two methods to be compatible with last version of `matplotlib` 

## Introduction

This is a continuous adjoint opimtization wrapper for Lumerical, using Python as the main user interface. It is released under an MIT license. It is still work in progress 
and any contribution will be very welcome! New features to come out soon, and make it even easier to use (hopefully)!

If you use this tool in any published work, please cite https://www.osapublishing.org/oe/abstract.cfm?uri=oe-21-18-21693 and give a link to this repo. Thanks!

## Tutorials, Examples, and Documentation

It is all here: https://lumopt.readthedocs.io/en/latest/

## Download and install
Move to package folder of main repo
`cd .\packages\`

Download the modified LumOpt package from my GitHub repository
`git submodule add https://github.com/giomalt/lumopt.git packages/LumOpt`

Install it via
`python setup.py develop`

## Check that it works:
Run an example:
`cd examples/Ysplitter`
`python splitter_opt_2D.py`