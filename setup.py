from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in scienceoffice/__init__.py
from scienceoffice import __version__ as version

setup(
	name="scienceoffice",
	version=version,
	description="Research and development",
	author="Diamond pharma",
	author_email="dianmond@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
