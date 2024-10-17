import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = "0.1.0"
PACKAGE_NAME = "pyberdata"
AUTHOR = "Hanjo Odendaal"
AUTHOR_EMAIL = "hanjo@sun.ac.za"
URL = "https://github.com/Bureau-for-Economic-Research/pyberdata"

LICENSE = "MIT"
DESCRIPTION = "Python BER DataPlayground API Python Package"
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
    "setuptools",
    "polars",
    "pytest",
    "requests",
    "logger",
    "python-decouple==3.8",
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    license=LICENSE,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
)
