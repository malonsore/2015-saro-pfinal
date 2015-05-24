from django.conf.urls import patterns, include, url
from django.contrib   import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/'         , include(admin.site.urls)),
	url(r'^$'              , 'app.views.indice'),
	url(r'^login'         , 'app.views.login_view'),
	url(r'^ayuda'         , 'app.views.ayuda'),
	url(r'^logout'        , 'app.views.logout_view'),
	url(r'^portales/(.+)'        , 'app.views.portales'),
	url(r'^image'        , 'app.views.image'),
	url(r'^css'           , 'app.views.css'),
	url(r'^eventos'   , 'app.views.eventos'),
	url(r'^actividad/(.+)'      , 'app.views.actividad'),
	url(r'^(.+)/RSS'      , 'app.views.canalRSS'),
	url(r'^(.+)'          , 'app.views.usuario')
	)

