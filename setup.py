
import os
import setuptools

requires = [
]

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'gitdata', '__version__.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='gitdata-cli',
    version=about['__version__'],
    author="DSI Labs",
    author_email="support@gitdata.com",
    description="Data extraction and analysis tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitdata/gitdata",
    packages=[
        'gitdata',
        'gitdata.cli',
    ],
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'gitdata = gitdata.cli:main'
        ]
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Database :: Front-Ends',
   ],
   package_data={
       'gitdata': ['sql/*.sql'],
   }
)