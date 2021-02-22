

# Scanning Task



## Description

#### Task: 

- Log into **upwork.com**  
- Scan the information from the site and return structured data

```
Username:      ***
Password:      ***
Secret answer: ***
Portal link:   https://www.upwork.com/ab/account-security/login
```



#### Detailed Task

###### Level 01

- Log into the portal using credentials

- scan the main portal page and return the information which you think is valuable

- Save the result to a file in a **json format**

- ```json
  {
    "name": "<scraped_name>",
    "surname":"<scraped_surname>",
    ....
  }
  ```

  

###### Level 02

- Get information from profile settings as per https://argyle.com/docs/api-reference/profiles
- Find an elegant way to handle missing fields and communicate it via response
- Make data serializable to an object (example using https://pydantic-docs.helpmanual.io/)

###### Level 03

- Handle possible errors
- Retry if the scanning fails

###### Nice to haves..

- Docker image implementation
- performance improvements
- lint
- mypy checks
- dependency management



## Stack

python, scrapy, selenium



## Login

Will use selenium to get passed the login page

Start url: https://www.upwork.com/ab/account-security/login

#### Username Page

![image-20210217123441351](/Users/br20069521/Library/Application Support/typora-user-images/image-20210217123441351.png)

##### username input

```html
<input data-v-9baadd78="" data-v-17f0650e="" id="login_username" name="login[username]" placeholder="Username or Email" aria-label="Username or email" inputmode="username email" autocomplete="username" type="text" class="up-input">
```

##### continue button

```html
<button data-v-0c7bde74="" data-v-733406b2="" id="login_password_continue" button-role="continue" type="button" class="up-btn mr-0 full-width mb-0 up-btn-primary" data-v-44072c38="">Continue</button>
```



#### Password Page

![Screenshot 2021-02-17 at 12.42.44](/Users/br20069521/Desktop/Screenshot 2021-02-17 at 12.42.44.png)

##### password input

```html
<input data-v-9baadd78="" data-v-17f0650e="" id="login_password" name="login[password]" placeholder="Password" aria-label="Password" autocomplete="current-password" type="password" class="up-input">
```

##### log in button

```html
<button data-v-0c7bde74="" data-v-58ebcdf7="" id="login_control_continue" button-role="continue" type="button" class="up-btn mr-0 width-sm mb-0 up-btn-primary" data-v-44072c38="">Log in</button>
```



#### Security Question Page







##### python

```python
from selenium import webdriver

driver = webdriver.Chrome('./chromedriver')
driver.get('http://upwork.com')
# username page
driver.find_element_by_xpath('//*[@id="login_username"]').click()
driver.find_element_by_xpath('//*[@id="login_username"]').send_keys('bobsuperworker')
driver.find_element_by_xpath('//*[@id="login_password_continue"]').click()
# password page
driver.find_element_by_xpath('//*[@id="login_password"]').click()
driver.find_element_by_xpath('//*[@id="login_password"]').send_keys('Argyleawesome123!')
driver.find_element_by_xpath('//*[@id="login_control_continue"]').click()
# secret answer page


driver = webdriver.Chrome('./chromedriver')
driver.get('https://www.upwork.com/ab/account-security/login')
driver.find_element_by_xpath('//*[@id="login_username"]').send_keys('bobsuperworker')
driver.find_element_by_xpath('//*[@id="login_username"]').send_keys(Keys.TAB)
driver.find_element_by_xpath('//*[@id="login_username"]').send_keys(Keys.ENTER)
driver.find_element_by_xpath('//*[@id="login_password"]').send_keys('Argyleawesome123!')
driver.find_element_by_xpath('//*[@id="login_control_continue"]').click()


```





## After Login

After login user  is redirected to https://www.upwork.com/ab/find-work/domestic

![Screenshot 2021-02-18 at 14.55.40](/Users/br20069521/Desktop/Screenshot 2021-02-18 at 14.55.40.png)

Looking at XHR request in chrome dev tools can see there is a GET reqest to upworks API

- https://www.upwork.com/ab/find-work/api/feeds/search?user_location_match=1

This returns the following JSON

![Screenshot 2021-02-18 at 14.41.18](/Users/br20069521/Desktop/Screenshot 2021-02-18 at 14.41.18.png)

Points of interest

- paging 

  - gives us pagination info

    ```json
    "paging": {
      "total": 53,
      "offset": 0,
      "count": 10,
      "resultSetTs": 1613617811311
    }
    ```

    

- results

  - gives info about each list item on the page

  - sample item:

  - ```json
    {
    "title": "Design a Microsoft Excel report system",
    "createdOn": "2021-02-18T03:10:11+00:00",
    "type": 1,
    "ciphertext": "~01f4053f6d37b4f9f2",
    "description": "Design a Microsoft report system given sample report.  One time job",
    "category2": null,
    "subcategory2": null,
    "skills": [],
    "duration": null,
    "shortDuration": null,
    "durationLabel": null,
    "engagement": null,
    "shortEngagement": null,
    "amount": {
        "currencyCode": "USD",
        "amount": 500
    },
    "recno": 222881809,
    "uid": "1362237947263033344",
    "client": {
        "paymentVerificationStatus": null,
        "location": {
          "country": "United States"
        },
        "totalSpent": 0,
        "totalReviews": 0,
        "totalFeedback": 0,
        "companyRid": 0,
        "companyName": null,
        "edcUserId": 0,
        "lastContractPlatform": null,
        "lastContractRid": 0,
        "lastContractTitle": null,
        "feedbackText": "No feedback yet",
        "companyOrgUid": "1257257427128717312",
        "hasFinancialPrivacy": false
    },
    "freelancersToHire": 0,
    "relevanceEncoded": "{\u0022position\u0022:\u00220\u0022}",
    "enterpriseJob": false,
    "tierText": "Intermediate",
    "tier": "Intermediate",
    "tierLabel": "Experience Level",
    "isSaved": null,
    "feedback": "",
    "proposalsTier": "5 to 10",
    "isApplied": false,
    "sticky": false,
    "stickyLabel": "",
    "jobTs": "1613617811311",
    "prefFreelancerLocationMandatory": true,
    "prefFreelancerLocation": ["United States"],
    "premium": false,
    "plusBadge": null,
    "publishedOn": "2021-02-18T03:10:11+00:00",
    "renewedOn": null,
    "sandsService": null,
    "sandsSpec": null,
    "sandsAttrs": null,
    "occupation": null,
    "attrs": [
        {
        "parentSkillUid": null,
        "freeText": null,
        "skillType": 3,
        "uid": "1031626758615973888",
        "highlighted": false,
        "prettyName": "Microsoft Excel"
        },
        {
        "parentSkillUid": null,
        "freeText": null,
        "skillType": 3,
        "uid": "1031626768082518016",
        "highlighted": false,
        "prettyName": "PDF Conversion"
        }
    ],
    "isLocal": false,
    "workType": null,
    "locations": [],
    "occupations": {
        "category": {
        "uid": "531770282580668419",
        "prefLabel": "IT \u0026 Networking"
        },
        "subcategories": [
            {
            "uid": "531770282589057033",
            "prefLabel": "Database Administration"
            }
        ],
        "oservice": {
            "uid": "1017484851352699011",
            "prefLabel": "Database Administration"
        }
    },
    "weeklyBudget": null,
    "hourlyBudgetText": null,
    "tags": [],
    "clientRelation": null
    }
    ```



### Job Details Page

After clicking on a list item, we are taken to a job details page.

![image-20210218150805440](/Users/br20069521/Library/Application Support/typora-user-images/image-20210218150805440.png)





### Performance - reducing requests to upwork server

As most of the information here is available from the <u>list view API</u> we may not need to scrape each profile page.

This would greatly reduce the number of request needed.

54 items across 6 pages:

- list and item view: 60 requests
- list view only: 6 requests ( **90% reduction** )



Looking further into the API, we can see the next page url is:

- https://www.upwork.com/ab/find-work/api/feeds/search?max_result_set_ts=1613666702146&paging=10;10&user_location_match=1

- after testing the url in postman we can decide the number of items per page by changing the **10** before the ''**&**'' sign
- as we have the pagination info from the initial request we can get all the items with 2 requests
  - 1st: to get paginaton info with number of items (e.g. 53)
  - 2nd: https://www.upwork.com/ab/find-work/api/feeds/search?paging=0;53&user_location_match=1



#### Data Model

```
uid: str
url: str
title: str
description:str
date_posted: str (ISO 8601)
country: str (ISO 3166-1 alpha-2 format)
attributes: list[str]
project_type: str

project:
	duration
	engagement
	payment:
		type: str
		amount: str
	experience_level: str
	prefFreelancerLocationMandatory: bool
occupation:
	category
	subcategory
	service
client:
	location: str
	paymentVerificationStatus: bool
	rating: int
	reviews: float

```

