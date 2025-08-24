from setuptools import setup, find_packages

setup(
    name='resipaia',
    version='1.0.0',
    packages=find_packages(),
    package_dir={'': '.'},
    install_requires=[
        'supabase',
        'python-dotenv',
        'requests',
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='A library for IAResipa project',
    long_description=open('../README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jezerportilho/IAResipa',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)