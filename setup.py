import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyaccessors",
    version="0.0.5",
    author="David Born",
    author_email="laggs0@gmail.com",
    description="Access lists of dictionaries with their keys' values",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hypostulate/pyaccessors",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)