from setuptools import setup, find_packages

INSTALL_REQUIRES = [
    "coverage==5.5",
    "coveralls",
    "networkx",
    "nose",
    "numpy",
    "pandas",
    "pickle5",
    "python-libsbml",
    "pyyaml",
    "requests"
    ]

def doSetup(install_requires):
  setup(
      name='SBMate',
      version='1.1.2',
      author='Woosub Shin',
      author_email='woosubs@umich.edu',
      packages=find_packages(exclude=['tests', 'notebooks']),
      url='https://github.com/woosubs/SBMate',
      description='Annotation quality metrics calculator (coverage, consistency, specificity).',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      package_dir={'SBMate': 'SBMate'},
      install_requires=install_requires,
      include_package_data=True,
      data_files=[('knowledge_resources', 
                   ['knowledge_resources/chebi_graph.gpickle',
                    'knowledge_resources/go_graph.gpickle',
                    'knowledge_resources/sbo_graph.gpickle'
                   ])],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',      # Define that your audience are developers
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'License :: OSI Approved :: MIT License',   # Again, pick a license
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
        ],
      )

if __name__ == '__main__':
  doSetup(INSTALL_REQUIRES)
