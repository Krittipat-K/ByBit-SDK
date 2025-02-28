from setuptools import setup, find_packages

setup(
    name="ByBit-SDK",
    version="0.0.1",
    packages=find_packages(include=['bybit']),
    author='Krittipat Krittakom',
    install_requires=['python-dotenv'
                      'pycrypto==2.6.1',
                      ],
)