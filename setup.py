from setuptools import setup


setup(
    name='helperlib',    
    version='2.0',                         
    url="https://github.com/applied-systems-biology/HelperLib",
    author="Anna Medyukhina",
    author_email='anna.medyukhina@gmail.com',
    packages=['helper_lib'],
    license='BSD-3-Clause',

    install_requires=[
        'scikit-image',
        'pandas',
        'numpy',
        'ddt'
      ],
 )
