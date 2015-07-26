from setuptools.command.install import install
from setuptools import setup, find_packages
import codecs
import sys
import os


def read(*parts):
    # intentionally *not* adding an encoding option to open
    # see here: https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts), 'r').read()

setup(name="patrol",
      version="0.3.1",
      description="Trigger custom commands from filesystem events.",
      long_description=read('README.rst'),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Topic :: Software Development :: Build Tools',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.1',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
      ],
      keywords='development environment tool pyuv epoll build',
      author='Colm O\'Connor',
      author_email='colm.oconnor.github@gmail.com',
      packages=find_packages(exclude=["tests/", ]),
      url='https://github.com/crdoconnor/patrol',
      license='MIT',
      install_requires=['pyuv', 'psutil', ],
      package_data={},
      zip_safe=False,)
