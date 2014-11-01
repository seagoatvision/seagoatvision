[![Build Status](https://travis-ci.org/seagoatvision/seagoatvision.svg?branch=develop)](https://travis-ci.org/seagoatvision/seagoatvision)
[![Stories in Ready](https://badge.waffle.io/seagoatvision/seagoatvision.png?label=ready&title=Ready)](http://waffle.io/seagoatvision/seagoatvision)
[![Stories in Progress](https://badge.waffle.io/seagoatvision/seagoatvision.png?label=In Progress&title=In Progress)](http://waffle.io/seagoatvision/seagoatvision)
[![Coverage Status](https://coveralls.io/repos/seagoatvision/seagoatvision/badge.png?branch=develop)](https://coveralls.io/r/seagoatvision/seagoatvision?branch=develop)

SeaGoatVision
=============

Description
-----------
SeaGoatVision is a computer vision system running into a server.

Actually, this platform is used to doing robotic.

Principal feature :

 - Manage multiple client and media
 - Run filterchain
 - Control filter by parameters
 - Give environment for debug and create filter
 - Run in local or in remote
 - Can send message to other platform
 - Execute Python and C++ filters

Installation
------------
Be sure to read the INSTALL.md file.

Operating instructions
----------------------
Read HOWTO.md file.

Test
----
Run all test:

	make test

Run a specific test, example with cli test:

	python2 -m nose2 tests.test_cli

To see coverage report

	coverage report -m

License
-------
Read LICENSE file.

Contact information
-------------------
Go on website https://github.com/seagoatvision/seagoatvision and create an issue.
Or send email to seagoatvision at gmail.com
Or by chat : [![Gitter](https://badges.gitter.im/Join Chat.svg)](https://gitter.im/seagoatvision/seagoatvision?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

Known bugs
----------
The bugs is showing in issues of the project : https://github.com/seagoatvision/seagoatvision/issues?labels=bug&page=1&state=open

Troubleshooting
---------------
The project is only supported in python 2.7, because OpenCV is not supported in python 3 at this moment.

Credits
-------
Thanks club Capra and club Sonia to support us.

 - http://capra.etsmtl.ca
 - http://sonia.etsmtl.ca

Release
-------
Read RELEASE file.

Statistic
---------
[Open Hub SeaGoatVision](https://www.openhub.net/p/SeaGoatVision)
