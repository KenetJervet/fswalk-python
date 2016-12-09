import sys
from setuptools import setup, find_packages

if sys.version_info[0] == 2:
    additional_install_requires = [
        "enum34"
    ]
elif sys.version_info[0] == 3:
    additional_install_requires = [
    ]

setup(
    name="fswalk-python",
    version="0.0.1a1",
    description="A file system utility which provides various algorithms in traversing directories, etc",
    author="Yukio Usuzumi",
    author_email="anohigisavay@gmail.com",
    url="https://github.com/KenetJervet/fswalk-python",
    license="BSD 3-Clause License",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='',
    packages=[
    ],
    install_requires=[
        "six",
        "memoized_property"
        "regex"
    ] + additional_install_requires
)
