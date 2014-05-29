

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


