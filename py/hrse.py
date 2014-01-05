"""hrse

This module provides statistical functions for analyzing the randomness of a
given (e.g. human-generated) sequence of 0s and 1s.

"""

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
