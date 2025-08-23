from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hostex-python",
    version="1.0.0",
    author="Keith",
    author_email="keith@example.com",
    description="Python client library for the Hostex API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/hostex-python",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "python-dateutil>=2.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.812",
            "requests-mock>=1.8.0",
        ],
    },
    keywords="hostex api property management vacation rental",
    project_urls={
        "Documentation": "https://github.com/example/hostex-python/tree/main/docs",
        "Bug Reports": "https://github.com/example/hostex-python/issues",
        "Source": "https://github.com/example/hostex-python",
    },
)