from setuptools import setup, find_packages

setup(
    name="pdf_magic",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "PyQt5",
        "PyMuPDF",
        "Pillow",
        "pdf2docx",
    ],
    entry_points={
        "console_scripts": [
            "pdf_magic=pdf_magic.main:main",
        ],
    },
    author="Leon Gajtner",
    author_email="l.gajtner@gmail.com",
    description="A PDF processing application with GUI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/wac0ku/pdf_magic",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)