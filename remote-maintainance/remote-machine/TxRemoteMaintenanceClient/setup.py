import setuptools

try:
    with open("../README.md", "r") as fh:
        long_description = fh.read()
except FileNotFoundError:
    print("No Readme available")
    long_description = ""

setuptools.setup(
    name="TxRemoteMaintenance-paszin",
    version="0.0.1",
    author="Pascal Crenzin",
    author_email="pc@thullex.de",
    description="Remote Maintenance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/paszin/clothing-industry-diginal",
    packages=setuptools.find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            "tx-rema-client = RemoteMaintenanceClient.bin.txRemaClient:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
