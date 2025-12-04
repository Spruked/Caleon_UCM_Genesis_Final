from setuptools import setup, find_packages
setup(
    name="skg-core",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["torch", "networkx", "torch-geometric", "flask"],
    entry_points={"console_scripts":["skg=skg.daemon:main"]},
    python_requires=">=3.9",
)