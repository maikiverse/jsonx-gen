from setuptools import setup, find_packages

setup(
    name="jsonxgen",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "pydantic>=1.8.0"
    ],
    entry_points={
        'console_scripts': [
            'jsonxgen=src.cli:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to generate extraction code from JSON schemas",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/jsonxgen",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    package_data={
        'jsonxgen': ['py.typed'],
    },
) 