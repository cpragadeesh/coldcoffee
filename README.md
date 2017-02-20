# coldcoffee
# Online Judge for Debugging contest


## Table of Contents:


	1. Adding new problem
	2. Setting up Source file server
	3. Validator

## 1. Adding new problem

	
	1.1) Login to /admin with superuser account

	1.2) Goto problems panel

	1.3) Click on Add problem on the top right corner

	1.4) Add title, Problem content (HTML formatted).

	1.5) Leave nick & Problem_id blank

	1.6) Leave source file name, input file name blank (Default is <problem_nickname>_source.cpp, <problem_nickname>_input.txt respectively)

	1.7) Set source author to "server" for round 1 or the username of the author for round 2.

	1.8) Set validator field to the problem's validator's name.


## 2. Setting up Source/Input file server:


	2.1) Setup the apache/ngnix to serve files.
		2.1.1) All source files must be named <problem_nick_name>_source.cpp
	2.2) Login to /admin

	2.3) Update SourceURL & InputURL Model's url field to point to the apache source file server address.

## 3. Validator:

	3.1) Place validators inside validators in base directory.

	3.2) Validators are called this way: `./validator output.txt`

	3.3) Validators must return 0 in case of Correct answer, or a Positive integer denoting the case in which the solution failed.

	3.4) Validate solutions at /console.

	> NOTE: Validations are logged at validator_logs.txt in base directory.


## NOTES:
Unexpected outcomes might occur when adding news to the database due to stale cache. Hard reset by visiting /console while logged in as admin to resolve the issue.

All source files must be named (problem_nick_name)_source.cpp

All input files must be named (problem_nick_name)_input.txt