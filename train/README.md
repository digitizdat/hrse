
Notes for Creating a Bogus Training Set
=======================================

Purpose
-------

I need to create a bogus training set to determine if I'm using the ML
algorithms correctly.  I don't have access to five thousand people to
get actual data, and even if I did, I wouldn't know if the algorithms
are working if it turns out that the information I'm seeking cannot be
extracted using the features I'm using.

The assertions I'm inventing here are completely arbitrary, and have nothing to do with any
preconception that I have about what features might actually be related to each
attribute in any way.  They are chosen simply to provide a clear association of features to
attributes.



Methodology
-----------

I am going to invent specific formulas for identifying characteristics about a person.  In order for them
to be most clearly identified by the algorithms, they must not conflict with each other.  I believe that is
to say they must be linearly independent.

For example, let's say that a female consistently enters in 20% more 0s than 1s.  But let's also say that
a right-handed person enters 20% more 1s than 0s.  In this case we have a conflict, because these assumptions
indicate that we cannot identify a right-handed female, so we need to avoid this condition in order to
create a test set that provides the most clear results.

Similarly, and in the sense of linear independence, let's say we're taking the Boolean values of keyboard
for sex (True -> male) and mouse for handedness (True -> right).  Then we cannot take the logical AND of
(keyboard && mouse) for military service, because that would mean that we could only have right-handed males
for military service.

All of the participant attributes are outputs.  The sequence-related features are inputs.  All of those are
listed below.

For each participant attribute, there are a number of discrete values.


Participant attributes
----------------------
* age
* sex
* handedness
* favcolor
* curzip
* enoughhours
* superpower
* residence
* family
* pets
* maritalstatus
* military
* education


Sequence-related Features
-------------------------
* features of the actual sequence (ngrams, length, etc.)
* keyboard
* mouse
* touch
* starttime
* firstchartime
* lastchartime
* endtime
* maxtimebetweenchars
* mintimebetweenchars
* avgtimebetweenchars


Assertions
----------
* **Age**
    * *These attributes will be determined by sequence length*
    * (1 - 11): Under 12
    * (12 - 17): 12-17 years old
    * (18 - 24): 18-24 years old
    * (25 - 34): 25-34 years old
    * (35 - 44): 35-44 years old
    * (45 - 54): 45-54 years old
    * (55 - 64): 55-64 years old
    * (75+): 75 years or older
* **Sex**
    * *These attributes will be determined by whether there is an even or odd number of characters in the sequence.*
    * (odd): Male
    * (even): Female
* **Handedness**
    * *These attributes will be determined by (endtime - starttime)
    * (< 30000) Right
    * (>= 30000) Left
* **Favorite color**
    * *These attributes will be determined by the average time between chars.*
    * (1 - 120) Red
    * (120 - 140) Orange
    * (140 - 160) Yellow
    * (160 - 180) Green
    * (180 - 200) Blue
    * (200 - 240) Purple
    * (240 - 280) Pink
    * (280 - 320) Brown
    * (320 - 400) Black
    * (400+) White
* **Current Zipcode**
    * *This could be anything.  (It's a bad attribute.  We should kick it out.)*
* **Are there enough hours in the day?**
    * *These attributes will be determined by touch*
    * (True) Yes
    * (False) No
* **Most desired superpower**
    * *These attributes will be determined by maxtimebetweenchars*
    * (1 - 200) Flight
    * (200 - 400) Teleportation
    * (400 - 300) Invisibility
    * (600 - 300) Super fast healing
    * (800 - 300) Super strength
    * (1000 - 1500) Mind reading
    * (1500 - 2000) Mind control
    * (2000 - 2500) Super intelligence
    * (2500 - 3000) Time travel
    * (3000+) Time freeze
* **How many people in your residence?**
    * *These attributes will be determined by mintimebetweenchars*
    * *We'll need to categorize this down into four or five bins, plus there should be "Commune", "Dorm", and "Barracks" options.*
        * *Or maybe we should just ask if the person lives alone, with immediate family, or in a commune, dorm, or barracks.*
        * *Then the questions Do you live with your children? and Do you live with your parents? need to be asked, which makes the 'family' question below rather irrelevant.*
    * (1-10) 1
    * (10-20) 2
    * (20-30) 3-4
    * (30-40) 5-6
    * (40-50) 7-8
    * (50-60) 9-10
    * (60+) 11+
* **Family**
    * *These attributes will be determined by keyboard*
    * (True) Yes
    * (False) No
* **Pets**
    * *These attributes will be determined by mouse (get it?)*
    * (True) Yes
    * (False) No
* **Marital Status**
    * *These attributes will be determined by (firsttime - starttime)*
    * (1-1000) Single, never married
    * (1000-5000) Married
    * (5000-10000) Divorced
    * (10000-20000) Widowed
    * (20000-30000) Civil union
    * (30000-40000) Domestic Partnership
    * (40000-50000) Separated
    * (50000+) Cohabitating
* **Military service**
    * *These attributes will be determined by (endtime - lastchartime)*
    * (1 <= n < 3000) Yes
    * (>= 3000) No
* **Education level**
    * *These attributes will be determined by (lastchartime - firstchartime)*
    * (1-1000) No schooling completed
    * (1000-5000) Completed up to 8th grade
    * (5000-10000) High school graduate, diploma, or the equivalent
    * (10000-20000) Some college credit, no degree
    * (20000-30000) Trade/Tech/Vocactional training
    * (30000-40000) Associate degree
    * (40000-50000) Bachelor's degree
    * (50000-60000) Master's degree
    * (60000-70000) Professional degree
    * (70000+) Doctorate degree

