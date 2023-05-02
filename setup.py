import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymx2",
    version="0.1.3",
    author="Vincent Paeder",
    author_email="python@paeder.fi",
    description="A Python driver to communicate with an Omron MX2 inverter through Modbus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['omron', 'mx2', 'inverter'],
    url="https://github.com/vpaeder/pymx2",
    project_urls={
        "Bug Tracker": "https://github.com/vpaeder/pymx2/issues",
    },
    packages=setuptools.find_packages(),
    install_requires=['pyserial'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Communications",
        "Topic :: System :: Hardware :: Hardware Drivers"
    ],
    python_requires='>=3.9',
)
