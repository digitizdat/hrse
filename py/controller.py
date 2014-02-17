#!/usr/bin/env python

import operator, os, pickle, sys
import json, cherrypy
import math, time
from hrse import getval, genresults, renderimages
import query, form, daemon, config
from genshi.template import TemplateLoader
import MySQLdb
import ConfigParser
from cherrypy import log


templdir = config.get('templates')
progname = "hrsedaemon"

loader = TemplateLoader(
    templdir,
    auto_reload=True
)


class Root():
    """This is the default root object needed for a CherryPy web instance."""
    def __init__(self, credentials):
        self.creds = credentials  # Database credentials
        self.pool = {}  # a rudimentary connection pool for the db connections
        self.last = 0   # This tracks the latest sequence ID so that we can
                        # determine if we need to re-render the PNGs for the
                        # overall stats page.


    @cherrypy.expose
    def index(self):
        """Load the front page."""

        tmpl = loader.load('index.html')

        return tmpl.generate().render('html', doctype='html', strip_whitespace=False)


    @cherrypy.expose
    def getpid(self, **kwargs):
        """Return the participant's ID, if it exists, along with a new sequence ID.

        If the participant doesn't already exist, create a new participant,
        the formatted date of admittance to the experiment, and a new sequence ID.

        """
        data = json.loads(cherrypy.request.body.read())
        log("getpid called with: "+str(data))
        fingerprint = getval("fingerprint", data)
        useragent = getval("useragent", data)
        screenwidth = getval("screenwidth", data)

        db = MySQLdb.connect(self.creds['host'], self.creds['user'], self.creds['passwd'], 'hrse')
        id = query.createparticipant(db, fingerprint)
        admitdate = query.getadmittance(db, id)
        seqid = query.startsequence(db, fingerprint, useragent, screenwidth)
        #self.pool.update({seqid: (db, time.time())})

        # Do some housecleaning on the pool.  This could reasonably be put in
        # a function that gets called every 61 minutes, but I think this will
        # be fine too, since this function is only called when the first page
        # is loaded, and I don't expect a regular stream of traffic on this
        # website.
        query.prunepool(self.pool)

        return json.dumps({"id": id, "seqid": seqid, "date": admitdate.ctime()})


    @cherrypy.expose
    def updateseq(self, **kwargs):
        """Update the sequence in the database given by the sequenceid with the given sequence."""
        data = json.loads(cherrypy.request.body.read())
        log("updateseq called with: "+str(data))
        seqid = getval("seqid", data)
        sequence = getval("sequence", data)
        inittime = getval("inittime", data)
        keyboard = getval("keyboard", data)
        mouse = getval("mouse", data)
        touch = getval("touch", data)

        # There should already be a connection for us in the connection pool.
        try:
            db = self.pool[seqid][0]
            log("updateseq: reusing available db connection: "+str(self.pool))
        except KeyError:
            log("updateseq: Opening a new connection to continue sequence "+str(seqid))
            db = MySQLdb.connect(self.creds['host'], self.creds['user'], self.creds['passwd'], 'hrse')
            #self.pool.update({seqid: (db, time.time())})

        # Update the given sequence
        try:
            query.updatesequence(db, seqid, sequence, inittime, keyboard, mouse, touch)
        except MySQLdb.OperationalError:
            log("updateseq: Connection was closed during update for sequence "+str(seqid)+" (code: "+str(v)+")")
            pass

        return


    @cherrypy.expose
    def endsequence(self, **kwargs):
        """Close the connection in the connection pool for the given sequence ID."""
        data = json.loads(cherrypy.request.body.read())
        log("endsequence called with: "+str(data))
        seqid = getval("seqid", data)
        sequence = getval("sequence", data)
        inittime = getval("inittime", data)
        keyboard = getval("keyboard", data)
        mouse = getval("mouse", data)
        touch = getval("touch", data)

        # Update the given sequence
        try:
            db = self.pool[seqid][0]
            log("updateseq: reusing available db connection: "+str(self.pool))
        except KeyError:
            log("updateseq: Opening a new connection to conclude sequence "+str(seqid))
            db = MySQLdb.connect(self.creds['host'], self.creds['user'], self.creds['passwd'], 'hrse')
            #self.pool.update({seqid: (db, time.time())})

        try:
            log("endsequence: committing final upate for sequence "+str(seqid))
            query.updatesequence(db, seqid, sequence, inittime, keyboard, mouse, touch)
        except MySQLdb.OperationalError, v:
            log("endsequence: Connection was closed during update for sequence "+str(seqid)+" (code: "+str(v)+")")
            pass

        log("endsequence: returned from final update to sequence "+str(seqid))

        # Shut down the db connection
        if seqid in self.pool:
            log("endsequence: closing DB connection for sequence "+str(seqid))
            self.pool[seqid][0].close()
            del self.pool[seqid]

        # Generate the PNGs for this sequence
        log("endsequence: rendering images for sequence "+str(seqid))
        renderimages(sequence, seqid)

        # Generate new PNGs for the overall stats
        log("endsequence: calling overallstats"+str(seqid))
        self.overallstats()


    @cherrypy.expose
    def yourinfo(self, **kwargs):
        """Update the participant's demographic information.

        This method is almost exactly like the submit() method, except that we
        do not attempt to submit a new sequence in this method (so, these two
        methods could probably be consolidated by examining the referrer,
        although I'm not sure if that's actually possible since I'm just
        AJAXing between pages).

        """
        data = json.loads(cherrypy.request.body.read())
        log("yourinfo called with: "+str(data))
        fingerprint = getval("fingerprint", data)

        # Create a database connection
        db = MySQLdb.connect(self.creds['host'], self.creds['user'], self.creds['passwd'], 'hrse')
        id = query.getparticipantid(db, fingerprint)

        # Load the yourinfo page
        data = {'id': id}
        data.update(form.formvars(query.getparticipantinfo(db, id)))
        tmpl = loader.load('yourinfo.html')

        return tmpl.generate(data=data).render('html', doctype='html', strip_whitespace=False)


    @cherrypy.expose
    def demosubmit(self, **kwargs):
        """Organize the given form data (given in JSON) and pass it into the
        query.submitdemo() function to update the database, then load the
        results page.

        """
        data = json.loads(cherrypy.request.body.read())
        log("demosubmit called with: "+str(data))
        fingerprint = getval("fingerprint", data)

        # Create a database connection
        db = MySQLdb.connect(self.creds['host'], self.creds['user'], self.creds['passwd'], 'hrse')
        id = query.getparticipantid(db, fingerprint)
        
        # Submit the given form data to the database
        query.submitdemo(db, id, data)

        return


    @cherrypy.expose
    def yourresults(self, **kwargs):
        """Load the yourresults page for the sequence submitted most recently by
        the current browser fingerprint.

        """
        data = json.loads(cherrypy.request.body.read())
        log("yourresults called with: "+str(data))
        fingerprint = getval("fingerprint", data)

        # Create a database connection
        db = MySQLdb.connect(self.creds['host'], self.creds['user'], self.creds['passwd'], 'hrse')
        id = query.getparticipantid(db, fingerprint)
        
        # Load the most recently submitted sequence for this fingerprint
        results = query.getsequences(db, fingerprint)
        mostrecent = results[len(results)-1]

        # Load the yourresults page
        data = {'curdate': time.ctime(),
                'id': id,
                'sequence': mostrecent['sequence']}
        data.update(genresults(mostrecent['sequence'], mostrecent['idsequences']))
        tmpl = loader.load("yourresults.html")

        return tmpl.generate(data=data).render('html', doctype='html', strip_whitespace=False)


    @cherrypy.expose
    def overallstats(self, **kwargs):
        """Load the overall results page."""
        log("overallstats: called")

        # Create a database connection
        db = MySQLdb.connect(self.creds['host'], self.creds['user'], self.creds['passwd'], 'hrse')

        # Determine the sequence ID of the last time we rendered the overall stats
        last = query.getlastseqid(db)

        # Only perform the renderings if there is new data to render for.
        if last > self.last:
            log("overallstats: rendering overall images, updating last to "+str(last))
            self.last = last
            renderpngs = True
        else:
            log("overallstats: setting renderpngs to false")
            renderpngs = False

        # Create a sequence of all sequences concatenated together
        sequence = ''.join(query.getallsequences(db))

        data = {'curdate': time.ctime()}
        data.update(genresults(sequence, 'overall', renderpngs))

        tmpl = loader.load("overall.html")

        return tmpl.generate(data=data).render('html', doctype='html', strip_whitespace=False)


    @cherrypy.expose
    def about(self, **kwargs):
        """Load the about page."""

        tmpl = loader.load("about.html")

        return tmpl.generate().render('html', doctype='html', strip_whitespace=False)



if __name__ == '__main__':
    # Daemonize
    pid = daemon.become(close_stderr=False)

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
        'tools.staticdir.root': config.get('hrsehome'),
        'log.access_file': config.get('accesslog'),
        'log.error_file': config.get('errorlog'),
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 80
    })

    cherrypy.quickstart(Root(credentials), '/', {
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
            'tools.staticfile.filename': config.get('favicon')
        }
    })


