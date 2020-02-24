# GMU Hillel Reports

This repo contains scripts for running the following process for GMU Hillel:

1. Pull contact information from HEART CRM
2. Check to see if that contact information has been entered in Little Green Light
3. Generate and save a report that shows any contacts that exist in HEART CRM, but not in Little Green Light.

The script works by iterating through the contacts in HEART CRM and checking whether the first name/last name combo, email address, and phone number exists in LGL. If any of that information is missing, the contact is adding to the report, with a description of what information is missing. The script is not currently set up to check if an email/phone number is added to the wrong contact. If either piece of information appears anywhere in LGL, LGL is considered up-to-date with respect to that information.

## Installing and Running Locally

To install and run the script, run the following commands from the terminal

```
git clone https://github.com/fiddler-analytics/gmu-hillel-reports.git
cd gmu-hillel-reports && pip install -r requirements.txt
python main.py
```

The script has only been tested for `python>=3.5`.

## Running on Repl.it

[![Run on Repl.it](https://repl.it/badge/github/fiddler-analytics/gmu-hillel-reports)](https://repl.it/github/fiddler-analytics/gmu-hillel-reports)

You can also run the script on Repl.it, a service that allows you to run containerized code in your browser. To run the code on Repl.it, click the badge above. That will clone the repo in a Repl.it session. If you have't already, you may want to create an account on Repl.it. That will allow you to add a `.env` file to the repo to set environmental variables.

Once the repo clones, you can create a `.env` file to manager your secrets. This file can _only_ be seen on your copy of the Repl.it, and allows you to store credentials so you don't have to enter them each time. If you don't want to add a `.env` file, that's fine too. The script will prompt you for your credentials on each run. To generate a token for the Little Green Light API, follow the instructions in [their documentation](https://api.littlegreenlight.com/api-docs/static.html). Please contact the HEART administrator for the HEART Consumer Key and Consumer Secret.

![.evn file example](/img/add_secrets.png)


