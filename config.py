# -*- coding: utf-8 -*-
'''
	LF-Portal: Configuration
	~~~~~~~~~~~~~~~~~~~~~~~~

	A video portal for Opencast Matterhorn and compatible systems.

	:copyright: 2013 by Lars Kiesow <lkiesow@uos.de>
	:license: GPL, see LICENSE for more details.
'''

SEARCH_SERVICE   = 'http://engage.opencast.org/search/'
SECURITY_SERVICE = 'http://engage.opencast.org/j_spring_security_check'

# The amount of series per page to display on /serieslist
SERIES_PER_PAGE  = 15

# The amount of series per page to display on /recordinglist
RECORDINGS_PER_PAGE  = 9

# The amount of videos displayed on the home page
NEW_EPISODES_ON_HOME    = 6
RANDOM_EPISODES_ON_HOME = 6

# The amount of recordings per search page
SEARCH_RESULTS_PER_PAGE = 9

# One of: simple, track-url, included
#   simple    Try to construct the player URL by ENGAGE_SERVICE variable and
#             mediapackage id. Fast but reliable only in some cases. Not if
#             there are more than one engage server and not if the IDs might
#             have changed.
#   track-url Try to construct the engage player URL from a random track URL.
#             This will work in most cases. Even if there are more than one
#             engage server. Not, however, if the tracks are served from a
#             dedicated server which is not the engage server.
#   included  Uses the links included in the mediapackage. This is the most
#             reliable one. But this method only works if the links to the
#             player are included into the mediapackage.
ENGAGE_URL_DETECTION = 'track-url'

# Set this if ENGAGE_URL_DETECTION is set to simple:
#ENGAGE_SERVICE   = 'http://engage.opencast.org/engage/'

# Set this if ENGAGE_URL_DETECTION is set to track-url:
# The following value specifies the position of the mediapackage identifier in
# a track URL, if split by '/':
TRACK_ID_PART = 5

# Part which will be added to all detectet server URLs.
# For example if you serve your files using lighthttpd from port 80 and your
# Engage Service will run on port 8080 you might want to add ':8080' as the
# port will be missing from the autodetection.
#URL_ADD_PART = ':8080'


USE_MEMCACHD     = True
MEMCACHED_HOST   = 'localhost:11211'
CACHE_TIME_SEC   = 600

# Configuration for built-in server only:
SERVER_DEBUG = True
SERVER_HOST  = '0.0.0.0' # Set to localhost for local access only
SERVER_PORT  = 5000
