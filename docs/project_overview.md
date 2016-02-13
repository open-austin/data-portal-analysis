## Components

The NetUtils module contains code that queries the Socrata API

The PortalUtils module contains code that analyzes views and tables.

The PortalAnalyzer script is the command line interface for the above modules, which queries Socrata and creates a CSV when run.

## Concepts

Views provide data about resources - the portal analyzer only deals with tabular data, so in our case views provide data about tables.

A table is Socrata resource that can be represented as a traditional (rows and columns) list of relations.

