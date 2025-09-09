from setuptools import setup, find_packages

setup(
    name="mcp-server",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "pydantic>=1.8.2",
        "PyYAML>=5.4.1",
        "google-generativeai>=0.1.0",
        "python-markdown>=3.3.4",
        "python-dotenv>=0.19.0",
        "databricks-connect>=7.3",
        "cryptography>=3.4.7",
        "python-jose[cryptography]>=3.3.0"
    ],
    package_data={
        'agente_roteador': [
            'config/*.yaml',
            'config/*.md',
            'config/schemas/*.json',
        ],
    },
    include_package_data=True,
    python_requires='>=3.8',
    author="Your Name",
    author_email="your.email@example.com",
    description="MCP Server - Model Context Protocol Server",
    long_description=open("README.md").read() if open("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mcpserver",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={
        'console_scripts': [
            'mcp-server=agente_roteador.main:main',
        ],
    },
)
