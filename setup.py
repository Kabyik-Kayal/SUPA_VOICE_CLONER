"""Setup script for the Supa Voice Cloner package."""
from setuptools import setup, find_packages

def read_requirements():
    """Read requirements from requirements.txt, filtering out pip options."""
    with open("docker-requirements.txt") as f:
        requirements = []
        for line in f.read().splitlines():
            line = line.strip()
            # Skip empty lines, comments, and pip options
            if line and not line.startswith('#') and not line.startswith('--'):
                requirements.append(line)
        return requirements

setup(
    name="Supa Voice Cloner",
    version="0.1",
    author="Kabyik",
    packages=find_packages(),
    install_requires=read_requirements(),
)