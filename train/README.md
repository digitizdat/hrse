
Notes for Creating a Bogus Training Set
=======================================

Purpose
-------

I need to create a bogus training set to determine if I'm using the ML algorithms correctly.  I don't have
access to five thousand people to get actual data, and even if I did, I wouldn't know if the algorithms are
working if it turns out that the information I'm seeking cannot be extracted using the features I'm using.


Methodology
-----------

I am going to invent specific formulas for identifying characteristics about a person.  In order for them
to be most clearly identified by the algorithms, they must not conflict with each other.

For example, let's say that a female consistently enters in 20% more 0s than 1s.  But let's also say that
a right-handed person enters 20% more 1s than 0s.  In this case we have a conflict, because these assumptions
indicate that we cannot identify a right-handed female, so we need to avoid this condition in order to
create a test set that provides the most clear results.


Participant-related Features
----------------------
age
sex
handed
favcolor
curzip
enoughhours
superpower
residence
family
pets
maritalstatus
military
education


Sequence-related Features
-------------------------
features of the actual sequence
keyboard
mouse
touch
starttime
firstchartime
lastchartime
endtime
maxtimebetweenchars
mintimebetweenchars
avgtimebetweenchars



