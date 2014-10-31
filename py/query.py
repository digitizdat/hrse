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
from data import getval
import time
from cherrypy import log
import config


def boolconv(val):
    """Convert a Python boolean value to its corresponding MySQL value."""
    if val is True:
        return 1

    return 0


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


def dictlistquery(conn, statement, args=None):
    """Execute a SQL statement and return a list of dictionary results, where
    each dictionary is keyed by field name.

    """
    retval = None

    c = conn.cursor()
    res = c.execute(statement, args)

    if res is not None:
        desc = c.description
        retval = []
        for line in c.fetchall():
            tmpdict = {}
            for i in xrange(len(desc)):
                tmpdict[desc[i][0]] = line[i]

            retval.append(tmpdict)

    c.close()
    return retval


def strquery(conn, statement, args=None):
    """Execute a SQL statement and return the first result or None."""
    c = conn.cursor()
    rc = c.execute(statement, args)
    if rc == 0:
        retval = None
    else:
        retval = c.fetchone()[0]
    c.close()
    return retval


def intquery(conn, statement, args=None):
    """Execute a SQL statement and return the first result or None."""
    c = conn.cursor()
    rc = c.execute(statement, args)
    if rc == 0:
        retval = None
    else:
        retval = int(c.fetchone()[0])
    c.close()
    return retval

 
def intlistquery(conn, statement, args=None):
    """Execute a SQL statement and return a list of results or None."""
    c = conn.cursor()
    rc = c.execute(statement, args)
    if rc == 0:
        retval = None
    else:
        retval = [int(x[0]) for x in c.fetchall()]
    c.close()
    return retval


def strlistquery(conn, statement, args=None):
    """Execute a SQL statement and return a list of results or None."""
    c = conn.cursor()
    rc = c.execute(statement, args)
    if rc == 0:
        retval = []
    else:
        retval = [x[0] for x in c.fetchall()]
    c.close()
    return retval


def startsequence(conn, fingerprint, useragent, screenwidth):
    """Insert a new sequence into the database."""
    c = conn.cursor()
    c.execute("insert into sequences (fingerprint, sequence, useragent, screenwidth) " \
      + "values (%s, %s, %s, %s)", (fingerprint, '', useragent, screenwidth))
    c.close()

    idlist = intlistquery(conn, "select idsequences from sequences where " \
      + "fingerprint=%s", (fingerprint,))
    mostrecent = idlist[len(idlist)-1]

    conn.commit()

    return mostrecent


def updatesequence(conn, sequence, seqid, keyboard, mouse, touch, starttime,
                   firstchartime, lastchartime, tbcmax, tbcmin, tbcmean,
                   tbcmedian, tbcrange, tbcstdev, tbcsumsqrd, tbcsumsqerr,
                   tbcmeansqerr, tbcgeomean, tbcvariance, tbccoeffvar,
                   endtime):
    """Update the sequence identified by seqid with the given sequence."""
    if sequence == '':
        log("updatesequence: sequence was empty. returning.")
        return

    # If the sequence to be submitted is shorter than the one already in
    # there, ignore this update.
    if len(sequence) < len(getseqbyid(conn, seqid)):
        log("updatesequence: ignoring shorter sequence.")
        return

    sql = "update sequences set sequence=%s"
    args = (sequence,)

    sql += ", keyboard=%s"
    args += (boolconv(keyboard),)

    sql += ", mouse=%s"
    args += (boolconv(mouse),)

    sql += ", touch=%s"
    args += (boolconv(touch),)

    sql += ", starttime=%s"
    args += (str(starttime),)

    sql += ", firstchartime=%s"
    args += (str(firstchartime),)

    sql += ", lastchartime=%s"
    args += (str(lastchartime),)

    sql += ", tbcmax=%s"
    args += (str(tbcmax),)

    sql += ", tbcmin=%s"
    args += (str(tbcmin),)

    sql += ", tbcmean=%s"
    args += (str(tbcmean),)

    sql += ", tbcmedian=%s"
    args += (str(tbcmedian),)

    sql += ", tbcrange=%s"
    args += (str(tbcrange),)

    sql += ", tbcstdev=%s"
    args += (str(tbcstdev),)

    sql += ", tbcsumsqrd=%s"
    args += (str(tbcsumsqrd),)

    sql += ", tbcsumsqerr=%s"
    args += (str(tbcsumsqerr),)

    sql += ", tbcmeansqerr=%s"
    args += (str(tbcmeansqerr),)

    sql += ", tbcgeomean=%s"
    args += (str(tbcgeomean),)

    sql += ", tbcvariance=%s"
    args += (str(tbcvariance),)

    sql += ", tbccoeffvar=%s"
    args += (str(tbccoeffvar),)

    sql += ", endtime=%s"
    args += (str(endtime),)

    sql += " where idsequences=%s"
    args += (seqid,)

    c = conn.cursor()
    c.execute(sql, args)
    c.close()
    conn.commit()

    return


def createparticipant(conn, fingerprint, referrer='', prevpid=None):
    """Create a participant record"""
    try:
        id = int(prevpid)
    except ValueError:
        id = None
        pass

    oid = getparticipantid(conn, fingerprint)
    c = conn.cursor()

    if id is None:  # Then there was no cookie.
        log("createparticipant: No cookie detected for fingerprint "+str(fingerprint))
        if oid is None:  # No record matching fingerprint was found
            log("createparticipant: (A) Creating a new participant record for fingerprint "+str(fingerprint))
            try:
                rc = c.execute("insert into participant (fingerprint, referrer) " \
                  + "values (%s, %s)", (fingerprint, referrer))
            except MySQLdb.IntegrityError, v:
                log("createparticipant: MySQLdb error occurred while inserting a new participant record (2) for fingerprint "+str(fingerprint))
                raise MySQLdb.IntegrityError, v

    elif oid == id:  # The cookie and the id in the record found via the fingerprint match.
        log("createparticipant: This user already exists with this fingerprint.")

    elif oid is None:  # There was a cookie, but the fingerprint has changed.
        log("createparticipant: The fingerprint has changed for participant "+str(id))
        log("createparticipant: (B) Creating a new participant record for fingerprint "+str(fingerprint))
        try:
            rc = c.execute("insert into participant (fingerprint, referrer, original_id) " \
              + "values (%s, %s, %s)", (fingerprint, referrer, id))
        except MySQLdb.IntegrityError, v:
            log("createparticipant: MySQLdb error occurred while inserting a new participant record (1) for fingerprint "+str(fingerprint))
            raise MySQLdb.IntegrityError, v

    c.close()
    conn.commit()

    # Return the original ID, if possible.
    if id is not None and oid is not None and oid != id:
        log("createparticipant: The cookie ("+str(id)+") seems to be forged, " \
          + "because the fingerprint ("+str(fingerprint)+") matches a " \
          + "different participant ID ("+str(oid)+") in the DB.")
        id = oid

    elif id is None and oid is not None:  # The cookie was gone, but we found a participant record matching the fingerprint.
        log("createparticipant: A participant record was located for this fingerprint: "+str(oid))
        id = oid

    elif id is not None and oid is None:  # We created a new record for the new fingerprint, but we'll keep the original ID.
        id = id

    else:
        id = getparticipantid(conn, fingerprint)

    return id


def getparticipantid(conn, fingerprint):
    """Return the participant ID of the participant identified by the given
    fingerprint.

    Returns an integer on success, or None of no such participant record can be
    located.

    """
    oid = intquery(conn, "select original_id from participant where " \
      + "fingerprint=%s", (fingerprint,))
    if oid != 0:
        return oid

    return intquery(conn, "select idparticipant from participant where " \
      + "fingerprint=%s", (fingerprint,))


def getadmittance(conn, participantid):
    """Return the string-formatted date of admittance for the given participant.

    Returns a string on success, or None of no such participant record can be
    located.

    """
    return strquery(conn, "select admitted from participant where " \
      + "idparticipant=%s", (participantid,))


def getsequences(conn, fingerprint):
    """Return a list of dictionaries keyed by 'idsequences' and 'sequence' for
    the given fingerprint.
    
    The returned list will be ordered chronologically, so the most recently
    entered sequence will be last.

    The conn parameter is an open database handle to the server database.

    """
    return dictlistquery(conn, "select idsequences,sequence from sequences " \
      + "where fingerprint=%s", (fingerprint,))


def getseqsbypid(conn, idparticipant):
    """Return a list of dictionaries keyed by 'idsequences' and 'sequence' for
    the given participant ID.
    
    The returned list will be ordered chronologically, so the most recently
    entered sequence will be last.

    The conn parameter is an open database handle to the server database.

    """
    return dictlistquery(conn, "select sequences.idsequences, " \
      + "sequences.sequence, participant.idparticipant from participant " \
      + "inner join sequences on sequences.fingerprint=participant.fingerprint " \
      + "where participant.idparticipant=%s", (idparticipant,))


def getseqbyid(conn, seqid):
    """Return the sequence for sequence ID seqid."""
    return strquery(conn, "select sequence from sequences where " \
      + "idsequences=%s", (seqid,))


def getallsequences(conn, last=None):
    """Return a list of all sequences submitted by all participants.

    If the last parameter is specified, then only the sequences that have been
    submitted since the sequence identified by the idsequences value of last
    will be loaded.

    """
    query = "select sequence from sequences"
    args = None

    if last is not None:
        query += " where idsequences > %s"
        args = (last,)

    return strlistquery(conn, query, args)


def getseqrange(conn, begin=None, end=None):
    """Return a list of sequences, starting with the sequence ID begin and
    ending with the sequence id end.

    If begin is left None, then the list will start with the first sequence ID
    in the database.  If end is left None, then the list will end with the
    last sequence ID.

    Note that if this function is called with only the conn argument, it
    behaves the same as getallsequences with the same argument.

    """
    query = "select sequence from sequences"
    args = ()

    if begin is not None:
        query += " where idsequences >= %s"
        args += begin,

    if begin is not None and end is not None:
        query += " and idsequences <= %s"
        args += end,
    elif end is not None:
        query += " where idsequences <= %s"
        args += end,

    return strlistquery(conn, query, args)


def getlastseqid(conn):
    """Return the latest idsequences value from the sequences table."""
    idlist = intlistquery(conn, "select idsequences from sequences where sequence != ''")

    if idlist is None:
        return None

    return idlist[len(idlist)-1]


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
    try: demodata.update({'handedness': getval("formdata:handed", data)})
    except KeyError: pass
    try: demodata.update({'favcolor': getval("formdata:favcolor", data)})
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
    

