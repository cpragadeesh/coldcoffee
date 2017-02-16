# coldcoffee
Online Judge for Debugging contest


Table of Contents:


	1. Adding new problem
	2. Setting up Source file server


1. Adding new problem

	
	1.1) Login to /admin with superuser account
	1.2) Goto problems panel
	1.3) Click on Add problem on the top right corner
	1.4) Add title, Problem content with HTML formatting.
	1.5) Leave Problem_id blank
	1.6) Add source file name
	1.7) Leave Source author untouched. DO NOT MODIFY IT.


2. Setting up Source file server:


	2.1) Setup the apache/ngnix to serve files.
	2.2) Login to /admin
	2.3) Update SourceURL Model's url field to point to the apache source file server address.



NOTE: Problems may occur due to stale cache. In that case hard reset all caches by visiting /cachereset while logged in as admin