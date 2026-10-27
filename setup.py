import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fiscal-transition-engine",
    version="1.1.4",
    author="Abhishek Singh",
    author_email="your.email@domain.com",
    description="Closed-loop adaptive control system for sovereign fiscal transitions and subsidy phase-outs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Abhishek1033ubuntu/fiscal-transition-engine",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Office/Business :: Financial",
    ],
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
    ],
)
