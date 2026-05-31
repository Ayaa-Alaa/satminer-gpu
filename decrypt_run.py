#!/usr/bin/env python3
"""Decrypt wrapper - decrypts PRIVATE_KEY at runtime from ENCRYPTED_PK + FERNET_KEY env vars."""
import os, sys, subprocess

def main():
    encrypted_pk = os.environ.get("ENCRYPTED_PK")
    fernet_key = os.environ.get("FERNET_KEY")
    
    if not encrypted_pk or not fernet_key:
        print("[ERROR] ENCRYPTED_PK or FERNET_KEY env var missing", flush=True)
        sys.exit(1)
    
    try:
        from cryptography.fernet import Fernet
        f = Fernet(fernet_key.encode())
        private_key = f.decrypt(encrypted_pk.encode()).decode()
        os.environ["PRIVATE_KEY"] = private_key
        print("[OK] Private key decrypted successfully", flush=True)
    except Exception as e:
        print(f"[ERROR] Decryption failed: {e}", flush=True)
        sys.exit(1)
    
    # Run the miner
    os.execvp("python3", ["python3", "/app/gpu_miner.py"])

if __name__ == "__main__":
    main()
