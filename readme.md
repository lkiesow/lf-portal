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

-----------------
Demo Installation
-----------------

A demonstration and testing environment can be found here:

	[http://repo.virtuos.uos.de:5000/](http://repo.virtuos.uos.de:5000/)

It is running on a test VM and is deployed using Gunicorn with 4 worker
processes.

---------------
Getting Started
---------------

For installation, configuration and customization guides have a look at the
[Wiki](https://github.com/lkiesow/lf-portal/wiki)
