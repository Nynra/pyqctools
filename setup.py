from setuptools import setup

setup(
    name="pyqctools",
    version="0.0.1a",
    author="Nynra",
    description="A containing some tools for quantum computing using python.",
    py_modules=["pyqctools"],
    package_dir={"": "src"},
    install_requires=[list(map(str.strip, open("requirements.txt").readlines()))],
)