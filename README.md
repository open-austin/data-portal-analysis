NOTE: This is the sodashop branch. Sodashop is a web app plugin/extension to the data portal analysis project that will allow visitors to quickly see what's new on the portal.

Sodashop currently consists of a single website, but an API and twiter bots are in the works

# Data Portal Analysis

There's a lot of content on the City of Austin's open data portal. This project is about studying that content so we can make the portal better. 

## Status 

[![Build Status](https://travis-ci.org/open-austin/data-portal-analysis.svg?branch=develop)](https://travis-ci.org/open-austin/data-portal-analysis) 

We're currently developing the second release of the Portal Analyzer; previous releases can be found [on this page](https://github.com/open-austin/data-portal-analysis/releases).


## Current project goals

Write code that grabs specific pieces of information from Austin's public data portal and rearranges it into a format that's useful for analysis.

Next goals include automated publishing to the City's data portal, so everyone can access and analyze this data.


## Why we're doing this

There are many ways to explore data quality. Improving data quality is a job that's never done. 

_Current business needs/issues to explore include_:

Identifiers... How often are departments using unique identifiers for City assets? What is the nature of those identifiers? Where might we benefit from using common identifiers?

Redundancy... How often are departments publishing the same information within their datasets? Are there any departments publishing about the same topics who might want to collaborate?

Accessibility... Are we using multiple resources to publish the same information repeatedly for different time periods? (Not ideal for API consumers.) What column labels and descriptions don't match up with their values, and could perhaps use some tuning? How often are schemas changing? Are these changes good or bad for data consumers?

Table grain... How often are we publishing aggregate information (subtotals and totals) when we could be publishing atomic data? This one is huge!


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



#### Documentation

[![Documentation Status](https://readthedocs.org/projects/data-portal-analysis/badge/?version=latest)](http://data-portal-analysis.readthedocs.org/en/latest/?badge=latest)

## How to contribute

The easiest way for Python developers to contribute is by fixing problems detected by QuantifiedCode, because the "learn to fix" link provides guidelines for resolving each issue. Click on the badge below to get started.

[![Code Issues](https://www.quantifiedcode.com/api/v1/project/88253a7da12a4f85be52f5800d43dcc1/badge.svg)](https://www.quantifiedcode.com/app/project/88253a7da12a4f85be52f5800d43dcc1)

Developers can also help by creating enhancements and new features; visit [the project board on waffle.io](https://waffle.io/open-austin/data-portal-analysis) to get an overview of development status. 

[![Stories in Ready](https://badge.waffle.io/open-austin/data-portal-analysis.png?label=ready&title=Ready)](https://waffle.io/open-austin/data-portal-analysis)

If you'd like to contribute but you're not sure how to start, comment on the [meta-issue for the current release](https://github.com/open-austin/data-portal-analysis/issues/28) and one of the project maintainers will be happy to help. 


## Contributing terms

When you contribute to this project, you are sharing and/or creating content. Please do not contribute content unless you agree with the terms [here](https://github.com/open-austin/data-portal-analysis/blob/develop/CONTRIBUTING.md).


## Credits

Coming soon

## History

A detailed record of significant changes can be found in [the changelog](https://github.com/open-austin/data-portal-analysis/blob/develop/CHANGELOG.md)

## License

[Unlicense](https://github.com/open-austin/data-portal-analysis/blob/develop/LICENSE.md)
