// Highlight.js:
if (window.require) {
    require(["highlight.js"], function () {
        //This function is called after some/script.js has loaded.
    });
} else {
    document.write('<script src=Screenshot/highlight.js></script>');
}

var link = document.createElement("link");
link.type = "text/css";
link.rel = "stylesheet";
link.href = "./Screenshot/highlight.css";
document.getElementsByTagName("head")[0].appendChild(link);

/* Copyright (C) 1998-2016 by Northwoods Software Corporation. All Rights Reserved. */

function goSamples() {
    // save the body for goViewSource() before we modify it
    window.bodyHTML = document.body.innerHTML;
    window.bodyHTML = window.bodyHTML.replace(/</g, "&lt;");
    window.bodyHTML = window.bodyHTML.replace(/>/g, "&gt;");

    // look for links to API documentation and convert them
    _traverseDOM(document);
}
    
function _traverseDOM(node) {
    if (node.nodeType === 1 && node.nodeName === "A" && !node.getAttribute("href")) {
        var text = node.innerHTML.split(".");
        if (text.length === 1) {
            node.setAttribute("href", "../api/symbols/" + text[0] + ".html");
            node.setAttribute("target", "api");
        } else if (text.length === 2) {
            node.setAttribute("href", "../api/symbols/" + text[0] + ".html" + "#" + text[1]);
            node.setAttribute("target", "api");
        } else {
            alert("Unknown API reference: " + node.innerHTML);
        }
    }
    for (var i = 0; i < node.childNodes.length; i++) {
        _traverseDOM(node.childNodes[i]);
    }
}

function goViewSource() {
    // show the code:
    var script = document.getElementById("code");
    if (!script) {
        var scripts = document.getElementsByTagName("script");
        script = scripts[scripts.length - 1];
    }
    var sp1 = document.createElement("pre");
    sp1.setAttribute("class", "javascript");
    sp1.innerHTML = script.innerHTML;
    var samplediv = document.getElementById("sample") || document.body;
    samplediv.appendChild(sp1);

    // show the body:
    var sp2 = document.createElement("pre");
    sp2.innerHTML = window.bodyHTML;
    samplediv.appendChild(sp2);

    window.hdr.children[0].style.display = "none"; // hide the "View Source" link

    // apply formatting
    hljs.highlightBlock(sp1);
    hljs.highlightBlock(sp2);
    window.scrollBy(0, 100);
}

(function (i, s, o, g, r, a, m) {
    i['GoogleAnalyticsObject'] = r; i[r] = i[r] || function () {
        (i[r].q = i[r].q || []).push(arguments)
    }, i[r].l = 1 * new Date(); a = s.createElement(o),
    m = s.getElementsByTagName(o)[0]; a.async = 1; a.src = g; m.parentNode.insertBefore(a, m)
})(window, document, 'script', 'https://www.google-analytics.com/analytics.js', 'ga');

ga('create', 'UA-1506307-5', 'auto');
ga('send', 'pageview');

