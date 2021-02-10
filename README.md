Convert Humanitarian 3W to IATI
===============================

This tool converts humanitarian 3W reports with appropriate HXL hashtags into bare-bones IATI XML.

# Installation

TODO

# Usage

TODO

# HXL hashtags

Attributes (starting with "+") may appear in any order within a hashtag spec. Additional attributes will be ignored (the ones shown are the minimum required). Column order is not significant.

## Required HXL hashtags

#org+impl

#sector+name

#activity

#adm1+name

#date+start

#date+end

## Optional HXL hashtags

#org+impl+type

#org+prog

#org+funder

#adm1+name

#adm2+name

#adm2+code

#targeted+total

#targeted+f+children

#targeted+m+children

#targeted+f+adults

#targeted+m+adults

#meta+id+x_iati

# Output format

TODO

# License

This tool was created by David Megginson for Development Initiatives, with funding from the Netherlands Ministry of Foreign Affairs. It is free to use and is released into the Public Domain (see UNLICENSE.md).
