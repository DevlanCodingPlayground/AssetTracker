# [AssetTracker](https://github.com/DevlanCodingPlayground/AssetTracker)

An asset management system is a software application or set of tools that organizations use to track and manage their physical and digital assets. These assets can include things like equipment, vehicles, buildings, and computer hardware and software.

The main purpose of an asset management system is to provide a centralized location for storing and retrieving information about an organization's assets. This information can include details such as the asset's make and model, serial number, purchase date, and current location.

Asset management systems can also include features such as tracking maintenance schedules, monitoring asset usage and tracking depreciation. This information can be used to make informed decisions about when to replace or upgrade assets.

Open-source **AssetTracker** Crafted using Flask and a theme named  **[Datta Able](https://appseed.us/product/datta-able/flask/)** 


## ✨ Manual Build

> Download the code

```bash
$ git clone https://github.com/DevlanCodingPlayground/AssetTracker.git
$ cd AssetTracker
```

<br />

### 👉 Set Up for `Unix`, `MacOS`

> Install modules via `VENV`

```bash
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

<br />

> Set Up Flask Environment

```bash
$ export FLASK_APP=run.py
$ export FLASK_ENV=development
```

<br />

> Start the app

```bash
$ flask run
// OR
$ flask run --cert=adhoc # For HTTPS server
```

At this point, the app runs at `http://127.0.0.1:5000/`.

<br />

### 👉 Set Up for `Windows`

> Install modules via `VENV` (windows)

```
$ virtualenv env
$ .\env\Scripts\activate
$ pip install -r requirements.txt
```

<br />

> Set Up Flask Environment

```bash
$ # CMD
$ set FLASK_APP=run.py
$ set FLASK_ENV=development
$
$ # Powershell
$ $env:FLASK_APP = ".\run.py"
$ $env:FLASK_ENV = "development"
```

<br />

> Start the app

```bash
$ flask run
// OR
$ flask run --cert=adhoc # For HTTPS server
```

At this point, the app runs at `http://127.0.0.1:5000/`.

<br />

### 👉 Create Users

By default, the app redirects guest users to authenticate. In order to access the private pages, follow this set up:

- Start the app via `flask run`
- Access the `registration` page and create a new user:
  - `http://127.0.0.1:5000/register`
- Access the `sign in` page and authenticate
  - `http://127.0.0.1:5000/login`

<br />


