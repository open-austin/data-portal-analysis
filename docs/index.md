## About

Open Austin's Data Portal Analyzer gathers metadata about resources that are available from ```data.austintexas.gov``` and creates a report in CSV format. 

## Quick Start Guide

#### Installation and Use

Run the following commands from a terminal:

    git clone https://github.com/open-austin/data-portal-analysis.git
    cd data-portal-analysis

Optional steps: 
* If you will be usng virtualenv, create an environment and activate it before continuing.
* To run the most recent stable release, see the note about branches below.

This command will install dependencies:

	pip install -r requirements.txt

After pip is finished, run the test suite with:
	
	nosetests -v

Finally, use the folowing command to run the analyzer in online mode; you can replace ```results.csv``` with a filename of your choice:

    ./PortalAnalyzer.py results.csv

Note: ```PortalAnalyzer.py``` also creates a file called ```portal_analyzer.log``` that can be used for troubleshooting. Passing either ```-v``` or ```--verbose``` on the command line will result in a more detailed logfile. Use ```--help``` for a complete list of options.

##### Regarding branches

The ```master``` branch always contains stable code that passes the same tests as the most recent release, but it may have patches that were not included in that release. The default branch, ```develop```, contains code that is still being tested and should not be used "in production."

The following command can be used to track and checkout ```master```:

    git checkout -b master origin/master

To switch back to the development branch, use ```git checkout develop```.


