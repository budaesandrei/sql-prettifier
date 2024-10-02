from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='sql-prettifier',
    version='1.0.0',
    author='Andrei Budaes-Tanaru',
    author_email='budaesandrei@gmail.com',
    description='A SQL prettifier / formatter library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        'sqlparse==0.5.1',
    ],
)