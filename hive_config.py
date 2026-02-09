# File: shield_hive/hive_config.py
import secrets

# This generates a secure, random 64-character hex key
# In production, you would generate this once and keep it safe.
# For now, we will use a fixed key for your setup so the Agent can match it.
SERVER_API_KEY = "8f4b2e1c9d3a5b7e6f8c1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d"

def generate_new_key():
    return secrets.token_hex(32)