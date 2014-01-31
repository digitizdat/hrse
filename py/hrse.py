"""hrse

This module provides statistical functions for analyzing the randomness of a
given (e.g. human-generated) sequence of 0s and 1s.

"""

import math
import pygal


def runs(sequence):
    """Calculate the number of runs and the longest run.

    This function returns a tuple of the form (runs, longest_run)

    From Dr. Christopher Wetzel
    (http://faculty.rhodes.edu/wetzel/random/mainbody.html):
    The concept of runs: number and length. A run is a repeated outcome. A run
    is defined as a sequence of repeating heads or tails. A new run occurs
    when a new symbol appears. For example, if 3 flips of a coin produce "HTT,"
    there are two runs: one of length 1--the first H, and one of length 2 --the
    second and third "T." Many people mistakenly think that a random coin toss
    would produce alternating sequences of HTHTHTHT... Although a randomly
    flipped coin might produce this once in a while, it is highly unlikely.
    Failures in randomness could produce too many runs (more than 60) or too
    few (less than 40) in a given sequence, and their length could be either
    too short (less than 4) or too long (more than 10).level 2+3 stats
    digression.
    """
    patterns = {}
    maxlen = 0

    # Take the first character and read until it stops appearing.  That will be
    # the first run.  Log that pattern in the patterns dict.  Then move on to
    # the next pattern, etc.

    origin = 0
    pos = 1

    if len(sequence) == 1:
        return (1, 1)

    while origin < len(sequence):
        c = sequence[origin]
        while pos <= len(sequence)-1 and sequence[pos] == c:
            pos += 1

        pattern = sequence[origin:pos]
        if len(pattern) > maxlen:
            maxlen = len(pattern)

        if pattern in patterns:
            patterns[pattern] += 1
        else:
            patterns.update({pattern: 1})

        origin = pos
        pos += 1

    # To see the actual dictionary of patterns, uncomment this line.
    # print str(patterns)

    return (len(patterns), maxlen)


def serdep(sequence):
    """Calculate the serial dependency ratios and standard error.

    This function returns a tuple of the form
        (P(0 given 0), P(1 given 0), S.E.),
    where these values are described below...


    From Dr. Christopher Wetzel
    (http://faculty.rhodes.edu/wetzel/random/serialdepend.html):
    We express p(H given H) as x/y where y is the number of couplets beginning
    with a head and x is the number of these which have a head in the second
    position.
    P(H given T) is z/w where w is the number of couplets beginning with a
    tail, and z is the number of these which have a head in the second
    position.

    As with the longest run, the tests of significance depend on the
    proportion of heads observed, so the general guidelines used for the other
    levels are not precise.

    You can use the following formula to calculate the standard error (SE) of
    the difference between the conditional probabilities:
        S.E. = \sqrt{\frac{z}{w} \frac{x}{y} (\frac{1}{w} + \frac{1}{y})}

    """
    zgivenz = 0  # zero given zero
    zccount = 0  # zero-led couplets
    zgiveno = 0  # zero given one
    occount = 0  # one-led couplets
    probzgz = 0.0  # probability of zero given zero
    probogz = 0.0  # probability of one given zero
    se = 0.0  # Standard error

    # First a special case
    if len(sequence) == 1:
        return (0, 0, 0)

    # Count the number of 0s that follow 0s.
    for i in range(0, len(sequence)-1):
        if sequence[i] == '0' and sequence[i+1] == '0':
            zgivenz += 1
            zccount += 1
        elif sequence[i] == '1' and sequence[i+1] == '0':
            zgiveno += 1
            occount += 1
        elif sequence[i] == '0':
            zccount += 1
        else:
            occount += 1

    # Calculate P(0 given 0)
    if zccount != 0:
        probzgz = float(zgivenz)/float(zccount)

    # Calculate P(0 given 1)
    if occount != 0:
        probogz = float(zgiveno)/float(occount)

    # Calculate the Standard Error
    if zccount != 0 and occount != 0:
        se = math.sqrt(probzgz*probogz*((1.0/occount)+(1.0/zccount)))

    return (probzgz, probogz, se)


def isserdep(pzgz, pogz, se):
    """Return a boolean value indicating whether or not the given statistics
    indicate serial independence.

    """
    probdiff = math.fabs(pzgz-pogz)
    if probdiff > 2*se:
        return False
    else:
        return True


def genresults(conn, seqstring, fingerprint):
    """Generate a Genshi template that includes the images for all of the
    pygal-generated charts that show the statistical analysis of the given
    participant's sequence.

    The return value is the path to the newly created template.
    """

    (runscount, longest_run) = runs(seqstring)
    (pzgz, pogz, se) = serdep(seqstring)

    # Examine the results of the serial dependency calculations
    serdepbool = isserdep(pzgz, pogz, se)

    return {'headstotails': '/img/hist/somechart.png'}

