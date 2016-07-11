#!/usr/bin/env python
"""
sphinx-markdown

Author: Alpha <alpha@alphaservcomputing.solutions>

"""

from setuptools import setup

setup(
    name='sphinx-markdown',
    version='1.0.0',
    description='Sphinx extension to support Markdown files',
    url='https://github.com/Alphadelta14/sphinx-markdown',
    author='Alphadelta14',
    author_email='alpha@alphaservcomputing.solutions',
    license='MIT',
    install_requires=[
        'Markdown',
        'sphinx'
    ],
    packages=['sphinx_markdown', 'sphinx_markdown.extensions'],
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Plugins',
                 'License :: OSI Approved :: MIT License',
                 'Topic :: Documentation',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3'],
    keywords='sphinx markdown',
)
