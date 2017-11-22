# wsb-catalog

## Overview

A project to make a web-hosted catalog of my William S. Burroughs collection using the latest and greatest shiny object tech, at least that which I can wrap my head around. A sandbox for figuring out how to build Web catalog resources, if you will. Ultimately this might lead to a framework for the easy creation of digital humanities linked data resources using Github as a platform. We shall see.

## Current status

A simple one-page catalog rendered from linked-data-ish data managed in a CSV file is up and running at [http://www.bradleypallen.org/wsb-catalog/](http://www.bradleypallen.org/wsb-catalog/). Basically, we have a bunch of Jupyter notebooks that I can run to massage the CSV data into a Markdown table configured to be served up using Github Pages in a minimalist fashion. I kinda like it.

## Roadmap

Early days here. Things will be in flux.

### System

* Build a python module out of the code in the notebook to support a single-button-press to go from CSV to Markdown.
* Rig up continuous integration so that changes to the CSV will trigger a rebuild of the Markdown file. I have an idea of how to do that using AWS Lambda and Github Webhooks...
* Generate linked data from the CSV in JSON-LD and deploy it to Github Pages.
* Add individual pages for each catalog item using the larger images. Once we have these, I'll print QR code stickers encoding the page URLs and place them on the items-in-hand.

### Data

* Fix the dc:publisher metadata for Schottlaender "C" type items.

## License
MIT.
