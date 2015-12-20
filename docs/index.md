## About

Open Austin's Data Portal Analyzer gathers metadata about resources that are available from ```data.austintexas.gov``` and creates a report in CSV format. 

## Quick Start Guide

First, clone the git repository and ```cd``` to the projects root directory.

Next, install dependencies with the command ```pip install -r requirements.txt```.

After pip is done, use the command ```nosetests -v``` to ensure that the program is working correctly.

When the tests pass, you can connect to the Socrata API and start building a report by running ```./PortalAnalyzer.py output.csv```; a list of options can be obtained with the command ```./PortalAnalyzer.py --help```.

