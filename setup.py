
from setuptools import setup, find_packages


setup(
    name="src",
    version="0.0.1",
    author="Manav664",
    description="DVC pipeline for the diamond vendor files transformation",
    long_description="",
    long_description_content_type="text",
    url="https://github.com/Manav664/MLOps-Demo.git",
    author_email="19bce062@nirmauni.ac.in",
    packages=["src"],
    python_requires=">=3.6",
    install_requires=[
        'pandas',
        'scikit-learn',
        'numpy'
    ]
)