#
# dbutils.py
#
# Miscellaneous functions that are useful when interfacing with the HRSE
# MySQL databases
#
# January 9, 2014 - Martin McGreal
#

import exceptions
import MySQLdb
from hrse import getval


def field(name, desc):
    """Return the index of the given field (name) from the given table
    description (desc).  The table description is provided by the 'description'
    variable of a MySQLdb cursor.  You need to perform a query on a specific
    table for the description variable to be populated.
    """
    i = 0
    for j in desc:
        if j[0] == name:
            return i
        i += 1

    raise exceptions.LookupError, "Cannot locate a field named "+name+" in the given table description ("+str(desc)+")"


def dictquery(conn, statement, args=None):
    """Execute a SQL statement and return the first result or None.  The
    result is returned in dictionary form, where the dictionary is keyed by
    field name.
    """
    retval = None

    c = conn.cursor()
    c.execute(statement, args)
    res = c.fetchone()

    if res is not None:
        desc = c.description
        retval = {}
        for name in [x[0] for x in desc]:
            retval.update({name: res[field(name, desc)]})

    c.close()
    return retval


def strquery(conn, statement, args):
    """Execute a SQL statement and return the first result or None."""
    c = conn.cursor()
    rc = c.execute(statement, args)
    if rc == 0:
        retval = None
    else:
        retval = c.fetchone()[0]
    c.close()
    return retval


def intquery(conn, statement, args):
    """Execute a SQL statement and return the first result or None."""
    c = conn.cursor()
    rc = c.execute(statement, args)
    if rc == 0:
        retval = None
    else:
        retval = int(c.fetchone()[0])
    c.close()
    return retval

 
def intlistquery(conn, statement, args):
    """Execute a SQL statement and return a list of results or None."""
    c = conn.cursor()
    rc = c.execute(statement, args)
    if rc == 0:
        retval = None
    else:
        retval = [int(x[0]) for x in c.fetchall()]
    c.close()
    return retval


def strlistquery(conn, statement, args):
    """Execute a SQL statement and return a list of results or None."""
    c = conn.cursor()
    rc = c.execute(statement, args)
    if rc == 0:
        retval = None
    else:
        retval = [x[0] for x in c.fetchall()]
    c.close()
    return retval


def insertsequence(conn, fingerprint, sequence, useragent):
    """Insert a new sequence into the database."""
    c = conn.cursor()
    rc = c.execute("insert into sequences (fingerprint, sequence, useragent) " \
      + "values (%s, %s, %s)", (fingerprint, sequence, useragent))
    c.close()
    conn.commit()
    return rc


def createparticipant(conn, fingerprint, useragent):
    """Create a participant record"""
    id = getparticipantid(conn, fingerprint)
    if id is not None:
        print "Participant already exists: "+str(id)
        return id

    c = conn.cursor()
    try:
        rc = c.execute("insert into participant (fingerprint, useragent) " \
          + "values (%s, %s)", (fingerprint, useragent))
    except MySQLdb.IntegrityError, v:
        if v[0] == 1062:
            # Remove this print statement
            print "ERROR: Record for participant "+fingerprint+" already exists.  (This should never happen.)"
            pass
        else:
            raise MySQLdb.IntegrityError, v
    c.close()
    conn.commit()
    id = getparticipantid(conn, fingerprint)
    return id


def getparticipantid(conn, fingerprint):
    """Return the ID (primary key) of the named server.

    The conn parameter is an open database handle to the server database, and
    name is the name of the server.

    """
    return intquery(conn, "select idparticipant from participant where " \
      + "fingerprint=%s", (fingerprint,))


def getadmittance(conn, participantid):
    """Return the string-formatted date of admittance for the given participant.

    The conn parameter is an open database handle to the server database, and
    name is the name of the server.

    """
    return strquery(conn, "select admitted from participant where " \
      + "idparticipant=%s", (participantid,))

def getsequences(conn, fingerprint):
    """Return a list of sequences entered by the participant.
    
    The participant is identified by his/her browser fingerprint. The returned
    list will be ordered chronologically, so the most recently entered
    sequence will be last.

    The conn parameter is an open database handle to the server database, and
    name is the name of the server.

    """
    return strlistquery(conn, "select sequence from sequences where " \
      + "fingerprint=%s", (fingerprint,))

def getallsequences(conn):
    """Return a list of all sequences submitted by all participants.
    
    The conn parameter is an open database handle to the server database, and
    name is the name of the server.

    """
    return strlistquery(conn, "select sequence from sequences", None)

def getparticipantinfo(conn, participantid):
    """Return a dictionary populated with any demographic information that we
    can muster.
    
    Any field that has been not yet been provided by the participant is left
    out of the dictionary, such that if no demographic information has yet
    been provided by the participant, this function will return an empty
     dictionary.

    """
    results = {}

    lres = dictquery(conn, "select * from participant where idparticipant=%s",
    (participantid,))

    if lres is None:
        return results

    print "getparticipantinfo() returned "+str(lres)
    for entry in lres:
        if lres[entry] is not None:
            results.update({entry: lres[entry]})

    return results

def submitdemo(conn, participantid, data):
    """Insert whatever demographic data has been supplied in the demodata
    dictionary.

    """
    demodata = {}

    # Create a dictionary of demographic data that were provided by the participant
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

    print "submitdemo(): demodata: "+str(demodata)

    if len(demodata) == 0:
        return

    c = conn.cursor()
    for key in demodata.keys():
        rc = c.execute("update participant set "+key+"=" \
          + "%s where idparticipant=%s", (demodata[key], participantid))
    c.close()
    conn.commit()
    return rc
    

