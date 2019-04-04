from setuptools import setup


setup(
    name='helperlib',    # This is the name of your PyPI-package.
    version='1.0',                          # python versioneer
    url="https://github.com/applied-systems-biology/HelperLib",
    author="Anna Medyukhina",
    packages=['helper_lib'],
    author_email='anna.medyukhina@gmail.com',
    license='BSD-3-Clause',

    install_requires=[
        'scikit-image',
        'pandas',
        'numpy',
        'ddt'
      ],
 )
