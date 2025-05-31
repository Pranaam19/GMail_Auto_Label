#!/usr/bin/env python3
"""
Simple script to update the .env file with the correct environment variable name.
"""

import os

def update_env_file():
    """Update the .env file with the correct environment variable name."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    
    # Define the environment variables
    env_vars = {
        'PLAM_API_KEY': 'AIzaSyAC22dCgCLVG6XQDb0BimkBe7MCGS_-95w'
    }
    
    # Write the environment variables to the .env file
    with open(env_path, 'w') as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
    
    print(f".env file updated at {env_path}")
    print("Environment variables set:")
    for key in env_vars:
        print(f"- {key}")

if __name__ == "__main__":
    update_env_file()
