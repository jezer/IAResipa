from setuptools import setup, find_packages
import datetime

# Get the current date and time for the wheel filename
now = datetime.datetime.now()
version = "0.1.0"  # Example version, update as needed
timestamp = now.strftime("%Y.%m.%d.%H.%M")

# Define the library name
library_name = "n8n_python_workflow"

setup(
    name=library_name,
    version=f"{version}_{timestamp}",
    packages=find_packages(include=["src"]),
    install_requires=[
        # Add your project dependencies here
    ],
    description="A library for processing and managing workflows in n8n.",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/n8n_python_workflow",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)