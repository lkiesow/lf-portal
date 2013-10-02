# -*- coding: utf-8 -*-
'''
	LF-Portal :: Simple Player Plugin
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	This plugin tries the include the Opencast Engage Player using a preset
	engage server and the episode identifier.

	This plugin needs the ENGAGE_SERVICE configuration parameter.

	:copyright: 2013 by Lars Kiesow <lkiesow@uos.de>
	:license: GPL, see LICENSE for more details.
'''

# Set default encoding to UTF-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def player( media, config, request ):
	'''Generate an HTML code for the inclusion of the player into the portal.

	:param media:   Mediapackage media XML structure
	:param config:  Portal configuration
	:param request: Current request object
	'''
	id = media.getAttribute('id')
	session = request.cookies.get('JSESSIONID')
	session = (';jsessionid=%s' % session) if session else ''
	embed   = '%sui/embed.html%s?id=%s' % (config['ENGAGE_SERVICE'], session, id)
	engage  = '%sui/watch.html%s?id=%s' % (config['ENGAGE_SERVICE'], session, id)
	html = '<iframe src="%s"></iframe>' % embed
	data = {'engagelink' : engage}
	return html, data
