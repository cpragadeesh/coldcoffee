# coldcoffee
## Webapp for Debugging contests
## Platform for Anokha 2017

## Table of Contents:

	0. Hosting the server
	1. Adding new problem
	2. Creating New Contest
	3. Setting up Source file server
	4. Validator

## 0. Hosting the server

	0.1) Naviage to the project directory.

	0.2) Run: `python manage.py runserver 0.0.0.0:8080`


## 1. Adding new problem
	
	1.1) Login to /admin with superuser account

	1.2) Add problem by clicking '+' sign in "Problems" row.

	1.3) Add title, Problem content (HTML formatted).

	1.4) Leave nick & Problem_id blank (They are auto-generated).

	1.5) Upload Source, Input, Validator files.

	1.6) Set source author to "server" for round 1 or the appropriate contestant for round 2

	1.7) Choose a contest from the list(Ensure that you have created a contest first).

	1.9) Click Save.


## 2. Creating New Contest

	2.1) Login to /admin with superuser account.

	2.2) Add contest by clicking '+' sign in "Contests" row.

	2.3) Give a name for the contest.

	2.4) Set the starting time of the contest. 

	2.5) Set the ending time of  the contest.


## 3. Setting up Source/Input file server:


	3.1) Setup the apache/ngnix to serve files.

	3.2) Login to /admin

	3.3) Update SourceURL & InputURL Model's url field to point to the apache source file server address.


## 4. Validator:

	4.1) Upload validator in "validator" field of "Problems" model.

	4.2) Validators are called this way: `./validator input.txt output.txt`

	4.3) Validators must return 0 in case of Correct answer, or a positive integer denoting the case in which the solution failed.

	4.4) Validate solutions at /console.

	> NOTE: Validations are logged at validator_logs.txt in base directory.


## NOTES:
When adding new rows to models, Hard reset cache by hitting "Reset cache" link in /console while logged in as admin to get updated views.
