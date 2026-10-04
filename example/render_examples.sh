#!/usr/bin/env bash

set -e

cd "$(dirname "$0")"

../render.py ./francis_chrism_mass.md
../render.py --web ./francis_chrism_mass.md
