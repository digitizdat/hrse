#!/usr/bin/env python

import operator, os, pickle, sys
import cherrypy
from genshi.template import TemplateLoader

webhome = "/home/hrseweb/hrse"
templdir = webhome+"/templates"

loader = TemplateLoader(
    templdir,
    auto_reload=True
)


class Root(object):
    def __init__(self, data):
        self.data = data

    @cherrypy.expose
    def index(self):
        tmpl = loader.load('index.html')
        return tmpl.generate(title='Human Random Sequence Experiment').render('html', doctype='html', strip_whitespace=False)


def main(filename):
    data = {} # We'll replace this later

    # Some global configuration; note that this could be moved into a
    # configuration file
    cherrypy.config.update({
        'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
        'tools.decode.on': True,
        'tools.trailing_slash.on': True,
        'tools.staticdir.root': webhome,
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 80
    })

    cherrypy.quickstart(Root(data), '/', {
        '/media': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static'
        },
        '/stylesheets': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'stylesheets'
        },
        '/js': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'bower_components'
        },
        '/img': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'img'
        }
    })

if __name__ == '__main__':
    main(sys.argv[1])

