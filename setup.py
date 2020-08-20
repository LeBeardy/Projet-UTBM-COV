import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="UTBM-COV-PAPR", # Replace with your own username
    version="0.0.1",
    author="Paul-Antoine Pechmeja--Richard",
    author_email="paul-antoine.pechmejarichard@utbm.fr",
    description="Package about a project for UTBM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Paul-AntoinePechmeja-Richard/Projet-UTBM-COV",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
