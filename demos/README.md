# Ivy Mechanics Demos

We provide a simple set of interactive demos for the Ivy Mechanics library.
Running these demos is quick and simple.

## Install

First, clone this repo, and install the requirements provided in this demos folder like so:

```bash
git clone https://github.com/ivy-dl/mech.git ~/ivy_mech
cd ~/ivy_mech/demos
python3 -m pip install -r requirements.txt
```

The interactive demos optionally make use of the simulator
[CoppeliaSim](https://www.coppeliarobotics.com/),
and the python wrapper [PyRep](https://github.com/stepjam/PyRep).

To get the full benefit of these demos, CoppeliaSim
and PyRep should both be installed, following the installation [intructions](https://github.com/stepjam/PyRep#install).

If these are not installed, the demos will all still run, but will display pre-rendered images from the simultator.

## Demos

All demos can be run by executing the python scripts directly.
If a demo script is run without command line arguments, then a random backend framework will be selected from those installed.
Alternatively, the `--framework` argument can be used to manually specify a framework from the options
`jax`, `tensorflow`, `torch`, `mxnd` or `numpy`.

To further explore the demos, breakpoints can be added to the scripts at any stage.
Adding `import pdb; pdb.set_trace()` works for python < 3.7,
and the built-in `breakpoint()` can be used for python > 3.7.

### Run Through

For a basic run through the library:

```bash
cd ~/ivy_mech/demos
python3 run_through.py
```

This script, and the various parts of the library, are further discussed in the [Run Through](https://github.com/ivy-dl/mech#run-through) section of the main README.
We advise following along with this section for maximum effect. The demo script should also be opened locally,
and breakpoints added to step in at intermediate points to further explore.

To run the script using a specific backend, tensorflow for example, then run like so:

```bash
python3 run_through.py --framework tensorflow
```

### Target Facing Rotation Matrix

In this demo, a plant pot is dragged around the scene, and a camera is set to
dynamically track the plant pot using the function ivy_mech.target_facing_rotation_matrix.

```bash
cd ~/ivy_mech/demos/interactive
python3 target_facing_rotation_matrix.py
```

Example output from the simulator is given below:

<p align="center">
    <img width="75%" style="display: block;" src='https://github.com/ivy-dl/ivy-dl.github.io/blob/master/img/externally_linked/ivy_mech/demo_a.gif?raw=true'>
</p>

### Polar to Cartesian Co-ordinates

In this demo, an omni-directional camera is dragged around the scene,
and a cartesian point cloud reconstruction is dynamically generated from the omni camera polar depth maps,
using the method ivy_mech.polar_to_cartesian_coords.

```bash
cd ~/ivy_mech/demos/interactive
python3 polar_to_cartesian_coords.py
```
Example output from the simulator, and Open3D renderings, are given below:

<p align="center">
    <img width="75%" style="display: block;" src='https://github.com/ivy-dl/ivy-dl.github.io/blob/master/img/externally_linked/ivy_mech/demo_b.gif?raw=true'>
</p>

## Get Involved

If you have any issues running any of the demos, would like to request further demos, or would like to implement your own, then get it touch.
Feature requests, pull requests, and [tweets](https://twitter.com/ivythread) all welcome!