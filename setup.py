from setuptools import setup, find_packages

setup(
    name="mbqc_transpiler",
    version="0.1.0",
    author="Rex Fleur",
    author_email="r.fleur@student.tudelft.nl",
    description="A transpiler to convert gate-based quantum circuits to MBQC cluster state representations.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/quantum-mbqc-transpiler",  #TODO MAKE A GITLAB!
    packages=find_packages(),  # Automatically finds 'mbqc_transpiler/' and submodules
    install_requires=[
        "qiskit",
        "networkx",
        "matplotlib",
        "numpy",
        "quimb",
        "pennylane",
        "pytket",
        "cirq",
        "scipy",
        "tensorly",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", #TODO CHECK LICENSE
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Blind Quantum Machine Learning",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "mbqc-transpile=mbqc_transpiler.transpiler:main"
        ]
    },
)
