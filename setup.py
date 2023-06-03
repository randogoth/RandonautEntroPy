import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="randonautentropy",
    version="1.0.2",
    author="randogoth",
    author_email="randogoth@posteo.org",
    description="Python API for interacting with The Randonautica Quantum Random Number Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/randogoth/randonautentropy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points= {
        'console_scripts': ['rndo=randonautentropy.cmd:main']
    },
    install_requires=['requests'],
    python_requires='>=3.6',
)