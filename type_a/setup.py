from setuptools import setup, find_packages

# Read in the requirements.txt, ignoring special options
with open('requirements.txt') as f:
    requirements = [line for line in f.read().splitlines() if not line.startswith('--')]

import subprocess
from datetime import datetime
from setuptools import setup

def get_git_commit_hash():
    try:
        # Get the abbreviated commit hash
        commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()
        return commit_hash
    except subprocess.CalledProcessError:
        # Return a default value or raise an error if Git is not available
        return "unknown"

def generate_version():
    # Major version
    major = 0

    # Minor version as YYYYMM
    now = datetime.now()
    minor = now.strftime("%Y%m")

    # Patch version as HHMMSS
    patch = now.strftime("%H%M%S")

    # Get the abbreviated commit hash
    commit_hash = get_git_commit_hash()

    # Combine to form the version string
    return f"{major}.{minor}.{patch}+{commit_hash}"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="singularity_type_a",
    version=generate_version(),
    author="Richard Lee",
    author_email="rlee@tokyo3.com",
    description="Singularity package for Richard's experimentation with ML and LLMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rl337/singularity",
    packages=find_packages(
        include=['singularity']
    ),
    test_suite='tests',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: Creative Commons Attribution License",
    ],
    python_requires='>=3.6',
    install_requires=requirements
)

