import setuptools

setuptools.setup(
    name="my-watchdog-tricks",
    version="1.0.9",
    license="MIT",
    author="Martin Moss",
    author_email="martyzz1@github.com",
    url="https://github.com/martyzz1/my-watchdog-tricks",
    description="Some tricks for watchdog (Python file system monitoring tool), including CheckBeforeAutoRestart",
    long_description=open("README.md").read(),
    keywords=["watchdog", "watcher", "tricks"],
    classifiers=[
        "Environment :: Console",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Environment :: Other Environment",
        "Topic :: Utilities",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Filesystems",
    ],
    install_requires=[
        "watchdog[watchmedo]==1.0.2",
    ],
    packages=["my_watchdog_tricks"],
)
