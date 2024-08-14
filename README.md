# Assignment - 3 (Pub.Dev Dataset)
We will use python to scrap details about packages from https://pub.dev/packages?sort=like, The output will be 
* basic.csv
* detailed.csv

## What you Need
To run the main.py file, you will need `Python 3` and Chrome Browser with `version 104`. You can install all libraries by running `pip install -r requirements.txt`

## Scraping Packages
After executing main.py file you will get:
* basic.csv contains: `title`, `title_link`, `likes`, `pub_points`, `popularity`, `description`, `latest_version`,`latest_version_release_date`, `provided_license`
* detailed.csv contains: `title`,`title_link `, `sdk`, `platform`,`is_beta_version`, `documentation_link`, `verified_publisher`, `dependencies`, `github_link`

## How to Execute
* Git clone this repo.
* Import the modules required from the requirements.txt file.
* Open the constants.py file, and update the the constant CHROME_BINARY_LOCATION which represents chrome binary location.
* Run fire Command, `python main.py scrap_package True`, in command line (For force_download).
* Run fire command, `python main.py scrap_package`, in command line (otherwise).
* You will get output in new directory `/output`.
