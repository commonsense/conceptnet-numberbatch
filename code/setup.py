from setuptools import setup

setup(
    name = 'conceptnet_retrofitting',
    version = '0.1.1',
    install_requires=[
        'pandas', 'ftfy>=4.0', 'numpy', 'scikit-learn', 'wordfreq >= 1.1'
    ]
)
