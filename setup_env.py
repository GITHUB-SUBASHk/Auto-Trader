import subprocess
import sys

def install_package(pkg):
    """Install a Python package if not already installed"""
    try:
        __import__(pkg)
        print(f"{pkg} already installed")
    except ImportError:
        print(f"{pkg} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

def check_protoc():
    """Check if protobuf compiler is installed"""
    from shutil import which
    if which("protoc") is None:
        print("protoc not found. Installing protobuf-compiler...")
        subprocess.check_call(["apt-get", "update"])
        subprocess.check_call(["apt-get", "install", "-y", "protobuf-compiler"])
    else:
        print("protoc already installed")

def generate_upstox_proto():
    """Generate Python classes from MarketDataFeed.proto"""
    import os
    proto_file = "MarketDataFeed.proto"
    if os.path.exists(proto_file):
        print("Compiling Upstox proto file...")
        subprocess.check_call(["protoc", "--python_out=.", proto_file])
    else:
        print("MarketDataFeed.proto not found. Please place it in the project root.")

if __name__ == "__main__":
    # Python packages
    packages = ["protobuf", "websockets", "python-dotenv"]
    for pkg in packages:
        install_package(pkg)

    # Protobuf compiler
    check_protoc()
    generate_upstox_proto()

    print("Environment setup complete!")
