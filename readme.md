## SG code sharing site POC

This is a proof-of-concept code-sharing site for [Shotgun](http://shotgunsoftware.com) products including Shotgun Toolkit, the [shotgun-api3](https://github.com/shotgunsoftware/python_api) Python API, RV, the [shotgunEvents](https://github.com/shotgunsoftware/shotgunEvents) event trigger daemon, etc. It was started as part of the 2015 Shotgun | Autodesk hackathon.

## Requirements
A loose (yes, incomplete) list of the stack:

* Django 1.9
* Postgres 9.3
* Bootstrap 3.3.6
* jQuery 2.2.0

## Goal
Iterating on this to see if we can provide an easily maintainable solution that enables users to contribute code as well as discover code in a single catalog. Currently users have code scattered in various repos across Github and Bitbucket and there's no easy way to browse all of the projects out there that pertain to Shotgun products.

The site is currently a lightweight layer on top of Github repos. To contribute, users fork the [channel repo](https://github.com/kporangehat/shareshot_channel), add a small JSON snippet into the appropriate channel `.json` file and then submit it back in a pull request. 

Assuming the JSON is valid, the pull request will be merged and within minutes the project will be listed in the directory. 

## Status
This is still in a proof-of-concept state and isn't expected to be production ready. 