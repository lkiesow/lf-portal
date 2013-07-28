=========
LF-Portal
=========

A video portal for Opencast Matterhorn and compatible systems.

This web application provides a simple video portal for Opencast Matterhorn and
Lernfunk systems. It supports authentication against a Matterhorn system so
that users can access internal or protected videos. Users can search for
recordings and series. And, of cause, users can view recordigs.

lf-portal is available unter the terms of the GNU General Public License.
See 'license' for more details.

--------
Features
--------

User:

- Search in series and recordings
- List of all series
- View Recordings
- Authentication – access internal videos

Technology:

- Template based – easy design changes
- Simple Python based WSGI application
  * Flask as WSGI framework
  * Can be integrated into Apache, nginx, lighthttpd, gunicorn
- memcachd for fast, cached requests

Compatible with:

- Opencast Matterhorn 1.4.x
- Opencast Matterhorn 1.3.x *(1)*
- Lernfunk3
- Lernfunk2 (MH-Proxy)


<dl>
	<dt>Notice:</dt>
	<dd>
		Matterhorn 1.3.1 has some major bugs in its search service which cause
		performance issues and also incorrect paging of the series pages. The use
		of memcachd reduces the effect of the performance related issues.
		Nevertheless, if possible, use Matterhorn 1.4.x. For details about
		problematic bugs in 1.3.1 have a look at:
		<a href="https://opencast.jira.com/browse/MH-9800">MH-9800</a>,
		<a href="https://opencast.jira.com/browse/MH-9801">MH-9801</a>,
		<a href="https://opencast.jira.com/browse/MH-9802">MH-9802</a>
	</dd>
</dl>


------------
Installation
------------

**Requirements**

- Python
- Flask
- memcachd (optional but recommended)
  * Python memcachd module (python-memcached or pylibmc)
- WSGI capable server (optional but strongly recommended for productive usage)
  * Apache, i.e. with [mod_wsgi](http://code.google.com/p/modwsgi/)
  * [Gunicorn](http://gunicorn.org/)
  * For the 1k other options of deploying this see 
    [Flask: Deployment Options](http://flask.pocoo.org/docs/deploying/#deployment)


### The easy way ###

The easiest way is to use the build-in web server and just run the application.
The web server is, however, only build for debugging and testing purposes. It
will not perform very well. An application error might kill the whole server, …
In other words: Do not use this method for productive systems. At least not, if
you have more than 10 users.

If you notice during the installation that packages are not in the repository
of your distribution, use “**The easy way – 2**” which will tell you how to get
these packages from pypi instead.

1. Install Python and flask on your system:

		yum install python-flask

2. Install memcached and a python module for it (optional but recommended):

		yum install memcached

	You can either use python-memcached or python-pylibmc as python module for
	accessing memcached. pylibmc is based on the C library libmemcached. It is
	the faster of both modules. python-memcached on the other hand is a pure
	python module and thus easier to port. That is why it is available on more
	systems that pylibmc. If both modules are available, choose python-pylibmc.
	If not, use the one which is available. If both modules are installed,
	lf-portal will use pylibmc by default.

		yum install libmemcached python-pylibmc
		yum install python-memcached.noarch

	You might want to configure the service to your needs (i.e. allow more or
	less memory usage, …). Then start the service using the SysV-init script or
	the systemd script:

		service memcached start

	or

		systemctl start memcached.service

3. Clone the lf-portal repository:

		git clone https://github.com/lkiesow/lf-portal

4. Configure the portal:

	Open `portal.py` in the editor of your choice and set the configuration.
	Just go to the options at the top of the file. It should be done reasonable
	fast. The options itself are documented in the file.
	
5. Run lf-portal:

		python portal.py

	You can now access the portal using the web browser of your choice.


### The easy way – 2 ###

If you do not have all necessary python modules in your system repository or
they are quite old, you might consider creating a virtual environment and
install the python modules directly from the Python Package Index:

1. Clone the lf-portal repository:

		git clone https://github.com/lkiesow/lf-portal

2. Install python-virtualenv and create a virtual environment for python:

		yum install python-virtualenv
		cd lf-portal
		virtualenv venv

	Then activate the virtual environment:

		. ./venv/bin/activate

3. Install python modules:

		pip install Flask
		pip install python-memcached

4. Install and start memcached (optional but recommended):

		yum install memcached

	You might want to configure the service to your needs (i.e. allow more or
	less memory usage, …). Then start the service using the SysV-init script or
	the systemd script:

		service memcached start

	or

		systemctl start memcached.service

5. Configure the portal:

	Open `portal.py` in the editor of your choice and set the configuration.
	Just go to the options at the top of the file. It should be done reasonable
	fast. The options itself are documented in the file.
	
6. Run lf-portal:

		python portal.py

	You can now access the portal using the web browser of your choice.
	Remember to activate the virtual environment again each time you are in a
	new terminal and want to (re-)start the application.


### Deploy using Gunicorn ###

Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX. It is broadly
compatible with various web frameworks, simply implemented, light on server
resources, and fairly speedy.

You can deploy lf-portal with Gunicorn like this;

1. Clone the lf-portal repository:

		git clone https://github.com/lkiesow/lf-portal

2. Install python-virtualenv and create a virtual environment for python:

		yum install python-virtualenv
		cd lf-portal
		virtualenv venv

	Then activate the virtual environment:

		. ./venv/bin/activate

3. Install python modules:

		pip install Flask
		pip install python-memcached
		pip install gunicorn

4. Install and start memcached (optional but recommended):

		yum install memcached

	You might want to configure the service to your needs (i.e. allow more or
	less memory usage, …). Then start the service using the SysV-init script or
	the systemd script:

		service memcached start

	or

		systemctl start memcached.service

5. Configure the portal:

	Open `portal.py` in the editor of your choice and set the configuration.
	Just go to the options at the top of the file. It should be done reasonable
	fast. The options itself are documented in the file.
	
6. Run lf-portal:

	For details about all gunicorn options run:

		gunicorn --help

	For the beginning, just run:

		gunicorn -D --pid gunicorn.pid --error-logfile gunicorn.error.log \
			--access-logfile gunicorn.acess.log -w 4 -b 0.0.0.0:5000 portal:app

	This will launch Gunicorn as deamon with four workers. It will produce
	logfiles and will be globally accessible on port 5000.

	You can now access the portal using the web browser of your choice.
	Remember to activate the virtual environment again each time you are in a
	new terminal and want to (re-)start gunicorn..
