# -*- coding: utf-8 -*-
"""
	Flaskr
	~~~~~~

	A microblog example application written as Flask tutorial with
	Flask and sqlite3.

	:copyright: (c) 2010 by Armin Ronacher.
	:license: BSD, see LICENSE for more details.
"""
from __future__ import with_statement
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
		render_template, flash, _app_ctx_stack
import urllib2
from xml.dom.minidom import parseString
import random

# configuration
SEARCH_SERVICE = 'http://video2.virtuos.uos.de:8080/search/'
ENGAGE_SERVICE = 'http://video2.virtuos.uos.de:8080/engage/'
SECRET_KEY = 'development key'
SERIES_PER_PAGE = 50

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)


def get_db():
	"""Opens a new database connection if there is none yet for the
	current application context.
	"""
	'''
	top = _app_ctx_stack.top
	if not hasattr(top, 'sqlite_db'):
		sqlite_db = sqlite3.connect(app.config['DATABASE'])
		sqlite_db.row_factory = sqlite3.Row
		top.sqlite_db = sqlite_db

	return top.sqlite_db
	'''
	pass


@app.teardown_appcontext
def close_db_connection(exception):
	"""Closes the database again at the end of the request."""
	top = _app_ctx_stack.top
	if hasattr(top, 'sqlite_db'):
		top.sqlite_db.close()


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
	'''
	if cookie:
		req.add_header('cookie', 'session="%s"; Path=/; HttpOnly' % cookie)
	'''
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
def lectures():
	page  = int(request.args.get('page') or 1)
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
def series(id):
	data     = request_data('series', 1, 0, id=id)
	series   = prepare_series(data)
	series   = series[0] if series else None

	data     = request_data('episode', 999, 0, sid=series.get('id'))
	episodes = prepare_episode(data)

	return render_template('series.html', series=series, episodes=episodes)


@app.route('/search')
def search():
	page  = int(request.args.get('page') or 1)
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


@app.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	db = get_db()
	db.execute('insert into entries (title, text) values (?, ?)',
			[request.form['title'], request.form['text']])
	db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('home'))
		return render_template('login.html', error=error)


@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))


if __name__ == '__main__':
	app.run(debug=True)
