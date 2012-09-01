Monitis Python SDK
=============================

The Monitis API SDK provides a simple Python interface to the Monitis 
RESTful API.  More information on the API is available at 
http://monitis.com/api/api.html

Example Usage
-----------------------------
To  run  the example,  export  the  environment variables  MONITIS_APIKEY  and
MONITIS_SECRETKEY. To get the necessary keys, sign up for a Monitis account at
https://www.monitis.com/free_signup.jsp

    from os import getloadavg
    from monitis.monitors.params import ResultParams, DataType
    from monitis.monitors.custom import CustomMonitor

    rp = ResultParams('1m','1 Min. Load Avg.','load', DataType('integer'))
    cm = CustomMonitor.add_monitor(rp, name='1 Min. Load', tag='load')
    load1m,load5m,load15m = getloadavg()
    print cm.add_result(results={'1m':load1m})

Running Tests
-----------------------------
To run the tests, you will need nose installed

        $ pip install nose

Some of the tests require environment variables to be set, for API
authentication.

        $ export MONITIS_APIKEY='your API key'
        $ export MONITIS_SECRETKEY='your secretkey'
        $ export MONITIS_USER='username@yourdomain.com'
        $ export MONITIS_PASS='monitis password'

Once that's done, simply run nosetests in the root of the project.

        $ nosetests

Monitis API
-----------------------------
The Monitis API is documented at <http://monitis.com/api/api.html>. The 
Python SDK currently covers the following components of the API.

### Included in Python SDK
- API calls with checksum validation
- Custom Monitors
- Users
- Subaccounts
- Layout
- Contacts

### Included in future implementation of SDK
- Auth token validation
- Custom monitor agents
- Notifications
- Predefined monitors
    - External
    - Internal
    - Transaction
    - Full page load
    - Visitor tracker
    - Cloud instances
