# Reference
#   https://github.com/navdeep-G/setup.py/blob/master/setup.py

import io, os,sys
from shutil import rmtree
from setuptools import setup, Command, find_packages

# Support Function
def _requires_from_file(filename):
    with open(filename, encoding="utf-8") as file:
        return file.read().splitlines()

# Package meta-data
########## Edit this ##########
NAME = 'notion_kit'
DESCRIPTION = 'For easy use notion-sdk-py.'
URL = 'https://github.com/bluewhitep/Notion_kit'
AUTHOR = 'Jieqiang Zhang'
EMAIL = 'bluewhite2389@gmail.com'
VERSION = '1.1.1'
REQUIRES_PYTHON = '>=3.10, <4'

#-------[Extend: shouldn't have to touch too much]-------#
INSTALL_REQUIRES = _requires_from_file("requirements.txt")

here = os.path.abspath(os.path.dirname(__name__))

# Long description
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        LONG_DESCRIPTION = '\n' + f.read()
except FileNotFoundError:
    LONG_DESCRIPTION = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION

# setup.py upload
class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = [
				#('Option long name=', 'Option short name', 'Option describe'),
				('without-pypi', None, '(Bool)upload without PyPI'),    # Type:(Bool), Default: False
				('without-git', None, '(Bool)upload without git'),      # Type:(Bool), Default: False 
		]

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def bool_option_str_to_bool(bool_option):
        if (bool_option == 'True' or
                bool_option == 1 or
                bool_option == '1' or
                bool_option == True):
            return True
        elif (bool_option == 'False' or
                bool_option == 0 or
                bool_option == '0' or
                bool_option == False):
            return False
        else:
            return bool_option
            
    def initialize_options(self):
        self.without_pypi = False
        self.without_git = False
        
        pass

    def finalize_options(self):
        self.without_pypi = self.bool_option_str_to_bool(self.without_pypi)
        if type(self.without_pypi) != bool:
            raise Exception("upload --without_pypi is bool type.")
        
        self.without_git = self.bool_option_str_to_bool(self.without_git)
        if type(self.without_git) != bool:
            raise Exception("upload --without_git is bool type.")
        
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass
				
        if not self.without_pypi:
            # Building and Uploading to PyPI
            self.status('Building Source and Wheel (universal) distribution…')
            os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

            self.status('Uploading the package to PyPI via Twine…')
            os.system('twine upload dist/*')

        if not self.without_git:
            # Pushing in github(with tag)
            self.status('Pushing git tags…')
            os.system('git tag v{0}'.format(about['__version__']))
            os.system('git push --tags')
            
        sys.exit()

# Where the magic happens:
setup(
	name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    # If your package is a single module, use this instead of 'packages':
    # py_modules = ["test"],

    # If the package is cli tool: $ mycli
    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifier
        "Programming Language :: Python :: 3.10",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
    ],
    # $ setup.py upload
    cmdclass={
        'upload': UploadCommand,
    },
)