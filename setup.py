from setuptools import find_packages, setup

setup(
    name="reasonp",
    version="0.1.2",
    author="brendon.lin",
    author_email="brendon.lin@outlook.com",
    packages=find_packages(exclude=["tests"]),
    install_requires=["pandas>=1.1.0"],
    description="Data analysis tool for finding reasons for changes in data",
)
