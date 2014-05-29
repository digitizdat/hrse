"""hrse

This module provides statistical functions for analyzing the randomness of a
given (e.g. human-generated) sequence of 0s and 1s.

"""

import os, math
import pygal
from pygal.style import LightGreenStyle
import config, query
from cherrypy import log


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


def genrunlengths(sequence):
    """Return a list of run lengths for the given sequence string."""
    runlengths = []
    results = {}

    if len(sequence) == 0:
        return results

    char = None
    count = 0

    for x in sequence:
        if char is None:
            char = x
            count = 1
        elif x == char:
            count += 1
        else:  # Switching between 0 and 1
            char = x
            runlengths.append(count)
            count = 1

    runlengths.append(count)

    for i in range(1, max(runlengths)+1):
        results.update({str(i): 0})
        for r in runlengths:
            if r == i:
                results.update({str(i): results[str(i)]+1})

    return results


def genresults(sequence, seqid, render=True):
    """Generate a Genshi template that includes the images for all of the
    pygal-generated charts that show the statistical analysis of the given
    participant's sequence.

    The return value is the path to the newly created template.
    """
    (runscount, longest_run) = runs(sequence)
    (pzgz, pogz, se) = serdep(sequence)

    # Examine the results of the serial dependency calculations
    serdepbool = isserdep(pzgz, pogz, se)

    if render:
        imgpaths = renderimages(sequence, seqid)
    else:
        fprefix = '/img/hist/'+str(seqid)
        imgpaths = {'small_zerostoones': fprefix+'-small-zerostoones.png',
                    'large_zerostoones': fprefix+'-large-zerostoones.png',
                    'small_runlengths': fprefix+'-small-runlengths.png',
                    'large_runlengths': fprefix+'-large-runlengths.png',
                    'small_pairs': fprefix+'-small-pairs.png',
                    'large_pairs': fprefix+'-large-pairs.png',
                    'small_triples': fprefix+'-small-triples.png',
                    'large_triples': fprefix+'-large-triples.png'}

    results = {'pzgz': pzgz,
               'pogz': pogz,
               'se': se,
               'serdepbool': serdepbool}
    results.update(imgpaths)

    return results


def renderimages(sequence, seqid):
    """Render the PNG images of the charts for the given sequence.

    The return value is a dictionary of paths for the images, keyed by
    symbolic names.

    The images will not be rendered if they already exist, with the exception
    being if the seqid is 'overall', because the decision on whether to
    re-render the overall images is made outside this function.

    """
    fprefix = '/img/hist/'+str(seqid)

    # Create a bar chart for 0s and 1s counts
    smztopath = config.get('hrsehome')+fprefix+'-small-zerostoones.png'
    lgztopath = config.get('hrsehome')+fprefix+'-large-zerostoones.png'

    if seqid == "overall" or not os.path.exists(smztopath) or not os.path.exists(lgztopath):
        chart = pygal.Bar(width=375, height=400, style=LightGreenStyle)
        chart.title = "Ratio of 0s versus 1s"
        chart.add('Zeros', [sequence.count('0')])
        chart.add('Ones', [sequence.count('1')])
        chart.render_to_png(smztopath)
        chart.config.width = 400
        chart.render_to_png(lgztopath)
    else:
        log("genresults: skipping zto pngs for seqid "+str(seqid))

    # Create a histogram of run lengths
    smrunlengths = config.get('hrsehome')+fprefix+'-small-runlengths.png'
    lgrunlengths = config.get('hrsehome')+fprefix+'-large-runlengths.png'

    if seqid == "overall" or not os.path.exists(smrunlengths) or not os.path.exists(lgrunlengths):
        runlengths = genrunlengths(sequence)
        chart = pygal.Bar(width=375, height=400, style=LightGreenStyle)
        chart.title = "Run lengths"
        chart.x_labels = map(str, range(1, len(runlengths)+1))
        chart.add('Count', [runlengths[str(i)] for i in range(1, len(runlengths)+1)])
        chart.render_to_png(smrunlengths)
        chart.config.width = 400
        chart.render_to_png(lgrunlengths)
    else:
        log("genresults: skipping runlength pngs for seqid "+str(seqid))

    # Create a histogram of '01', '10', '00, '11' distribution
    smpairs = config.get('hrsehome')+fprefix+'-small-pairs.png'
    lgpairs = config.get('hrsehome')+fprefix+'-large-pairs.png'

    if seqid == "overall" or not os.path.exists(smpairs) or not os.path.exists(lgpairs):
        pairs = {'00': sequence.count('00'),
                 '01': sequence.count('01'),
                 '11': sequence.count('11'),
                 '10': sequence.count('10')}
        chart = pygal.Bar(width=375, height=400, style=LightGreenStyle)
        chart.title = "Distribution of pairs"
        chart.x_labels = pairs.keys()
        chart.add('Count', [pairs[i] for i in pairs.keys()])
        chart.render_to_png(smpairs)
        chart.config.width = 400
        chart.render_to_png(lgpairs)
    else:
        log("genresults: skipping pairs pngs for seqid"+str(seqid))


    # Create a histogram of triples: 000, 001, 010, 011, 100, 101, 110, 111
    smtrips = config.get('hrsehome')+fprefix+'-small-triples.png'
    lgtrips = config.get('hrsehome')+fprefix+'-large-triples.png'

    if seqid == "overall" or not os.path.exists(smtrips) or not os.path.exists(lgtrips):
        triples = {'000': sequence.count('000'),
                   '001': sequence.count('001'),
                   '010': sequence.count('010'),
                   '011': sequence.count('011'),
                   '100': sequence.count('100'),
                   '101': sequence.count('101'),
                   '110': sequence.count('110'),
                   '111': sequence.count('111')}
        chart = pygal.Bar(width=375, height=400, style=LightGreenStyle)
        chart.title = "Distribution of triples"
        chart.x_labels = triples.keys()
        chart.add('Count', [triples[i] for i in triples.keys()])
        chart.render_to_png(smtrips)
        chart.config.width = 400
        chart.render_to_png(lgtrips)
    else:
        log("genresults: skipping trips pngs for seqid"+str(seqid))

    return {'small_zerostoones': fprefix+'-small-zerostoones.png',
            'large_zerostoones': fprefix+'-large-zerostoones.png',
            'small_runlengths': fprefix+'-small-runlengths.png',
            'large_runlengths': fprefix+'-large-runlengths.png',
            'small_pairs': fprefix+'-small-pairs.png',
            'large_pairs': fprefix+'-large-pairs.png',
            'small_triples': fprefix+'-small-triples.png',
            'large_triples': fprefix+'-large-triples.png'}

def genfeatures(begin=None, end=None):
    """Create a features table for the given sequence range.

    If begin is None, then the collection will start with the earliest
    sequence ID.

    If end is None, then the collection will end on the most recent sequence
    ID.

    """
    pass
    
