from setuptools import setup, find_packages

setup(
    name="fiscal-transition-engine",
    version="1.0.0",
    description="A closed-loop non-linear adaptive control system for sovereign fiscal transition & subsidy phase-out.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Abhishek Singh",
    author_email="abhishek1033@gmail.com",
    url="https://github.com/Abhishek1033ubuntu/fiscal-transition-engine",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "matplotlib>=3.7.0",
    ],
)
