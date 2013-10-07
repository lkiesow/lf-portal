# -*- coding: utf-8 -*-
'''
	LF-Portal
	~~~~~~~~~

	A really simple colorization plug-in which just uses the first six
	characters from the identifier assuming that it is a uuid and thus that
	these characters are proper hexadecimal values.

	:copyright: 2013 by Lars Kiesow <lkiesow@uos.de>
	:license: GPL, see LICENSE for more details.
'''

# Set default encoding to UTF-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def seriescolor(id, title, config):
	return id[:6]
