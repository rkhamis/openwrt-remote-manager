
from setuptools import setup, find_packages

setup(name='openwrt-remote-manager',
      version='1.1',
      description='A Python module for remotely managing an OpenWRT instance',
      author='Amr Hassan',
      author_email='amr.hassan@gmail.com',
      url='https://github.com/Jumpscale/openwrt-remote-manager',
      packages=find_packages(),
      classifiers=[
          'Programming Language :: Python :: 2 :: Only',
      ]
      )