"""
Setup file for the Compliance Framework
Based on Omnimathematics Framework with Penalty-Augmented Objectives
"""

from setuptools import setup, find_packages

setup(
    name="compliance-framework",
    version="1.0.0",
    author="MT Tech Industries LLC",
    author_email="research@mttechindustries.com",
    description="Mathematical Framework for AI Compliance and Truthfulness using Penalty-Augmented Objectives",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mttechindustries/compliance-framework",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0"
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8"
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=0.5"
        ]
    },
    keywords="ai, compliance, truthfulness, mathematics, optimization, framework",
    license="MIT License"
)