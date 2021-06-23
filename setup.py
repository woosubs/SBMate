from setuptools import setup, find_packages

INSTALL_REQUIRES = [
    "coverage"
    "coveralls"
    "networkx",
    "nose",
    "numpy",
    "pandas",
    "python-libsbml",
    "pyyaml",
    "requests"
    ]

def doSetup(install_requires):
  setup(
      name='SBMate',
      version='1.1.1',
      author='Woosub Shin',
      author_email='woosubs@umich.edu',
      packages=find_packages(exclude=['tests', 'notebooks']),
      scripts=[
          'SBMate/sbmate',
          'SBMate/sbmate.bat',
          ],
      url='https://github.com/woosubs/SBMate',
      description='Annotation quality metrics calculator (coverage, consistency, specificity).',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      package_dir={'SBMate': 'SBMate'},
      install_requires=install_requires,
      include_package_data=True,
      data_files=[('knowledge_resources', ['knowledge_resources/*.gpickle'])],
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