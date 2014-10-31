#!/usr/bin/env python

import operator, os, pickle, sys, pwd, grp
import json, cherrypy
import math, time
from hrse import genresults, renderimages
from data import getval
import query, form, daemon, config
from genshi.template import TemplateLoader
import MySQLdb
import ConfigParser
from cherrypy import log
from cherrypy.process.plugins import DropPrivileges


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
        fingerprint = getval("fingerprint", data)
        useragent = getval("useragent", data)
        screenwidth = getval("screenwidth", data)
        referrer = getval("referrer", data)
        prevpid = getval("prevpid", data)

        # Debug
        log("getpid called with: "+str(data))
        print "fingerprint is type "+str(type(fingerprint))

        db = MySQLdb.connect(self.creds['host'], self.creds['user'], self.creds['passwd'], 'hrse')
        id = query.createparticipant(db, fingerprint, referrer, prevpid)
        admitdate = query.getadmittance(db, id)
        seqid = query.startsequence(db, fingerprint, useragent, screenwidth)
        seqcount = len(query.getseqsbypid(db, id))

        return json.dumps({"id": id,
                           "seqid": seqid,
                           "date": admitdate.ctime(), 
                           "seqcount": seqcount})


    def submitseq(self, seqid, data):
        """Update the sequence in the database given by the sequenceid with the given sequence.

        This method differs from updateseq() and endsequence() in that it is
        not exposed as a web method and it takes the parsed JSON document as
        input.  It is meant to be called from both of the other two functions.

        """
        sequence = getval("sequence", data)
        keyboard = getval("keyboard", data)
        mouse = getval("mouse", data)
        touch = getval("touch", data)
        starttime = getval("starttime", data)
        firstchartime = getval("firstchartime", data)
        lastchartime = getval("lastchartime", data)
        tbcmax = getval("tbcmax", data)
        tbcmin = getval("tbcmin", data)
        tbcmean = getval("tbcmean", data)
        tbcmedian = getval("tbcmedian", data)
        tbcrange = getval("tbcrange", data)
        tbcstdev = getval("tbcstdev", data)
        tbcsumsqrd = getval("tbcsumsqrd", data)
        tbcsumsqerr = getval("tbcsumsqerr", data)
        tbcmeansqerr = getval("tbcmeansqerr", data)
        tbcgeomean = getval("tbcgeomean", data)
        tbcvariance = getval("tbcvariance", data)
        tbccoeffvar = getval("tbccoeffvar", data)
        endtime = getval("endtime", data)

        log("submitseq: Opening a new connection to continue sequence "+str(seqid))
        db = MySQLdb.connect(self.creds['host'], self.creds['user'], self.creds['passwd'], 'hrse')

        # Submit the given sequence
        try:
            query.updatesequence(db, sequence, seqid, keyboard, mouse, touch,
                                 starttime, firstchartime, lastchartime,
                                 tbcmax, tbcmin, tbcmean, tbcmedian, tbcrange,
                                 tbcstdev, tbcsumsqrd, tbcsumsqerr,
                                 tbcmeansqerr, tbcgeomean, tbcvariance,
                                 tbccoeffvar, endtime)
        except MySQLdb.OperationalError, v:
            log("submitseq: a DB error occurred during the update for sequence "+str(seqid)+" ("+str(v)+")")
            pass

        return


    @cherrypy.expose
    def updateseq(self, **kwargs):
        """Update the sequence in the database given by the sequenceid with the given sequence."""
        data = json.loads(cherrypy.request.body.read())
        seqid = getval("seqid", data)

        # Debug
        log("updateseq called with: "+str(data))

        log("updateseq: submitting update for sequence "+str(seqid))
        self.submitseq(seqid, data)
        log("updateseq: returned from update for sequence "+str(seqid))

        return


    @cherrypy.expose
    def endsequence(self, **kwargs):
        """Conclude the sequence for the given sequence ID."""
        data = json.loads(cherrypy.request.body.read())
        seqid = getval("seqid", data)
        sequence = getval("sequence", data)

        # Debug
        log("endsequence called with: "+str(data))

        log("endsequence: committing final upate for sequence "+str(seqid))
        self.submitseq(seqid, data)
        log("endsequence: returned from final update to sequence "+str(seqid))

        # Generate the PNGs for this sequence
        log("endsequence: rendering images for sequence "+str(seqid))
        renderimages(sequence, seqid)

        # Generate new PNGs for the overall stats
        log("endsequence: calling overallstats for sequence "+str(seqid))
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
        fingerprint = getval("fingerprint", data)

        # Debug
        log("yourinfo called with: "+str(data))

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
        fingerprint = getval("fingerprint", data)

        # Debug
        log("demosubmit called with: "+str(data))

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
        fingerprint = getval("fingerprint", data)

        # Debug
        log("yourresults called with: "+str(data))

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
        seqsince = ''.join(query.getallsequences(db, self.last))
        log("Since sequence "+str(self.last)+" we have had the following new sequences entered: "+str(seqsince))

        # Only perform the renderings if there is new data to render for.
        if last > self.last and len(seqsince) > 0:
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
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--dbhost', dest='dbhost', type=str, default=None, help="Specify the hostname or IP address of the MySQL server.")
    parser.add_argument('--nofork', action='store_true', help="Do not fork.")
    args = parser.parse_args()

    # Daemonize
    if not args.nofork:
        pid = daemon.become(close_stderr=False)

    pwent = pwd.getpwnam(config.get('user'))
    uid = pwent.pw_uid
    homedir = pwent.pw_dir
    gid = grp.getgrnam(config.get('group')).gr_gid

    cp = ConfigParser.ConfigParser()
    cp.read([os.path.expanduser(homedir+'/.my.cnf')])
    credentials = {'user': cp.get('mysql', 'user'),
                   'passwd': cp.get('mysql', 'password'),
                   'host': cp.get('mysql', 'host')}

    if args.dbhost is not None:
        credentials['host'] = args.dbhost

    # Test the database connection (an exception will be raised if this fails).
    db = MySQLdb.connect(credentials['host'], credentials['user'], credentials['passwd'], 'hrse')
    db.close()

    dp = DropPrivileges(cherrypy.engine, uid=uid, gid=gid)
    dp.subscribe()

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


