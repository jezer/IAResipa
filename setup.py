from setuptools import setup, find_packages

setup(
    name='resipa_lib',
    version='0.1.0',
    packages=find_packages(where='03.src'),
    package_dir={'': '03.src'},
    install_requires=[
        'supabase',
        'python-dotenv',
        'requests',
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='A library for IAResipa project',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/IAResipa',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)