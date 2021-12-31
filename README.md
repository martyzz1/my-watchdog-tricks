watchdog-tricks
===============

This package includes several useful `Tricks` for `watchdog` (Python API for monitoring file system events, https://github.com/gorakhargosh/watchdog).

Tricks could be running in standalone mode or combined via a configuration file. They will perform specific tasks upon file change event.

- CheckBeforeAutoRestartTrick: Provided a check process exits successfully Restart a process on source code changes
- TouchFileTrick: Useful to chain together changes in alternative directories and then touch a file in a core directory

Configuration File - trick.yaml
-------------------------------
The true power of watchdog tricks is shown via configuration files, which could combine different tricks together and give you a fully automated development and building system.

Put the configuration file to the root directory that needs to be monitored. Assume the filename is `tricks.yaml`. To run watchdog with this configuration file

    $ watchmedo tricks tricks.yaml

API Documentation
-----------------
An example to restart celery when python source code changes in the main directory, or a parallel directory by using TouchFileTrick

    tricks:
    - watchdog_tricks.tricks.CheckBeforeAutoRestartTrick:
        patterns: ["*.py"]
        command: "celery -A config worker -l DEBUG -E"
		check_command: "./manage.py check"
        wait_for_process: true
    - watchdog_tricks.touchfile.TouchFileTrick:
        patterns: ["*.py"]
        touchfile: /app/manage.py
        source_directory: /var/libraries
    - watchdog_tricks.checkbeforeautorestart.CheckBeforeAutoRestartTrick:
        patterns: ["./requirements/base.txt", "./requirements/text.txt", "./requirements/local.txt"]
        command: ["/var/scripts_docker/django-refresh-requirements.sh"]
        touchfile: /app/manage.py
        check_command: ["echo", "'requirements changed'"]
        autostart: False

Installation
------------

Install directly from github.com

    $ pip install git+git://github.com/martyzz1/my-watchdog-tricks.git

Or clone this repository and run

	$ python setup.py install
