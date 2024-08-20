import os
from dotenv import load_dotenv

def print_env_vars():
    print("Before loading .env file:")
    for key, value in os.environ.items():
        print(f"{key}: {value}")

    print("\nLoading .env file...")
    load_dotenv()

    print("\nAfter loading .env file:")
    for key, value in os.environ.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    print_env_vars()