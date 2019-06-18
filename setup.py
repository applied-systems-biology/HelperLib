from setuptools import setup


setup(
    name='helper_lib',    
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
