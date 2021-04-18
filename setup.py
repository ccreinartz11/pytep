import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytep",
    version="0.0.2",
    author="Christopher Reinartz, Thomas Enevoldsen",
    author_email="ccrein@elektro.dtu.dk",
    url="https://github.com/ChristopherReinartz/pytep.git",
    download_url="https://github.com/ChristopherReinartz/pytep/archive/refs/tags/v0.0.2.tar.gz",
    description="Tennessee Eastman simulator",
    long_description="README.rst",
    long_description_content_type="text/x-rst",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='==3.7.*',
    include_package_data=True,
    install_requires=[
	'dash>=1.20.0',
	'pandas>=1.2.3',
	'pytest>=6.2.3',
    ]
)

