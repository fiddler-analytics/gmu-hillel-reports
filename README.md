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

Once the repo clones, you can create a `.env` file to manage your secrets. This file can _only_ be seen on your copy of the Repl.it, and allows you to store credentials so you don't have to enter them each time. If you don't want to add a `.env` file, that's fine too. The script will prompt you for your credentials on each run. To generate a token for the Little Green Light API, follow the instructions in [their documentation](https://api.littlegreenlight.com/api-docs/static.html). Please contact the HEART administrator for the HEART Consumer Key and Consumer Secret.

![Add a file to the Repl.it](/img/add_file.PNG)

![.env file example](/img/add_secrets.png)

After you have your Repl.it set up, head on over to [https://salesforce.shirconnect.com/](https://salesforce.shirconnect.com/) to get an access code for HEART CRM. This allows you to authenticate with HEART CRM using OAUTH2. The consumer key that you need to enter into the text box is the same consumer key you received from the HEART administrator and placed in your `.env` file in the step above. Note, the example shows the domain for the HEART Sandbox. To connect to production, you'll want to use `https://hillelcommunity.force.com` instead.

![Retreive your access code from HEART](/img/get_access_code.png)

Once you've enter all of the information, hit `Authenticate`. If you're not logged in to HEART CRM, you'll be redirected to the HEART login page. Once you login, HEART will redirect you back to `https://salesforce.shirconnect.com/` and supply you with an access code. If you're already logged in, an access code will appear on the left hand side of the screen, as shown below. Note, you can only authenticate once with an access code, and acccess codes expire after fifteen minutes. To run the script a second time, you'll need to perform this step again and retrieve a new access code.

![Copy your access code to the clip board](/img/copy_access_code.PNG)

After you've obtained your access code, hit the big green `Run` button on the Repl.it page.

![Run the Repl.it](/img/run_repl.png)

The script should start running and you'll some terminal output on the right. It has to install the dependencies for the script, so don't worry if it takes a few minutes. Once it's done installing the dependencies, you'll see a prompt asking you for an access code. Enter the access code you receive from `https://salesforce.shirconnect.com`. The script will also ask you if you would like to authenticate to the Sandbox account. Enter `n` if you want to connect to prod.

![Enter your acccess code](/img/enter_access_code.png)

Once you enter your access code, the script should be off to the races. If you see an error, odds are your access code is expired. You should return to `https://salesforce.shirconnect.com` and retrieve a new one. Otherwise you should see output along the lines of:

```
Processing constituent 1/132
Processing constituent 2/132
Processing constituent 3/132
```

If you see that, then the script is successfully pulling data from LGL. This will take a few minutes to run, because the LGL API limits users to 300 calls over a five minute period. This means we need to spread out the REST calls to avoid exceeding the limit. The script takes a 1.5 second break in between each call to the LGL API.

After the script is done running, you'll see a file called `missing_contact_report_<date>.csv`. If you don't see the file, try refreshing Repl.it. Sadly, Repl.it does not currenlty support downloading individual files. To extract the CSV, double click on the output CSV file and and copy the contents in Notepad on your local machine. Once you save it, you'll be able to open the file using Excel. At that point, it's also safe to save it as a `.xlsx` file if that is your preference.

![Copy the CSV](/img/copy_csv_file.png)
