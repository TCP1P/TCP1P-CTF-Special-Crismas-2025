#!/bin/sh
anvil --hardfork cancun --host 0.0.0.0 --port 8545 > /dev/null 2>&1 &
sleep 5
socat tcp-l:8011,reuseaddr,fork exec:"python3 chall.py"
