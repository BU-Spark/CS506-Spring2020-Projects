

if (Function.prototype.bind == null) {
Function.prototype.bind = function(object) {
var __method = this;
return function() {
return __method.apply(object, arguments);
}
}
}

if (typeof(Wicket) == "undefined")
Wicket = { };

if (typeof(Wicket.Browser) == "undefined") {
Wicket.Browser = {
isKHTML: function() {
return /Konqueror|KHTML/.test(navigator.userAgent) && !/Apple/.test(navigator.userAgent);
},
isSafari: function() {
return /KHTML/.test(navigator.userAgent) && /Apple/.test(navigator.userAgent);
},
isOpera: function() {
return !Wicket.Browser.isSafari() && typeof(window.opera) != "undefined";
},
isIE: function() {
return !Wicket.Browser.isSafari() && typeof(document.all) != "undefined" && typeof(window.opera) == "undefined";
},
isIEQuirks: function() {
 return Wicket.Browser.isIE() && document.documentElement.clientHeight == 0;
}, 
isIELessThan7: function() {
var index = navigator.userAgent.indexOf("MSIE");
var version = parseFloat(navigator.userAgent.substring(index + 5));
return Wicket.Browser.isIE() && version < 7;
},
isIE7: function() {
var index = navigator.userAgent.indexOf("MSIE");
var version = parseFloat(navigator.userAgent.substring(index + 5));
return Wicket.Browser.isIE() && version >= 7;
},
isGecko: function() {
return /Gecko/.test(navigator.userAgent) && !Wicket.Browser.isSafari();
}
};
}

if (typeof(Wicket.Event) == "undefined") {
Wicket.Event = {
idCounter: 0,
getId: function(element) {
var current = element.getAttribute("id");
if (typeof(current) == "string" && current.length > 0) {
return current;
} else {
current = "wicket-generated-id-" + Wicket.Event.idCounter++;
element.setAttribute("id", current);
return current;
}
},
handler: function() {
var id = this[0];
var original = this[1];
var element = Wicket.$(id);
original.bind(element)();
},
fire: function(element, event) {
if (document.createEvent) {
var e=document.createEvent("Event");
e.initEvent(event, true, true);
return element.dispatchEvent(e);
} else {
return element.fireEvent("on"+event);
}
},
   add: function(element, type, fn) {
 if (element == window && type == "domready") {
Wicket.Event.addDomReadyEvent(fn);
} else {
if (element.addEventListener){
element.addEventListener((type == 'mousewheel' && Wicket.Browser.isGecko()) ? 'DOMMouseScroll' : type, fn, false);
} else {
if (element == window || element == document) {
fn = fn.bind(element);
}
else {
fn = Wicket.Event.handler.bind([Wicket.Event.getId(element), fn]); 
} 
   element.attachEvent('on'+type, fn);
}
}
return element;
},
 domReadyHandlers : new Array(),
 fireDomReadyHandlers : function() {
var h = Wicket.Event.domReadyHandlers;
while (h.length > 0) {
var c = h.shift();
c();
}
Wicket.Event.domReadyHandlers = null;
},
 addDomReadyEvent : function(fn) {
 if (window.loaded) {
fn();
} else if (!window.events || !window.events.domready) {
 Wicket.Event.domReadyHandlers.push(fn);
 var domReady = function() {
if (window.loaded)
return;
window.loaded = true;
 Wicket.Event.fireDomReadyHandlers();
}.bind(this);
if (document.readyState && (Wicket.Browser.isKHTML() || Wicket.Browser.isSafari())) {
 var domCheck = function() {
if (document.readyState == "loaded" ||
document.readyState == "complete") {
domReady();
} else {
 window.setTimeout(domCheck, 10);
}
}
window.setTimeout(domCheck, 10);
} else if (document.readyState && Wicket.Browser.isIE()) {
if (document.getElementById('ie_ready') == null) {
   var src = (window.location.protocol == 'https:') ? '\/\/:' : 'javascript:void(0)';
document.write('<script id="ie_ready" defer src="' + src + '"><\/script>');
document.getElementById('ie_ready').onreadystatechange = function() {
if (this.readyState == 'complete') domReady();
};
}
} else {
 Wicket.Event.add(document, "DOMContentLoaded", domReady);
}
} else {
window.addEventListener("domready", fn, false);
}
}
};
}