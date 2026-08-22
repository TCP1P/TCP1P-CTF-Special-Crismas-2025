#!/usr/bin/env python3
import subprocess
import re
import os
import sys

try:
    with open("flag.txt", "r") as f:
        FLAG = f.read().strip()
except FileNotFoundError:
    FLAG = "XMAS{TEST_FLAG}"

ANVIL_RPC = "http://127.0.0.1:8545"
ADMIN_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"

def deploy():
    cmd = f"forge create Setup.sol:Setup --rpc-url {ANVIL_RPC} --private-key {ADMIN_KEY} --value 100000000000000000000 --broadcast --json"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0: return None
    match = re.search(r'"deployedTo":\s*"(0x[a-fA-F0-9]{40})"', result.stdout)
    return match.group(1) if match else None

def solved(addr):
    cmd = f"cast call {addr} 'isSolved()(bool)' --rpc-url {ANVIL_RPC}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return "true" in result.stdout.lower()

def main():
    addr = deploy()
    if not addr:
        print("Deploy failed")
        sys.exit(1)

    print(f"RPC: gzcli.1pc.tf:8545")
    print(f"Setup: {addr}")

    try:
        input("")
    except:
        return

    if solved(addr):
        print(FLAG)
    else:
        print("Fail")

if __name__ == "__main__":
    main()
