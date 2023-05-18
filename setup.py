from setuptools import find_packages, setup

# py -m build
# twine upload dist/*
VERSION = "0.1.0"
DESCRIPTION = "A tool to find the most common libraries used"
LONG_DESCRIPTION = """
A tool to find the most commonly imported
python libraries in a target directory 
"""

# Setup
setup(
    name="mcl-axis",
    version=VERSION,
    author="Axis (blankRiot96)",
    email="blankRiot96@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["click", "tabulate", "libcst"],
    python_requires=">=3.11",
    keywords=["cli", "most common libraries"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Intended Audience :: Developers",
    ],
    entry_points={"console_scripts": ["mcl=mcl:main"]},
)
