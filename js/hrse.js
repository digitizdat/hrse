
    function addzero() {
        seqstring = seqstring.concat("0");
        document.getElementById("sequence").innerHTML="<center><pre>"+seqstring+"</pre></center>";
    }

    function addone() {
        seqstring = seqstring.concat("1");
        document.getElementById("sequence").innerHTML="<center><pre>"+seqstring+"</pre></center>";
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

    function done() {
       jsonstr = JSON.stringify({"sequence": seqstring, "fingerprint": fingerprint, "useragent": navigator.userAgent})
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

    function getpid() {
       jsonstr = JSON.stringify({"fingerprint": fingerprint})
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
          });
    }

    function stepone() {
        var largetext = "Click or tap the 0 and 1 buttons below - or press 0 and 1 on your keyboard -";
        var smalltext = "Tap the 0 and 1 buttons below";

        if (screen.width < 640) {
            document.getElementById('clicktap').innerHTML = smalltext;
        } else {
            document.getElementById('clicktap').innerHTML = largetext;
        }
    }

