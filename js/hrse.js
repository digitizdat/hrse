
    function addzero() {
        seqstring = seqstring.concat("0");
        document.getElementById("sequence").innerHTML="<center>"+seqstring+"</center>";
        jsonstr = JSON.stringify({'sequence': seqstring, 'seqid': sequenceid});
        $.ajax({url: "/updateseq/",
                async: false,
                data: jsonstr,
                contentType: 'application/json',
                type: 'POST'
               });
    }

    function addone() {
        seqstring = seqstring.concat("1");
        document.getElementById("sequence").innerHTML="<center>"+seqstring+"</center>";
        jsonstr = JSON.stringify({'sequence': seqstring, 'seqid': sequenceid});
        $.ajax({url: "/updateseq/",
                async: false,
                data: jsonstr,
                contentType: 'application/json',
                type: 'POST'
               });
    }

    function keystroke(event) {
        keyuser = true;
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

        if (src == origin+"/img/done-100x42.png") {
            document.getElementById("doneimg").src = origin+"/img/done-grey-100x42.png";
        } else if (src == origin+"/img/done-140x58.png") {
            document.getElementById("doneimg").src = origin+"/img/done-grey-140x58.png";
        } else if (src == origin+"/img/done-167x69.png") {
            document.getElementById("doneimg").src = origin+"/img/done-grey-167x69.png";
        } else if (src == origin+"/img/done-grey-100x42.png") {
            document.getElementById("doneimg").src = origin+"/img/done-100x42.png";
        } else if (src == origin+"/img/done-grey-140x58.png") {
            document.getElementById("doneimg").src = origin+"/img/done-140x58.png";
        } else if (src == origin+"/img/done-grey-167x69.png") {
            document.getElementById("doneimg").src = origin+"/img/done-167x69.png";
        }
    }

    function clicksubmitdemo() {
        var src = document.getElementById("submitimg").src;
        var origin = window.location.origin;

        if (src == origin+"/img/submit-100x42.png") {
            document.getElementById("submitimg").src = origin+"/img/submit-grey-100x42.png";
        } else if (src == origin+"/img/submit-140x58.png") {
            document.getElementById("submitimg").src = origin+"/img/submit-grey-140x58.png";
        } else if (src == origin+"/img/submit-167x69.png") {
            document.getElementById("submitimg").src = origin+"/img/submit-grey-167x69.png";
        } else if (src == origin+"/img/submit-grey-100x42.png") {
            document.getElementById("submitimg").src = origin+"/img/submit-100x42.png";
        } else if (src == origin+"/img/submit-grey-140x58.png") {
            document.getElementById("submitimg").src = origin+"/img/submit-140x58.png";
        } else if (src == origin+"/img/submit-grey-167x69.png") {
            document.getElementById("submitimg").src = origin+"/img/submit-167x69.png";
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

    // Submit the sequence, fingerprint, and User-Agent info to the /submit
    // WS, and load the results page.
    function done() {
        mobileuser = false;

        if (navigator.userAgent.match(/mobile/i)) {
            mobileuser = true;
        }

        jsonstr = JSON.stringify({"sequence": seqstring, "fingerprint": fingerprint,
                                  "useragent": navigator.userAgent,"keyuser": keyuser,
                                  "screensize": screen.width, "mobileuser": mobileuser});
        $.ajax({url: "/submit/",
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
          .done(function(data, textStatus, jqXHR) {
              var doc = document.open("text/html", "replace");
              doc.write(data);
              doc.close();
          });
    }

    // Load the fingerprint into the database by calling the /getpid WS, which
    // returns the participant number and the timestamp for when that
    // participant was admitted.  Then write the participant number and the
    // admittance ts to the page at the specified locations.
    function getpid() {
       jsonstr = JSON.stringify({"fingerprint": fingerprint, "useragent": navigator.userAgent});
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

