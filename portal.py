# -*- coding: utf-8 -*-
"""
	Flaskr
	~~~~~~

	A microblog example application written as Flask tutorial with
	Flask and sqlite3.

	:copyright: (c) 2010 by Armin Ronacher.
	:license: BSD, see LICENSE for more details.
"""
from functools import wraps
from flask import Flask, request, session, g, redirect, url_for, abort, \
		render_template, flash, _app_ctx_stack
import urllib
import urllib2
from xml.dom.minidom import parseString
import random
import pylibmc

# configuration
SEARCH_SERVICE = 'http://video2.virtuos.uos.de:8080/search/'
ENGAGE_SERVICE = 'http://video2.virtuos.uos.de:8080/engage/'
SPRING_SECURITY_SERVICE = 'http://video2.virtuos.uos.de:8080/j_spring_security_check'
SECRET_KEY      = 'development key'
SERIES_PER_PAGE = 50

USE_MEMCACHD    = True
MEMCACHED_HOST  = 'localhost'
CACHE_TIME_SEC  = 600

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)


def get_mc():
	'''Returns a Memcached client. If there is none for the current application
	context it will create a new.
	'''
	top = _app_ctx_stack.top
	if not hasattr(top, 'memcached_cli'):
		top.memcached_cli = pylibmc.Client(
				[app.config['MEMCACHED_HOST']], binary = True,
				behaviors = {'tcp_nodelay': True, 'ketama': True})
	return top.memcached_cli


def cached(time=app.config['CACHE_TIME_SEC']):
	def decorator(f):
		@wraps(f)
		def decorated(*args, **kwargs):
			if not app.config['CACHE_TIME_SEC']:
				return f(*args, **kwargs)
			mc = get_mc()
			key = 'lf_portal_' + request.url \
					+ str(request.cookies.get('JSESSIONID'))
			result = mc.get(key)
			if not result:
				result = f(*args, **kwargs)
				mc.set(key, result, time)
			return result
		return decorated
	return decorator


def request_data(what, limit, offset, id=None, sid=None, q=None):
	url  = '%s%s.xml?limit=%i&offset=%i' % \
			( app.config['SEARCH_SERVICE'], what, limit, offset )
	if id:
		url += '&id=%s' % id
	if sid:
		url += '&sid=%s' % sid
	if q:
		url += '&q=%s' % q
	req  = urllib2.Request(url)
	
	cookie = request.cookies.get('JSESSIONID')
	if cookie:
		req.add_header('cookie', 'session="%s"; Path=/; HttpOnly' % cookie)

	req.add_header('Accept', 'application/xml')
	u = urllib2.urlopen(req)
	try:
		data = parseString(u.read())
	finally:
		u.close()
	return data


def get_xml_val(elem, name):
	try:
		return elem.getElementsByTagNameNS('*', name)[0].childNodes[0].data
	except IndexError:
		return ''


def prepare_episode(data):
	episodes = []
	for media in data.getElementsByTagNameNS('*', 'mediapackage'):
		id = media.getAttribute('id')
		title       = get_xml_val(media, 'title')
		series      = get_xml_val(media, 'series')
		seriestitle = get_xml_val(media, 'seriestitle')
		img = None
		for attachment in media.getElementsByTagNameNS('*', 'attachment'):
			if attachment.getAttribute('type').endswith('/player+preview'):
				img = attachment.getElementsByTagNameNS('*', 'url')[0].childNodes[0].data


		episodes.append( {'id':id, 'title':title, 'series':series,
			'seriestitle':seriestitle, 'img':img} )
	return episodes


def prepare_series(data):
	series = []
	for result in data.getElementsByTagNameNS('*', 'result'):
		if get_xml_val(result, 'mediaType') != 'Series':
			continue
		id = result.getAttribute('id')
		title       = get_xml_val(result, 'dcTitle')
		description = get_xml_val(result, 'dcDescription')

		creator     = [ c.childNodes[0].data 
				for c in result.getElementsByTagNameNS('*', 'dcCreator') ]

		contributor = [ c.childNodes[0].data 
				for c in result.getElementsByTagNameNS('*', 'dcContributor') ]

		series.append( {'id':id, 'title':title, 'creator':creator,
			'contributor':contributor} )
	return series


@app.route('/')
@cached(10)
def home():
	data = request_data('episode',6,0)
	total = data.getElementsByTagNameNS('*', 'search-results')[0].getAttribute('total')
	new_episodes = prepare_episode(data)

	# get some random picks
	# random.seed()
	offsets = [x+1 for x in random.sample(xrange(int(total)), 6)]
	random_episodes = []
	for offset in offsets:
		data = request_data('episode',1,offset)
		random_episodes += prepare_episode(data)

	return render_template('home.html', new_episodes=new_episodes,
			random_episodes=random_episodes)


@app.route('/lectures')
@app.route('/lectures/<int:page>')
@cached()
def lectures(page=1):
	page -= 1

	data = request_data('series', app.config['SERIES_PER_PAGE'], 
			app.config['SERIES_PER_PAGE'] * page)
	total = data.getElementsByTagNameNS('*', 'search-results')[0].getAttribute('total')
	series = prepare_series(data)

	pages = [ p+1 for p in xrange(int(total) / app.config['SERIES_PER_PAGE']) ]
	return render_template('lectures.html', series=series, pages=pages, activepage=page)


@app.route('/episode/<id>')
def episode(id):
	data    = request_data('episode', 1, 0, id=id)
	episode = prepare_episode(data)
	episode = episode[0] if episode else None
	return render_template('episode.html', episode=episode, 
			engage=app.config['ENGAGE_SERVICE'])


@app.route('/series/<id>')
@cached()
def series(id):
	data     = request_data('series', 1, 0, id=id)
	series   = prepare_series(data)
	series   = series[0] if series else None

	data     = request_data('episode', 999, 0, sid=series.get('id'))
	episodes = prepare_episode(data)

	return render_template('series.html', series=series, episodes=episodes)


@app.route('/search')
@app.route('/search/<int:page>')
@cached()
def search(page=1):
	page -= 1
	q     = request.args.get('q')

	series = []
	if not page:
		data     = request_data('series', 9999, 0, q=q)
		series   = prepare_series(data)

	data     = request_data('episode', 9, 0, q=q)
	total    = data.getElementsByTagNameNS('*', 'search-results')[0].getAttribute('total')
	episodes = prepare_episode(data)

	pages = [ p+1 for p in xrange(int(total) / 9) ]

	return render_template('search.html', series=series, episodes=episodes,
			pages=pages, activepage=page)


class NoRedirection(urllib2.HTTPErrorProcessor):
	def http_response(self, request, response):
		return response

	https_response = http_response


@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		# Prepare data
		data = {
				'j_username': request.form['username'],
				'j_password': request.form['password'] }
		try:
			'''
			req  = urllib2.Request(app.config['SPRING_SECURITY_SERVICE'])
			req.add_data(urllib.urlencode(data))
			u = urllib2.urlopen(req)
			'''
			opener = urllib2.build_opener(NoRedirection)
			u = opener.open(app.config['SPRING_SECURITY_SERVICE'],
					urllib.urlencode(data))
			if '/login.html' in u.headers.get('location'):
				return render_template('login.html',
						error='Could not log in. Incorrect credentials?')
			cookie = u.headers.get('Set-Cookie')
			u.close()

			response = redirect(url_for('home'))
			response.headers['Set-Cookie'] = cookie
			return response

		except urllib2.HTTPError as e:
			if e.code == 404:
				return render_template('login.html',
						error='Login service returned error. Please report this.')
			if e.code == 401:
				return render_template('login.html',
						error='Could not log in. Incorrect credentials?')
			raise e

	return render_template('login.html')


@app.route('/logout')
def logout():
	response = redirect(url_for('home'))
	response.headers['Set-Cookie'] = 'JSESSIONID=x; Expires=Wed, 09 Jun 1980 10:18:14 GMT'
	return response


if __name__ == '__main__':
	app.run(debug=True)
