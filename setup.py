from distutils.core import setup

setup(
  name = 'wizardpy',
  packages = ['wizardpy'],
  version = '0.2',
  license = 'MIT',
  description = ('python to pythonic code converter,'\
                        ' get the most out of your code for an effecient performance'),   
  author = 'Diaa Abujaber',
  author_email = 'diaa1999abujaber@gmail.com',
  url = 'https://github.com/DiaaAj/wizardpy',
  download_url = 'https://github.com/DiaaAj/wizardpy/archive/0.01v.tar.gz',
  keywords = [
      'pythonic code', 'effecient python code',
      'python code optimizer', 'fast python code',
      'optimized code', 'cmd application',
      ],
  install_requires=[            # I get to this in a second
          'validators',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
