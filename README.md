

# Installation Guidelines
- (optional) Activate your virtualenv
- Install `Selenium`
    > pip install selenium
- Install `prettytable` and `browsermobproxy`
- Download the browsermobproxy executables from [here](https://bmp.lightbody.net/).
- Unzip the downloaded zip file *in this project's root*.
- Install `requests`.
## BrowserMob-Proxy Installation Steps


This project is done by following the Butkiewicz' Paper Characterizing Webpage Complexity (`butkiewicz2014.pdf`)
## Steps to Execute the Project
- `output.json` is the final file that has the information from the websites in the dataset. This includes website name, website category, rank, request code and request details (request url, request code, start time, MIME type, duration).
- `dataset.csv` is the dataset file we'll be using in our project. It contains only the rank and name of the most popular websites.
- `main.py` is the file we use to generate data from the dataset. Run it using `python main.py -c NUMBER` where NUMBER is the NUMBER of websites you want to collect data for. You'd need to have a folder named `$PROJECTROOT/har_data/` for the program to save the HAR files in. 
- `analyse.py` will parse through the `output.json` file to give a glimpse of the data collected.
- `glimpse.ipynb` is the Jupyter-Notebook file to run the Final Analysis

To execute the analysis file, simply run the `glimpse.ipynb` file. 
