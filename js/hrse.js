
// AJAX call management pool
$.xhrPool = [];
$.xhrPool.abortAll = function() {
    $(this).each(function(idx, jqXHR) {
        jqXHR.abort();
    });
    $.xhrPool = [];
};

$.ajaxSetup({
    beforeSend: function(jqXHR) {
        $.xhrPool.push(jqXHR);
    },
    complete: function(jqXHR) {
        var index = $.xhrPool.indexOf(jqXHR);
        if (index > -1) {
            $.xhrPool.splice(index, 1);
        }
    }
});



// Functions

    function rendersequence(s) {
        if (screen.width <= 320) {
            document.getElementById("sequence1").innerHTML="<center>"+s.slice(0,40)+"</center>";
            document.getElementById("sequence2").innerHTML="<center>"+s.slice(40,80)+"</center>";
            document.getElementById("sequence3").innerHTML="<center>"+s.slice(80,120)+"</center>";
            document.getElementById("sequence4").innerHTML="<center>"+s.slice(120,s.length)+"</center>";
        } else {
            document.getElementById("sequence1").innerHTML="<center>"+s.slice(0,80)+"</center>";
            document.getElementById("sequence2").innerHTML="<center>"+s.slice(80,160)+"</center>";
            document.getElementById("sequence3").innerHTML="<center>"+s.slice(160,240)+"</center>";
            document.getElementById("sequence4").innerHTML="<center>"+s.slice(240,s.length)+"</center>";
        }
    }

    function addzero() {
        // First priority: update the interface
        seqstring = seqstring.concat("0");
        rendersequence(seqstring);

        // If this is is the first character, calculate the difference between
        // the start and finish time.
        if (firstchartime == 0) {
            fctime = new Date();
            firstchartime = fctime.getTime();
            inittime = firstchartime-starttime;
        }

        // Update the sequence in the database
        jsonstr = JSON.stringify({'sequence': seqstring, 'seqid': sequenceid,
                                  'inittime': inittime, 'keyboard': keyey,
                                  'mouse': mousey, 'touch': touchy});
        $.ajax({url: "/updateseq/",
                async: true,
                data: jsonstr,
                contentType: 'application/json',
                type: 'POST'
               });
    }

    function addone() {
        // First priority: update the interface
        seqstring = seqstring.concat("1");
        rendersequence(seqstring);

        // If this is is the first character, calculate the difference between
        // the start and finish time.
        if (firstchartime == 0) {
            fctime = new Date();
            firstchartime = fctime.getTime();
            inittime = firstchartime-starttime;
        }

        // Update the sequence in the database
        jsonstr = JSON.stringify({'sequence': seqstring, 'seqid': sequenceid,
                                  'inittime': inittime, 'keyboard': keyey,
                                  'mouse': mousey, 'touch': touchy});
        $.ajax({url: "/updateseq/",
                async: true,
                data: jsonstr,
                contentType: 'application/json',
                type: 'POST'
               });
    }

    function keystroke(event) {
        if (event.keyCode == 48) {
            addzero();
        }
        if (event.keyCode == 49) {
            addone();
        }
    }

    function clickzero() {
        var src = document.getElementById("updatezero").src;
        var origin = window.location.origin;

        if (src == origin+"/img/0-white-small.png") {
            document.getElementById("updatezero").src = origin+"/img/0-grey-small.png";
        } else if (src == origin+"/img/0-white-med.png") {
            document.getElementById("updatezero").src = origin+"/img/0-grey-med.png";
        } else if (src == origin+"/img/0-white-large.png") {
            document.getElementById("updatezero").src = origin+"/img/0-grey-large.png";
        } else if (src == origin+"/img/0-white-huge.png") {
            document.getElementById("updatezero").src = origin+"/img/0-grey-huge.png";
        } else if (src == origin+"/img/0-grey-small.png") {
            document.getElementById("updatezero").src = origin+"/img/0-white-small.png";
        } else if (src == origin+"/img/0-grey-med.png") {
            document.getElementById("updatezero").src = origin+"/img/0-white-med.png";
        } else if (src == origin+"/img/0-grey-large.png") {
            document.getElementById("updatezero").src = origin+"/img/0-white-large.png";
        } else if (src == origin+"/img/0-grey-huge.png") {
            document.getElementById("updatezero").src = origin+"/img/0-white-huge.png";
        }
    }

    function clickone() {
        var src = document.getElementById("updateone").src;
        var origin = window.location.origin;

        if (src == origin+"/img/1-black-small.png") {
            document.getElementById("updateone").src = origin+"/img/1-grey-small.png";
        } else if (src == origin+"/img/1-black-med.png") {
            document.getElementById("updateone").src = origin+"/img/1-grey-med.png";
        } else if (src == origin+"/img/1-black-large.png") {
            document.getElementById("updateone").src = origin+"/img/1-grey-large.png";
        } else if (src == origin+"/img/1-black-huge.png") {
            document.getElementById("updateone").src = origin+"/img/1-grey-huge.png";
        } else if (src == origin+"/img/1-grey-small.png") {
            document.getElementById("updateone").src = origin+"/img/1-black-small.png";
        } else if (src == origin+"/img/1-grey-med.png") {
            document.getElementById("updateone").src = origin+"/img/1-black-med.png";
        } else if (src == origin+"/img/1-grey-large.png") {
            document.getElementById("updateone").src = origin+"/img/1-black-large.png";
        } else if (src == origin+"/img/1-grey-huge.png") {
            document.getElementById("updateone").src = origin+"/img/1-black-huge.png";
        }
    }

    function clickdone() {
        var src = document.getElementById("doneimg").src;
        var origin = window.location.origin;

        if (src == origin+"/img/done-blue-100x42.png") {
            document.getElementById("doneimg").src = origin+"/img/done-dark-100x42.png";
        } else if (src == origin+"/img/done-blue-140x58.png") {
            document.getElementById("doneimg").src = origin+"/img/done-dark-140x58.png";
        } else if (src == origin+"/img/done-blue-167x70.png") {
            document.getElementById("doneimg").src = origin+"/img/done-dark-167x70.png";
        } else if (src == origin+"/img/done-dark-100x42.png") {
            document.getElementById("doneimg").src = origin+"/img/done-blue-100x42.png";
        } else if (src == origin+"/img/done-dark-140x58.png") {
            document.getElementById("doneimg").src = origin+"/img/done-blue-140x58.png";
        } else if (src == origin+"/img/done-dark-167x70.png") {
            document.getElementById("doneimg").src = origin+"/img/done-blue-167x70.png";
        }
    }

    function clicksubmitdemo() {
        var src = document.getElementById("submitimg").src;
        var origin = window.location.origin;

        if (src == origin+"/img/submit-blue-100x42.png") {
            document.getElementById("submitimg").src = origin+"/img/submit-dark-100x42.png";
        } else if (src == origin+"/img/submit-blue-140x58.png") {
            document.getElementById("submitimg").src = origin+"/img/submit-dark-140x58.png";
        } else if (src == origin+"/img/submit-blue-167x69.png") {
            document.getElementById("submitimg").src = origin+"/img/submit-dark-167x69.png";
        } else if (src == origin+"/img/submit-dark-100x42.png") {
            document.getElementById("submitimg").src = origin+"/img/submit-blue-100x42.png";
        } else if (src == origin+"/img/submit-dark-140x58.png") {
            document.getElementById("submitimg").src = origin+"/img/submit-blue-140x58.png";
        } else if (src == origin+"/img/submit-dark-167x69.png") {
            document.getElementById("submitimg").src = origin+"/img/submit-blue-167x69.png";
        }
    }

    function clickyourrelatives() {
        var src = document.getElementById("yourrelimg").src;
        var origin = window.location.origin;

        if (src == origin+"/img/yourrelatives-126x33.png") {
            document.getElementById("yourrelimg").src = origin+"/img/yourrelatives-grey-126x33.png";
        } else if (src == origin+"/img/yourrelatives-grey-126x33.png") {
            document.getElementById("yourrelimg").src = origin+"/img/yourrelatives-126x33.png";
        }
    }

    function clickoverallstats() {
        var src = document.getElementById("overallstatsimg").src;
        var origin = window.location.origin;

        if (src == origin+"/img/overallstats-126x33.png") {
            document.getElementById("overallstatsimg").src = origin+"/img/overallstats-grey-126x33.png";
        } else if (src == origin+"/img/overallstats-grey-126x33.png") {
            document.getElementById("overallstatsimg").src = origin+"/img/overallstats-126x33.png";
        }
    }

    function clickabout() {
        var src = document.getElementById("aboutimg").src;
        var origin = window.location.origin;

        if (src == origin+"/img/about-126x33.png") {
            document.getElementById("aboutimg").src = origin+"/img/about-grey-126x33.png";
        } else if (src == origin+"/img/about-grey-126x33.png") {
            document.getElementById("aboutimg").src = origin+"/img/about-126x33.png";
        }
    }

    function clickyourinfo() {
        var src = document.getElementById("yourinfoimg").src;
        var origin = window.location.origin;

        if (src == origin+"/img/yourinfo-126x33.png") {
            document.getElementById("yourinfoimg").src = origin+"/img/yourinfo-grey-126x33.png";
        } else if (src == origin+"/img/yourinfo-grey-126x33.png") {
            document.getElementById("yourinfoimg").src = origin+"/img/yourinfo-126x33.png";
        }
    }

    function clickyourresults() {
        var src = document.getElementById("yourresultsimg").src;
        var origin = window.location.origin;

        if (src == origin+"/img/yourresults-126x33.png") {
            document.getElementById("yourresultsimg").src = origin+"/img/yourresults-grey-126x33.png";
        } else if (src == origin+"/img/yourresults-grey-126x33.png") {
            document.getElementById("yourresultsimg").src = origin+"/img/yourresults-126x33.png";
        }
    }

    function clicknewsequence() {
        var src = document.getElementById("newseqimg").src;
        var origin = window.location.origin;

        if (src == origin+"/img/newsequence-126x33.png") {
            document.getElementById("newseqimg").src = origin+"/img/newsequence-grey-126x33.png";
        } else if (src == origin+"/img/newsequence-grey-126x33.png") {
            document.getElementById("newseqimg").src = origin+"/img/newsequence-126x33.png";
        }
    }

    // Load the demographic information page.
    function done() {
        // Abort any pending AJAX calls (pending sequence updates)
        $.xhrPool.abortAll();

        // Launch the spinner
        spintarget = document.getElementById("donerow");
        spinner = new Spinner(spinopts).spin(spintarget);

        // Load the next page.
        jsonstr = JSON.stringify({'sequence': seqstring, 'seqid': sequenceid,
                                  'inittime': inittime, 'keyboard': keyey,
                                  'mouse': mousey, 'touch': touchy});
        $.ajax({url: "/endsequence/",
                async: true,
                data: jsonstr,
                contentType: 'application/json',
                type: 'POST'
               })
           .done(yourinfo());
    }

    // Load the demographic information page.
    function yourinfo() {
        jsonstr = JSON.stringify({"fingerprint": fingerprint});
        $.ajax({url: "/yourinfo/",
                async: false,
                data: jsonstr,
                contentType: 'application/json',
                type: 'POST'
               })
           .done(function(data, textStatus, jqXHR) {
               var doc = document.open("text/html", "replace");
               doc.write(data);
               doc.close();
           });
    }

    // Load the participant results page
    function yourresults() {
        jsonstr = JSON.stringify({"fingerprint": fingerprint});
        $.ajax({url: "/yourresults/",
                async: false,
                data: jsonstr,
                contentType: 'application/json',
                type: 'POST'
               })
           .done(function(data, textStatus, jqXHR) {
               var doc = document.open("text/html", "replace");
               doc.write(data);
               doc.close();
           });
    }

    // Load the participant results page
    function overallstats() {
        $.ajax({url: "/overallstats/",
                async: false,
                data: jsonstr,
                contentType: 'application/json',
                type: 'POST'
               })
           .done(function(data, textStatus, jqXHR) {
               var doc = document.open("text/html", "replace");
               doc.write(data);
               doc.close();
           });
    }

    // Load the about page
    function about() {
        $.ajax({url: "/about/",
                async: false,
                data: jsonstr,
                contentType: 'application/json',
                type: 'POST'
               })
           .done(function(data, textStatus, jqXHR) {
               var doc = document.open("text/html", "replace");
               doc.write(data);
               doc.close();
           });
    }

    // I got this a kind of adhoc method that can be attached to an object.  I
    // found it here:
    // http://stackoverflow.com/questions/1184624/convert-form-data-to-js-object-with-jquery
    //
    // It converts the form data into a JSON string.  Demo here:
    // http://jsfiddle.net/sxGtM/3/
    $.fn.serializeObject = function() {
        var o = {};
        var a = this.serializeArray();
        $.each(a, function() {
            if (o[this.name] !== undefined) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return o;
    }

    // Submit the demographic form data, continue on to the results page.
    function submitdemo() {
       jsonstr = JSON.stringify({"formdata": $('form').serializeObject(), "fingerprint": fingerprint});
       $.ajax({url: "/demosubmit/",
               async: false,
               data: jsonstr,
               contentType: 'application/json',
               type: 'POST'
              })
          .done(yourresults());
    }

    // Load the fingerprint into the database by calling the /getpid WS, which
    // returns the participant number and the timestamp for when that
    // participant was admitted.  Then write the participant number and the
    // admittance ts to the page at the specified locations.
    function getpid() {
        mobileuser = false;

        if (navigator.userAgent.match(/mobile/i)) {
            mobileuser = true;
        }

        jsonstr = JSON.stringify({"fingerprint": fingerprint,
                                  "useragent": navigator.userAgent,
                                  "screenwidth": screen.width,
                                  "referrer": document.referrer});
        $.ajax({url: "/getpid/",
                async: false,
                data: jsonstr,
                contentType: 'application/json',
                type: 'POST'
               })
            .done(function(data, textStatus, jqXHR) {
               var jdoc = jQuery.parseJSON(data);
               document.getElementById('pid').innerHTML = jdoc.id;
               document.getElementById('adate').innerHTML = jdoc.date;
               sequenceid = jdoc.seqid;
            });
    }

    // If the screen width is less than 640 pixels, we'll assume it's touch
    // screen capable, so we'll just include the instructions for tapping the
    // 0 and 1 buttons.  It saves space for those smaller devices.
    function stepone() {
        var largetext = "Press 0 and 1 on your keyboard - or click or tap the 0 and 1 buttons below -";
        var smalltext = "Tap the 0 and 1 buttons below";

        if (screen.width < 640) {
            document.getElementById('clicktap').innerHTML = smalltext;
        } else {
            document.getElementById('clicktap').innerHTML = largetext;
        }
    }

