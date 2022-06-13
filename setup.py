from setuptools import setup, find_packages

setup(
    name='ngeht-util',
    version='0.14.0',    
    description='Utilities for performing calculations with ngEHT',
    url='https://github.com/shuds13/pyexample',
    author='Aaron Oppenheimer',
    author_email='aaron.oppenheimer@cfa.harvard.edu',
    license='BSD 2-clause',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['pandas',
                      'openpyxl',
                      'pillow',
                      'ehtim',
                      'jupyter-console',
                      'requests'                     
                      ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
)
