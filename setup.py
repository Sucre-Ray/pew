import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="pew",
    version="0.0.4",
    author="Valerii Vorobiov",
    tests_require=['pytest'],
    author_email="author@example.com",
    description="project for book places in coworking.",
    long_description=long_description,
    # install_requires=packages,
    long_description_content_type="text/markdown",
    url="https://github.com/Sucre-Ray/pew",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
