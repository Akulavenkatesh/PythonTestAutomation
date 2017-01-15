#!/bin/sh
cd -- "$(dirname "$0")"
cd 01_BDD_Tier/features
python3 ./trigger_build_batch_execution_V2.py