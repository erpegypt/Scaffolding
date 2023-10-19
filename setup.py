from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in scaffolding/__init__.py
from scaffolding import __version__ as version

setup(
	name="scaffolding",
	version=version,
	description="scaffolding Rent and Sales Operation",
	author="Connect4systems",
	author_email="info@connect4systems.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
