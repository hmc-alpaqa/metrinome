"""Handle publishing package to pip."""
from setuptools import setup  # type: ignore

with open("../../README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="metrinome",
    version="1.0.1",
    description="Compute code complexity metrics and generate CFGs for Python, \
                 C++, and Java easily.",
    keywords="cfg cyclomatic npath path apc code complexity",
    author="HMC Metrinome Team",
    author_email="lbang@hmc.edu",
    maintainer="Gabriel Bessler",
    maintainer_email="gbessler@hmc.edu",
    url="https://github.com/hmc-alpaqa/metrinome",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development",
        "Typing :: Typed"
    ]
)
