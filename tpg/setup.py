from setuptools import setup, find_packages
import os

def readme():
#  with open(f'{os.getcwd()}\\README.md', 'r') as f:
    return ''#f.read()


setup(
  name='tpg',
  version='1.0.0',
  author='@HITHELL',
  author_email='hit<@HITHELL.com>',
  description="легкая библиотека для работы с псевдо графикой в терминале",
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/xHak2215/tpg',
  packages=find_packages(),
  install_requires=['keyboard>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='terminal_py_grafic.py',
  project_urls={
    'GitHub': 'https://github.com/xHak2215/tpg'
  },
  python_requires='>=3.6'
)
