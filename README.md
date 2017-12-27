# wsb-catalog

![Travis CI Build Status](https://travis-ci.org/bradleypallen/wsb-catalog.svg?branch=master)

## Overview

A project to make a web-hosted catalog of my William S. Burroughs collection using the latest and greatest shiny object tech, at least that which I can wrap my head around. A sandbox for figuring out how to build Web catalog resources, if you will. Ultimately this might lead to a framework for the easy creation of digital humanities linked data resources using Github as a platform. We shall see.

## Current status

A simple one-page catalog rendered from linked-data-ish data managed in a CSV file is up and running at [http://www.bradleypallen.org/wsb-catalog/](http://www.bradleypallen.org/wsb-catalog/). Basically, we have a Python module that massages the CSV data into a Markdown table configured to be served up using Github Pages in a minimalist fashion. I kinda like it.

## Roadmap

Early days here. Things will be in flux.

### System

* Add individual pages for each catalog item incorporating the larger images and linked data embedded in JSON-LD format. 
* Generate QR codes with links to the page URLs, print them as stickers and place them on the items-in-hand.

### Data

* Mine the descriptions for improved dc:creator attributions.
* Figure out how to represent the relations implied by an association copy.
* Determine how to link dc:creator, dc:publisher into DBPedia.
* Investigate defining formal value spaces for dc:bibliographicCitation based on Schottlaender, Shoaf and M&M schemes.

## License
MIT.
