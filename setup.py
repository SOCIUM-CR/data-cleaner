from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="data-sanitizer",
    version="0.1.0",
    author="Franco Micalizzi",
    author_email="franco@example.com",
    description="Aplicación de anonimización reversible de datos sensibles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/francomicalizzi/data-sanitizer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Security :: Cryptography",
        "Topic :: Text Processing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "data-sanitizer=src.main:main",
        ],
    },
    package_data={
        "": ["*.md", "*.txt", "*.json"],
    },
    include_package_data=True,
)