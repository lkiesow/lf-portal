# -*- coding: utf-8 -*-
'''
	LF-Portal
	~~~~~~~~~

	A basic algorithm for color generation for series

	:copyright: 2013 by Lars Kiesow <lkiesow@uos.de>
	:license: GPL, see LICENSE for more details.
'''

# Set default encoding to UTF-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def seriescolor(id, title, config):
	rgb_max    = config['SERIESCOLOR_SUM_MAX']
	rgb_offset = config['SERIESCOLOR_SUM_OFFSET']
	rgb        = [0, 0, 0]

	s = (id if config.get('SERIESCOLOR_SUM_USE_ID') else '') + \
			(title if config.get('SERIESCOLOR_SUM_USE_TITLE') else '')
	i = 0
	for c in s:
		rgb[i] += ord(c)
		i = (i+1) % 3;

	rgb[0] = '%0.2x' % ((rgb[0] % rgb_max[0]) + rgb_offset[0])
	rgb[1] = '%0.2x' % ((rgb[1] % rgb_max[1]) + rgb_offset[1])
	rgb[2] = '%0.2x' % ((rgb[2] % rgb_max[2]) + rgb_offset[2])

	return ''.join(rgb)
