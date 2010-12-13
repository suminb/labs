from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^webarchive$', 'incubator.views.webarchive'),
    (r'^webarchive/thumbnail$', 'incubator.views.webarchive_thumbnail'),
    
    (r'^youtube$', 'incubator.views.youtube'),
    (r'^youtube/getinfo$', 'incubator.views.youtube_getinfo'),

	(r'^minesweeper$', 'incubator.views.minesweeper'),
	(r'^minesweeper/init$', 'incubator.views.minesweeper_init'),
	(r'^minesweeper/mines$', 'incubator.views.minesweeper_mines'),
	(r'^minesweeper/click/(?P<x>\d+),(?P<y>\d+)$', 'incubator.views.minesweeper_click'),
	
	(r'^$', 'incubator.sector7.index'),
	(r'^auth$', 'incubator.sector7.auth'),
)
