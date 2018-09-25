# MCNP-FMESH-parser
Python parser for basic MCNP FMESH output files

## Requirements:
- rectangular FMESH type 4.
- one or no energy bins.
- "OUT" set to "IJ" on the FMESH card.

## usage
./parse.py [input] [output]

### input
The msht file location provided by MCNP.

### output
The matlab export location, optional, defaults to: "./mesh.mat".

## Author
Diederik Feilzer - 2018
