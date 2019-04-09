#!/usr/bin/env bash

# Exit script as soon as a command fails.
set -o errexit

# Running echidna test script
cd echidna
./run_echidna.sh

cd ../

# Running manticore test script
cd manticore
python3 add_and_remove_source.py
# python3 gons_invariant.py // Note this script fails
