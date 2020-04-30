from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="seventh_client",
    packages=["seventh_client"],
    version="0.1",
    license="MIT",
    description="Strategy client for Seventh cryptocurrency trading engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Rushil Mallarapu",
    author_email="rushil.mallarapu@gmail.com",
    url="https://github.com/sudo-rushil/seventh-client",
    download_url="https://github.com/sudo-rushil/seventh-client/archive/v0.1.tar.gz",
    include_package_data=True,
    install_requires=["numpy", "Click"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points="""
        [console_scripts]
        seventh-cli=seventh_client:cli
    """,
)
