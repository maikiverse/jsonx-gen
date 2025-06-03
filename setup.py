from setuptools import setup, find_packages

setup(
    name="jsonx_gen",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "ijson>=3.2.3"
    ],
    extras_require={
        'web': [
            "fastapi>=0.68.0",
            "uvicorn>=0.15.0",
            "pydantic>=1.8.0",
        ],
    },
    entry_points={
        'console_scripts': [
            'jsonx_gen=jsonx_gen.cli:main',
        ],
    },
    author="Marc Scheu",
    author_email="marc@scheu.org",
    description="A tool to search JSON objects for keywords and generate extraction code",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/jsonxgen",
    project_urls={
        "Bug Tracker": "https://github.com/maikiverse/jsonx-gen/issues",
        "Documentation": "https://github.com/maikiverse/jsonx-gen#readme",
        "Source Code": "https://github.com/maikiverse/jsonx-gen",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Code Generators",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    package_data={
        'jsonx_gen': ['py.typed'],
    },
    keywords="json, code-generation, extraction, search, cli, web-interface",
) 