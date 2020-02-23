# GMU Hillel Reports

[![Run on Repl.it](https://repl.it/badge/github/fiddler-analytics/gmu-hillel-reports)](https://repl.it/github/fiddler-analytics/gmu-hillel-reports)

This repo contains scripts for running the following process for GMU Hillel:

1. Pull contact information from HEART CRM
2. Check to see if that contact information has been entered in Little Green Light
3. Generate and save a report that shows any contacts that exist in HEART CRM, but not in Little Green Light.

The script works by iterating through the contacts in HEART CRM and checking whether the first name/last name combo, email address, and phone number exists in LGL. If any of that information is missing, the contact is adding to the report, with a description of what information is missing. The script is not currently set up to check if an email/phone number is added to the wrong contact. If either piece of information appears anywhere in LGL, LGL is considered up-to-date with respect to that information.

## Installing and Running Locally

To install and run the script, run the following commands from the terminal

```
git clone https://github.com/fiddler-analytics/gmu-hillel-reports.git
cd gmu-hillel-reports && pip install requirements.txt
python main.py
```

The script has only been tested for `python>=3.5`.
