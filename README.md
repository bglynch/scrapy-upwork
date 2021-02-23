# scrapy-upwork



## About

This is a single spider scrapy project.

Given a username, password and secret answer, this spider will log in to upwark.com and scrape data from the /find-jobs/ page.

This spider handles the zero resistance login flow as well as handling **reCAPTCHA** and a **secret answer** pages. The secret answer page bypass is automated, while the reCAPTCHA page requires user input to bypass. To do this, if a reCAPTCHA page appears the spider is paused. Once the user completes the reCAPTCHA, a user must click enter inside the terminal to continue the spider.

If the spider stalls on a page, errors are handled using selenium timeouts. If selenium raises a timeout error, a screenshot will be taken of the page and the html will be downloaded. These will be saved to the **scrapy-upwork/output/errors/** directory to be used for debugging.



To see notes on the approach to building this spider view  [doc/approach.md](doc/approach.md)



### Stack

- Python 3.9
- scrapy
- selenium
- pydantic
- pycountry



### Running locally

##### terminal

```bash
git clone https://github.com/bglynch/scrapy-upwork.git
cd scrapy-upwork/

# create virtual env and install dependencies
virtualenv -p python3.9 venv
source venv/bin/activate
pip install -r requirements.txt

# rename secret file
mv argyle_challenge/secret.sample.py argyle_challenge/secret.py
```



Modify credential in secret.py to your login credentials.

##### scrapy-upwork/argyle_challenge/secret.py

```python
username = 'your-username'
password = 'your-username'
secret_answer = 'your-username'
```



Run the spider. 

##### terminal

```bash
cd argyle_challenge/
scrapy crawl upwork
```



After running, if successful, data is exported to **scrapy-upwork/output/data/jobs.json**

