#!/usr/bin/env python

import operator, os, pickle, sys
import json, cherrypy
import hrse, query, math, time
from genshi.template import TemplateLoader
import MySQLdb
import ConfigParser


webhome = "/home/hrseweb/hrse"
templdir = webhome+"/templates"

loader = TemplateLoader(
    templdir,
    auto_reload=True
)


def getval(spec, jdict=None):
    """Retrieve the value of the specified attribute.

    The attribute to retrieve is specified via the spec parameter, where:
       spec: 'parent1:parent2:...:parentN:valname'

    The jdict parameter is the dictionary of dictionaries to extract the
    value from.  Typically this would be the decoded JSON document that was
    passed into the web service.

    If the value is not found, this function will raise a KeyError.

    """
    if jdict is None:
        raise RuntimeError, "getval(): You passed me an empty jdict!"

    if ':' in spec:
        valpath = spec.split(':')
        return getval(':'.join(valpath[1:]),
                           jdict[valpath[0]])

    return jdict[spec]


class Root():
    """This is the default root object needed for a CherryPy web instance."""
    def __init__(self, credentials):
        self.creds = credentials


    @cherrypy.expose
    def index(self):
        tmpl = loader.load('index.html')

        return tmpl.generate().render('html', doctype='html', strip_whitespace=False)


    @cherrypy.expose
    def getpid(self, **kwargs):
        """Load the participant's ID from the database if it exists.  If not,
        create a new participant.  Return the participant ID and the formatted
        date of admittance to the experiment.

        """
        data = json.loads(cherrypy.request.body.read())
        fingerprint = getval("fingerprint", data)
        useragent = getval("useragent", data)

        db = MySQLdb.connect(self.creds['host'], self.creds['user'], self.creds['passwd'], 'hrse')
        id = query.createparticipant(db, fingerprint, useragent)
        admitdate = query.getadmittance(db, id)

        return json.dumps({"id": id, "date": admitdate.ctime()})


    @cherrypy.expose
    def myinfo(self, **kwargs):
        """Update the participant's demographic information.

        This method is almost exactly like the submit() method, except that we
        do not attempt to submit a new sequence in this method.

        """
        data = json.loads(cherrypy.request.body.read())
        print "myinfo called with: "+str(data)
        fingerprint = getval("fingerprint", data)

        db = MySQLdb.connect(self.creds['host'], self.creds['user'], self.creds['passwd'], 'hrse')
        id = query.getparticipantid(db, fingerprint)
        demodata = query.getparticipantinfo(db, id)

        data = {'id': id}
        data.update(demodata)

        print "myinfo: loading myinfo.html template with data="+str(data)
        tmpl = loader.load('myinfo.html')
        return tmpl.generate(data=data).render('html', doctype='html', strip_whitespace=False)


    @cherrypy.expose
    def submit(self, **kwargs):
        """Insert the given sequence into the database, and direct the user
        to the myinfo page for demographic info collection.

        """
        data = json.loads(cherrypy.request.body.read())
        print "submit called with: "+str(data)
        sequence = getval("sequence", data)
        fingerprint = getval("fingerprint", data)
        useragent = getval("useragent", data)

        db = MySQLdb.connect(self.creds['host'], self.creds['user'], self.creds['passwd'], 'hrse')
        id = query.createparticipant(db, fingerprint, useragent)
        query.insertsequence(db, fingerprint, sequence, useragent)
        demodata = query.getparticipantinfo(db, id)

        data = {'id': id}
        data.update(demodata)

        tmpl = loader.load('myinfo.html')
        return tmpl.generate(data=data).render('html', doctype='html', strip_whitespace=False)


    @cherrypy.expose
    def demosubmit(self, **kwargs):
        """Generate a page of charts that describes the statistical analysis
        of the participant's sequence.

        """
        data = json.loads(cherrypy.request.body.read())
        print "demosubmit called with: "+str(data)
        fingerprint = getval("fingerprint", data)

        db = MySQLdb.connect(self.creds['host'], self.creds['user'], self.creds['passwd'], 'hrse')
        id = query.getparticipantid(db, fingerprint)
        sequences = query.getsequences(db, fingerprint)
        sequence = sequences[len(sequences)-1]
        
        # Create a dictionary of demographic data that were provided by the participant
        demodata = {}
        try: demodata.update({'maritalstatus': getval("formdata:maritalstatus", data)})
        except KeyError: pass
        try: demodata.update({'curzip': getval("formdata:curzip", data)})
        except KeyError: pass
        try: demodata.update({'origzip': getval("formdata:origzip", data)})
        except KeyError: pass
        try: demodata.update({'family': getval("formdata:family", data)})
        except KeyError: pass
        try: demodata.update({'residence': getval("formdata:residence", data)})
        except KeyError: pass
        try: demodata.update({'age': getval("formdata:age", data)})
        except KeyError: pass
        try: demodata.update({'education': getval("formdata:education", data)})
        except KeyError: pass
        try: demodata.update({'handed': getval("formdata:handed", data)})
        except KeyError: pass
        try: demodata.update({'income': getval("formdata:income", data)})
        except KeyError: pass
        try: demodata.update({'military': getval("formdata:military", data)})
        except KeyError: pass
        try: demodata.update({'sex': getval("formdata:sex", data)})
        except KeyError: pass
        try: demodata.update({'employment': getval("formdata:employment", data)})
        except KeyError: pass

        print "demodata: "+str(demodata)
        # If there was any demographic data provided, insert it into the database.
        if len(demodata) > 0:
            query.submitdemo(db, id, demodata)

        # The value for resultspage is a path to a newly created Genshi
        # template which includes images of all the pygal-generated charts.
        charts = hrse.genresults(db, sequence, fingerprint)

        data = {'curdate': time.ctime(),
                'id': id,
                'sequence': sequence,
                'small_zerostoones': charts['small_zerostoones'],
                'large_zerostoones': charts['large_zerostoones'],
                'small_runlengths': charts['small_runlengths'],
                'large_runlengths': charts['large_runlengths']}

        tmpl = loader.load("myresults.html")
        return tmpl.generate(data=data).render('html', doctype='html', strip_whitespace=False)


def main():
    cp = ConfigParser.ConfigParser()
    cp.read([os.path.expanduser('~/.my.cnf')])
    credentials = {'user': cp.get('mysql', 'user'),
                   'passwd': cp.get('mysql', 'password'),
                   'host': cp.get('mysql', 'host')}

    # Test the database connection (an exception will be raised if this fails).
    db = MySQLdb.connect(credentials['host'], credentials['user'], credentials['passwd'], 'hrse')
    db.close()

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

    cherrypy.quickstart(Root(credentials), '/', {
        '/static': {
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
        '/jc': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'js'
        },
        '/img': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'img'
        },
        '/favicon.ico': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': '/home/hrseweb/hrse/img/hrse.ico'
        }
    })


if __name__ == '__main__':
    main()

