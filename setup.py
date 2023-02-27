from setuptools import setup

def _get_description(filename):
    with open(filename, encoding='utf-8') as file:
        return file.read()

def _requires_from_file(filename):
    with open(filename, encoding="utf-8") as file:
        return file.read().splitlines()

_pkg_name = "notion_kit"
_version = "1.0.2" # Change 1.0.1 => 1.0.2
_packages=["notion_kit"]
_install_requires=_requires_from_file("requirements.txt"),
_author = "Jieqiang Zhang"
_author_email = "bluewhite2389@gmail.com"
_description = "For easy use notion-sdk-py"
_long_description = _get_description("README.md")
_long_description_content_type = "text/markdown"
_url = "https://github.com/bluewhitep/Notion_kit"
_classifiers = [
    "Programming Language :: Python :: 3.10",
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: MIT License",
]
_python_requires=">=3.10, <4"

setup(
    name=_pkg_name,
    version=_version,
    packages=_packages,
    install_requires=_install_requires,
    author=_author,
    author_email=_author_email,
    description=_description,
    license='MIT',
    long_description=_long_description,
    long_description_content_type=_long_description_content_type,
    url=_url,
    classifiers=_classifiers,
    python_requires=_python_requires,
)
