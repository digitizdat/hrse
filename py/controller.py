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
        demodata = formvars(query.getparticipantinfo(db, id))

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
        try: demodata.update({'age': getval("formdata:age", data)})
        except KeyError: pass
        try: demodata.update({'sex': getval("formdata:sex", data)})
        except KeyError: pass
        try: demodata.update({'handed': getval("formdata:handed", data)})
        except KeyError: pass
        try: demodata.update({'favcolor': getval("formdata:favcolor", data)})
        except KeyError: pass
        try: demodata.update({'curzip': getval("formdata:curzip", data)})
        except KeyError: pass
        try: demodata.update({'enoughhours': getval("formdata:enoughhours", data)})
        except KeyError: pass
        try: demodata.update({'superpower': getval("formdata:superpower", data)})
        except KeyError: pass
        try: demodata.update({'residence': getval("formdata:residence", data)})
        except KeyError: pass
        try: demodata.update({'family': getval("formdata:family", data)})
        except KeyError: pass
        try: demodata.update({'pets': getval("formdata:pets", data)})
        except KeyError: pass
        try: demodata.update({'maritalstatus': getval("formdata:maritalstatus", data)})
        except KeyError: pass
        try: demodata.update({'military': getval("formdata:military", data)})
        except KeyError: pass
        try: demodata.update({'education': getval("formdata:education", data)})
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


def formvars(data):
    """Return a dictionary of variables for use with the myinfo.html template

    """

    # Initialize all the form variables to empty strings.
    results = {
      'age_lt12': '',
      'age_lt18': '',
      'age_lt25': '',
      'age_lt35': '',
      'age_lt45': '',
      'age_lt55': '',
      'age_lt65': '',
      'age_ge75': '',
      'sex_m': '',
      'sex_f': '',
      'handed_l': '',
      'handed_r': '',
      'color_red': '',
      'color_orange': '',
      'color_yellow': '',
      'color_green': '',
      'color_blue': '',
      'color_purple': '',
      'color_pink': '',
      'color_brown': '',
      'color_black': '',
      'color_white': '',
      'curzip': '',
      'enoughhours_y': '',
      'enoughhours_n': '',
      'suppow_flight': '',
      'suppow_telep': '',
      'suppow_invis': '',
      'suppow_healing': '',
      'suppow_strength': '',
      'suppow_mindre': '',
      'suppow_mindco': '',
      'suppow_mindco': '',
      'suppow_intel': '',
      'suppow_timetrav': '',
      'suppow_timefrez': '',
      'residence': '',
      'family_y': '',
      'family_n': '',
      'pets_y': '',
      'pets_n': '',
      'mari_single': '',
      'mari_married': '',
      'mari_divorced': '',
      'mari_widowed': '',
      'mari_civunion': '',
      'mari_dompart': '',
      'mari_separated': '',
      'mari_cohab': '',
      'military_y': '',
      'military_n': '',
      'edu_none': '',
      'edu_elem': '',
      'edu_hs': '',
      'edu_somecol': '',
      'edu_trade': '',
      'edu_assoc': '',
      'edu_under': '',
      'edu_master': '',
      'edu_prof': '',
      'edu_doctor': ''}


    if data['age'] == 'lt12': results['age_lt12'] = 'selected'
    elif data['age'] == 'lt18': results['age_lt18'] = 'selected'
    elif data['age'] == 'lt25': results['age_lt25'] = 'selected'
    elif data['age'] == 'lt35': results['age_lt35'] = 'selected'
    elif data['age'] == 'lt45': results['age_lt45'] = 'selected'
    elif data['age'] == 'lt55': results['age_lt55'] = 'selected'
    elif data['age'] == 'lt65': results['age_lt65'] = 'selected'
    elif data['age'] == 'ge75': results['age_ge75'] = 'selected'

    if data['sex'] == 'male': results['sex_m'] = 'checked'
    elif data['sex'] == 'female': results['sex_f'] = 'checked'

    if data['handed'] == 'left': results['handed_l'] = 'checked'
    elif data['handed'] == 'right': results['handed_r'] = 'checked'

    if data['favcolor'] == 'red': results['color_red'] = 'selected'
    elif data['favcolor'] == 'orange': results['color_orange'] = 'selected'
    elif data['favcolor'] == 'yellow': results['color_yellow'] = 'selected'
    elif data['favcolor'] == 'green': results['color_green'] = 'selected'
    elif data['favcolor'] == 'blue': results['color_blue'] = 'selected'
    elif data['favcolor'] == 'purple': results['color_purple'] = 'selected'
    elif data['favcolor'] == 'pink': results['color_pink'] = 'selected'
    elif data['favcolor'] == 'brown': results['color_brown'] = 'selected'
    elif data['favcolor'] == 'black': results['color_black'] = 'selected'
    elif data['favcolor'] == 'white': results['color_white'] = 'selected'

    if data['curzip'] != 'na': results['curzip'] = data['curzip']

    if data['enoughhours'] == 'yes': results['enoughhours_y'] = 'checked'
    elif data['enoughhours'] == 'no': results['enoughhours_n'] = 'checked'

    if data['superpower'] == 'flight': results['suppow_flight'] = 'selected'
    elif data['superpower'] == 'teleport': results['suppow_telep'] = 'selected'
    elif data['superpower'] == 'invisible': results['suppow_invis'] = 'selected'
    elif data['superpower'] == 'healing': results['suppow_healing'] = 'selected'
    elif data['superpower'] == 'strength': results['suppow_strength'] = 'selected'
    elif data['superpower'] == 'mindre': results['suppow_mindre'] = 'selected'
    elif data['superpower'] == 'mindco': results['suppow_mindco'] = 'selected'
    elif data['superpower'] == 'intelligence': results['suppow_intel'] = 'selected'
    elif data['superpower'] == 'timetravel': results['suppow_timetrav'] = 'selected'
    elif data['superpower'] == 'timefreeze': results['suppow_timefrez'] = 'selected'

    if data['residence'] != 'na': results['residence'] = data['residence']

    if data['family'] == 'yes': results['family_y'] = 'checked'
    elif data['family'] == 'no': results['family_n'] = 'checked'

    if data['pets'] == 'yes': results['pets_y'] = 'checked'
    elif data['pets'] == 'no': results['pets_n'] = 'checked'

    if data['maritalstatus'] == 'single': results['mari_single'] = 'selected'
    elif data['maritalstatus'] == 'married': results['mari_married'] = 'selected'
    elif data['maritalstatus'] == 'divorced': results['mari_divorced'] = 'selected'
    elif data['maritalstatus'] == 'widowed': results['mari_widowed'] = 'selected'
    elif data['maritalstatus'] == 'civunion': results['mari_civunion'] = 'selected'
    elif data['maritalstatus'] == 'dompart': results['mari_dompart'] = 'selected'
    elif data['maritalstatus'] == 'separated': results['mari_separated'] = 'selected'
    elif data['maritalstatus'] == 'cohab': results['mari_cohab'] = 'selected'

    if data['military'] == 'yes': results['military_y'] = 'checked'
    elif data['military'] == 'no': results['military_n'] = 'checked'

    if data['education'] == 'none': results['edu_none'] = 'selected'
    elif data['education'] == 'elementary': results['edu_elem'] = 'selected'
    elif data['education'] == 'hs': results['edu_hs'] = 'selected'
    elif data['education'] == 'somecol': results['edu_somecol'] = 'selected'
    elif data['education'] == 'trade': results['edu_trade'] = 'selected'
    elif data['education'] == 'assoc': results['edu_assoc'] = 'selected'
    elif data['education'] == 'under': results['edu_under'] = 'selected'
    elif data['education'] == 'master': results['edu_master'] = 'selected'
    elif data['education'] == 'prof': results['edu_prof'] = 'selected'
    elif data['education'] == 'doctor': results['edu_doctor'] = 'selected'

    return results


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

