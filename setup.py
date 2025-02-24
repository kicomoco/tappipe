from setuptools import find_packages, setup

with open("Readme.md", "r") as f:
	long_description = f.read()

setup(
	name="tappipe",
	version="0.0.5",
	description="Tigo TAP->CCA RS485 Power Report Decoder",
	package_dir={"": "src"},
	packages=['tappipe'],
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/kicomoco/tap-pipe",
	author="Kicomoco",
	author_email="admin@kicomoco.com",
	license="GPLv3",
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Environment :: Console",
		"Programming Language :: Python :: 3.6",
		"Operating System :: OS Independent",
	],
	install_requires=[],
	extras_require={
		"dev": ["pytest>=7.0", "twine>=4.0.2"],
	},
	python_requires=">=3.6.9",
)