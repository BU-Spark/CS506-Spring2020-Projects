
;jQuery.ui || (function($) {
var _remove = $.fn.remove,
isFF2 = $.browser.mozilla && (parseFloat($.browser.version) < 1.9);

$.ui = {
version: "1.7.1",

plugin: {
add: function(module, option, set) {
var proto = $.ui[module].prototype;
for(var i in set) {
proto.plugins[i] = proto.plugins[i] || [];
proto.plugins[i].push([option, set[i]]);
}
},
call: function(instance, name, args) {
var set = instance.plugins[name];
if(!set || !instance.element[0].parentNode) { return; }
for (var i = 0; i < set.length; i++) {
if (instance.options[set[i][0]]) {
set[i][1].apply(instance.element, args);
}
}
}
},
contains: function(a, b) {
return document.compareDocumentPosition
? a.compareDocumentPosition(b) & 16
: a !== b && a.contains(b);
},
hasScroll: function(el, a) {

if ($(el).css('overflow') == 'hidden') { return false; }
var scroll = (a && a == 'left') ? 'scrollLeft' : 'scrollTop',
has = false;
if (el[scroll] > 0) { return true; }



el[scroll] = 1;
has = (el[scroll] > 0);
el[scroll] = 0;
return has;
},
isOverAxis: function(x, reference, size) {

return (x > reference) && (x < (reference + size));
},
isOver: function(y, x, top, left, height, width) {

return $.ui.isOverAxis(y, top, height) && $.ui.isOverAxis(x, left, width);
},
keyCode: {
BACKSPACE: 8,
CAPS_LOCK: 20,
COMMA: 188,
CONTROL: 17,
DELETE: 46,
DOWN: 40,
END: 35,
ENTER: 13,
ESCAPE: 27,
HOME: 36,
INSERT: 45,
LEFT: 37,
NUMPAD_ADD: 107,
NUMPAD_DECIMAL: 110,
NUMPAD_DIVIDE: 111,
NUMPAD_ENTER: 108,
NUMPAD_MULTIPLY: 106,
NUMPAD_SUBTRACT: 109,
PAGE_DOWN: 34,
PAGE_UP: 33,
PERIOD: 190,
RIGHT: 39,
SHIFT: 16,
SPACE: 32,
TAB: 9,
UP: 38
}
};

if (isFF2) {
var attr = $.attr,
removeAttr = $.fn.removeAttr,
ariaNS = "http://www.w3.org/2005/07/aaa",
ariaState = /^aria-/,
ariaRole = /^wairole:/;
$.attr = function(elem, name, value) {
var set = value !== undefined;
return (name == 'role'
? (set
? attr.call(this, elem, name, "wairole:" + value)
: (attr.apply(this, arguments) || "").replace(ariaRole, ""))
: (ariaState.test(name)
? (set
? elem.setAttributeNS(ariaNS,
name.replace(ariaState, "aaa:"), value)
: attr.call(this, elem, name.replace(ariaState, "aaa:")))
: attr.apply(this, arguments)));
};
$.fn.removeAttr = function(name) {
return (ariaState.test(name)
? this.each(function() {
this.removeAttributeNS(ariaNS, name.replace(ariaState, ""));
}) : removeAttr.call(this, name));
};
}

$.fn.extend({
remove: function() {


$("*", this).add(this).each(function() {
$(this).triggerHandler("remove");
});
return _remove.apply(this, arguments );
},
enableSelection: function() {
return this
.attr('unselectable', 'off')
.css('MozUserSelect', '')
.unbind('selectstart.ui');
},
disableSelection: function() {
return this
.attr('unselectable', 'on')
.css('MozUserSelect', 'none')
.bind('selectstart.ui', function() { return false; });
},
scrollParent: function() {
var scrollParent;
if(($.browser.msie && (/(static|relative)/).test(this.css('position'))) || (/absolute/).test(this.css('position'))) {
scrollParent = this.parents().filter(function() {
return (/(relative|absolute|fixed)/).test($.curCSS(this,'position',1)) && (/(auto|scroll)/).test($.curCSS(this,'overflow',1)+$.curCSS(this,'overflow-y',1)+$.curCSS(this,'overflow-x',1));
}).eq(0);
} else {
scrollParent = this.parents().filter(function() {
return (/(auto|scroll)/).test($.curCSS(this,'overflow',1)+$.curCSS(this,'overflow-y',1)+$.curCSS(this,'overflow-x',1));
}).eq(0);
}
return (/fixed/).test(this.css('position')) || !scrollParent.length ? $(document) : scrollParent;
}
});

$.extend($.expr[':'], {
data: function(elem, i, match) {
return !!$.data(elem, match[3]);
},
focusable: function(element) {
var nodeName = element.nodeName.toLowerCase(),
tabIndex = $.attr(element, 'tabindex');
return (/input|select|textarea|button|object/.test(nodeName)
? !element.disabled
: 'a' == nodeName || 'area' == nodeName
? element.href || !isNaN(tabIndex)
: !isNaN(tabIndex))


&& !$(element)['area' == nodeName ? 'parents' : 'closest'](':hidden').length;
},
tabbable: function(element) {
var tabIndex = $.attr(element, 'tabindex');
return (isNaN(tabIndex) || tabIndex >= 0) && $(element).is(':focusable');
}
});


function getter(namespace, plugin, method, args) {
function getMethods(type) {
var methods = $[namespace][plugin][type] || [];
return (typeof methods == 'string' ? methods.split(/,?\s+/) : methods);
}
var methods = getMethods('getter');
if (args.length == 1 && typeof args[0] == 'string') {
methods = methods.concat(getMethods('getterSetter'));
}
return ($.inArray(method, methods) != -1);
}
$.widget = function(name, prototype) {
var namespace = name.split(".")[0];
name = name.split(".")[1];

$.fn[name] = function(options) {
var isMethodCall = (typeof options == 'string'),
args = Array.prototype.slice.call(arguments, 1);

if (isMethodCall && options.substring(0, 1) == '_') {
return this;
}

if (isMethodCall && getter(namespace, name, options, args)) {
var instance = $.data(this[0], name);
return (instance ? instance[options].apply(instance, args)
: undefined);
}

return this.each(function() {
var instance = $.data(this, name);

(!instance && !isMethodCall &&
$.data(this, name, new $[namespace][name](this, options))._init());

(instance && isMethodCall && $.isFunction(instance[options]) &&
instance[options].apply(instance, args));
});
};

$[namespace] = $[namespace] || {};
$[namespace][name] = function(element, options) {
var self = this;
this.namespace = namespace;
this.widgetName = name;
this.widgetEventPrefix = $[namespace][name].eventPrefix || name;
this.widgetBaseClass = namespace + '-' + name;
this.options = $.extend({},
$.widget.defaults,
$[namespace][name].defaults,
$.metadata && $.metadata.get(element)[name],
options);
this.element = $(element)
.bind('setData.' + name, function(event, key, value) {
if (event.target == element) {
return self._setData(key, value);
}
})
.bind('getData.' + name, function(event, key) {
if (event.target == element) {
return self._getData(key);
}
})
.bind('remove', function() {
return self.destroy();
});
};

$[namespace][name].prototype = $.extend({}, $.widget.prototype, prototype);


$[namespace][name].getterSetter = 'option';
};
$.widget.prototype = {
_init: function() {},
destroy: function() {
this.element.removeData(this.widgetName)
.removeClass(this.widgetBaseClass + '-disabled' + ' ' + this.namespace + '-state-disabled')
.removeAttr('aria-disabled');
},
option: function(key, value) {
var options = key,
self = this;
if (typeof key == "string") {
if (value === undefined) {
return this._getData(key);
}
options = {};
options[key] = value;
}
$.each(options, function(key, value) {
self._setData(key, value);
});
},
_getData: function(key) {
return this.options[key];
},
_setData: function(key, value) {
this.options[key] = value;
if (key == 'disabled') {
this.element
[value ? 'addClass' : 'removeClass'](
this.widgetBaseClass + '-disabled' + ' ' +
this.namespace + '-state-disabled')
.attr("aria-disabled", value);
}
},
enable: function() {
this._setData('disabled', false);
},
disable: function() {
this._setData('disabled', true);
},
_trigger: function(type, event, data) {
var callback = this.options[type],
eventName = (type == this.widgetEventPrefix
? type : this.widgetEventPrefix + type);
event = $.Event(event);
event.type = eventName;



if (event.originalEvent) {
for (var i = $.event.props.length, prop; i;) {
prop = $.event.props[--i];
event[prop] = event.originalEvent[prop];
}
}
this.element.trigger(event, data);
return !($.isFunction(callback) && callback.call(this.element[0], event, data) === false
|| event.isDefaultPrevented());
}
};
$.widget.defaults = {
disabled: false
};

$.ui.mouse = {
_mouseInit: function() {
var self = this;
this.element
.bind('mousedown.'+this.widgetName, function(event) {
return self._mouseDown(event);
})
.bind('click.'+this.widgetName, function(event) {
if(self._preventClickEvent) {
self._preventClickEvent = false;
event.stopImmediatePropagation();
return false;
}
});

if ($.browser.msie) {
this._mouseUnselectable = this.element.attr('unselectable');
this.element.attr('unselectable', 'on');
}
this.started = false;
},


_mouseDestroy: function() {
this.element.unbind('.'+this.widgetName);

($.browser.msie
&& this.element.attr('unselectable', this._mouseUnselectable));
},
_mouseDown: function(event) {


event.originalEvent = event.originalEvent || {};
if (event.originalEvent.mouseHandled) { return; }

(this._mouseStarted && this._mouseUp(event));
this._mouseDownEvent = event;
var self = this,
btnIsLeft = (event.which == 1),
elIsCancel = (typeof this.options.cancel == "string" ? $(event.target).parents().add(event.target).filter(this.options.cancel).length : false);
if (!btnIsLeft || elIsCancel || !this._mouseCapture(event)) {
return true;
}
this.mouseDelayMet = !this.options.delay;
if (!this.mouseDelayMet) {
this._mouseDelayTimer = setTimeout(function() {
self.mouseDelayMet = true;
}, this.options.delay);
}
if (this._mouseDistanceMet(event) && this._mouseDelayMet(event)) {
this._mouseStarted = (this._mouseStart(event) !== false);
if (!this._mouseStarted) {
event.preventDefault();
return true;
}
}

this._mouseMoveDelegate = function(event) {
return self._mouseMove(event);
};
this._mouseUpDelegate = function(event) {
return self._mouseUp(event);
};
$(document)
.bind('mousemove.'+this.widgetName, this._mouseMoveDelegate)
.bind('mouseup.'+this.widgetName, this._mouseUpDelegate);



($.browser.safari || event.preventDefault());
event.originalEvent.mouseHandled = true;
return true;
},
_mouseMove: function(event) {

if ($.browser.msie && !event.button) {
return this._mouseUp(event);
}
if (this._mouseStarted) {
this._mouseDrag(event);
return event.preventDefault();
}
if (this._mouseDistanceMet(event) && this._mouseDelayMet(event)) {
this._mouseStarted =
(this._mouseStart(this._mouseDownEvent, event) !== false);
(this._mouseStarted ? this._mouseDrag(event) : this._mouseUp(event));
}
return !this._mouseStarted;
},
_mouseUp: function(event) {
$(document)
.unbind('mousemove.'+this.widgetName, this._mouseMoveDelegate)
.unbind('mouseup.'+this.widgetName, this._mouseUpDelegate);
if (this._mouseStarted) {
this._mouseStarted = false;
this._preventClickEvent = (event.target == this._mouseDownEvent.target);
this._mouseStop(event);
}
return false;
},
_mouseDistanceMet: function(event) {
return (Math.max(
Math.abs(this._mouseDownEvent.pageX - event.pageX),
Math.abs(this._mouseDownEvent.pageY - event.pageY)
) >= this.options.distance
);
},
_mouseDelayMet: function(event) {
return this.mouseDelayMet;
},

_mouseStart: function(event) {},
_mouseDrag: function(event) {},
_mouseStop: function(event) {},
_mouseCapture: function(event) { return true; }
};
$.ui.mouse.defaults = {
cancel: null,
distance: 1,
delay: 0
};
})(jQuery);

(function($) {
$.widget("ui.draggable", $.extend({}, $.ui.mouse, {
_init: function() {
if (this.options.helper == 'original' && !(/^(?:r|a|f)/).test(this.element.css("position")))
this.element[0].style.position = 'relative';
(this.options.addClasses && this.element.addClass("ui-draggable"));
(this.options.disabled && this.element.addClass("ui-draggable-disabled"));
this._mouseInit();
},
destroy: function() {
if(!this.element.data('draggable')) return;
this.element
.removeData("draggable")
.unbind(".draggable")
.removeClass("ui-draggable"
+ " ui-draggable-dragging"
+ " ui-draggable-disabled");
this._mouseDestroy();
},
_mouseCapture: function(event) {
var o = this.options;
if (this.helper || o.disabled || $(event.target).is('.ui-resizable-handle'))
return false;

this.handle = this._getHandle(event);
if (!this.handle)
return false;
return true;
},
_mouseStart: function(event) {
var o = this.options;

this.helper = this._createHelper(event);

this._cacheHelperProportions();

if($.ui.ddmanager)
$.ui.ddmanager.current = this;


this._cacheMargins();

this.cssPosition = this.helper.css("position");
this.scrollParent = this.helper.scrollParent();

this.offset = this.element.offset();
this.offset = {
top: this.offset.top - this.margins.top,
left: this.offset.left - this.margins.left
};
$.extend(this.offset, {
click: { 
left: event.pageX - this.offset.left,
top: event.pageY - this.offset.top
},
parent: this._getParentOffset(),
relative: this._getRelativeOffset() 
});

this.originalPosition = this._generatePosition(event);
this.originalPageX = event.pageX;
this.originalPageY = event.pageY;

if(o.cursorAt)
this._adjustOffsetFromHelper(o.cursorAt);

if(o.containment)
this._setContainment();

this._trigger("start", event);

this._cacheHelperProportions();

if ($.ui.ddmanager && !o.dropBehaviour)
$.ui.ddmanager.prepareOffsets(this, event);
this.helper.addClass("ui-draggable-dragging");
this._mouseDrag(event, true); 
return true;
},
_mouseDrag: function(event, noPropagation) {

this.position = this._generatePosition(event);
this.positionAbs = this._convertPositionTo("absolute");

if (!noPropagation) {
var ui = this._uiHash();
this._trigger('drag', event, ui);
this.position = ui.position;
}
if(!this.options.axis || this.options.axis != "y") this.helper[0].style.left = this.position.left+'px';
if(!this.options.axis || this.options.axis != "x") this.helper[0].style.top = this.position.top+'px';
if($.ui.ddmanager) $.ui.ddmanager.drag(this, event);
return false;
},
_mouseStop: function(event) {

var dropped = false;
if ($.ui.ddmanager && !this.options.dropBehaviour)
dropped = $.ui.ddmanager.drop(this, event);

if(this.dropped) {
dropped = this.dropped;
this.dropped = false;
}
if((this.options.revert == "invalid" && !dropped) || (this.options.revert == "valid" && dropped) || this.options.revert === true || ($.isFunction(this.options.revert) && this.options.revert.call(this.element, dropped))) {
var self = this;
$(this.helper).animate(this.originalPosition, parseInt(this.options.revertDuration, 10), function() {
self._trigger("stop", event);
self._clear();
});
} else {
this._trigger("stop", event);
this._clear();
}
return false;
},
_getHandle: function(event) {
var handle = !this.options.handle || !$(this.options.handle, this.element).length ? true : false;
$(this.options.handle, this.element)
.find("*")
.andSelf()
.each(function() {
if(this == event.target) handle = true;
});
return handle;
},
_createHelper: function(event) {
var o = this.options;
var helper = $.isFunction(o.helper) ? $(o.helper.apply(this.element[0], [event])) : (o.helper == 'clone' ? this.element.clone() : this.element);
if(!helper.parents('body').length)
helper.appendTo((o.appendTo == 'parent' ? this.element[0].parentNode : o.appendTo));
if(helper[0] != this.element[0] && !(/(fixed|absolute)/).test(helper.css("position")))
helper.css("position", "absolute");
return helper;
},
_adjustOffsetFromHelper: function(obj) {
if(obj.left != undefined) this.offset.click.left = obj.left + this.margins.left;
if(obj.right != undefined) this.offset.click.left = this.helperProportions.width - obj.right + this.margins.left;
if(obj.top != undefined) this.offset.click.top = obj.top + this.margins.top;
if(obj.bottom != undefined) this.offset.click.top = this.helperProportions.height - obj.bottom + this.margins.top;
},
_getParentOffset: function() {

this.offsetParent = this.helper.offsetParent();
var po = this.offsetParent.offset();




if(this.cssPosition == 'absolute' && this.scrollParent[0] != document && $.ui.contains(this.scrollParent[0], this.offsetParent[0])) {
po.left += this.scrollParent.scrollLeft();
po.top += this.scrollParent.scrollTop();
}
if((this.offsetParent[0] == document.body) 
|| (this.offsetParent[0].tagName && this.offsetParent[0].tagName.toLowerCase() == 'html' && $.browser.msie)) 
po = { top: 0, left: 0 };
return {
top: po.top + (parseInt(this.offsetParent.css("borderTopWidth"),10) || 0),
left: po.left + (parseInt(this.offsetParent.css("borderLeftWidth"),10) || 0)
};
},
_getRelativeOffset: function() {
if(this.cssPosition == "relative") {
var p = this.element.position();
return {
top: p.top - (parseInt(this.helper.css("top"),10) || 0) + this.scrollParent.scrollTop(),
left: p.left - (parseInt(this.helper.css("left"),10) || 0) + this.scrollParent.scrollLeft()
};
} else {
return { top: 0, left: 0 };
}
},
_cacheMargins: function() {
this.margins = {
left: (parseInt(this.element.css("marginLeft"),10) || 0),
top: (parseInt(this.element.css("marginTop"),10) || 0)
};
},
_cacheHelperProportions: function() {
this.helperProportions = {
width: this.helper.outerWidth(),
height: this.helper.outerHeight()
};
},
_setContainment: function() {
var o = this.options;
if(o.containment == 'parent') o.containment = this.helper[0].parentNode;
if(o.containment == 'document' || o.containment == 'window') this.containment = [
0 - this.offset.relative.left - this.offset.parent.left,
0 - this.offset.relative.top - this.offset.parent.top,
$(o.containment == 'document' ? document : window).width() - this.helperProportions.width - this.margins.left,
($(o.containment == 'document' ? document : window).height() || document.body.parentNode.scrollHeight) - this.helperProportions.height - this.margins.top
];
if(!(/^(document|window|parent)$/).test(o.containment) && o.containment.constructor != Array) {
var ce = $(o.containment)[0]; if(!ce) return;
var co = $(o.containment).offset();
var over = ($(ce).css("overflow") != 'hidden');
this.containment = [
co.left + (parseInt($(ce).css("borderLeftWidth"),10) || 0) + (parseInt($(ce).css("paddingLeft"),10) || 0) - this.margins.left,
co.top + (parseInt($(ce).css("borderTopWidth"),10) || 0) + (parseInt($(ce).css("paddingTop"),10) || 0) - this.margins.top,
co.left+(over ? Math.max(ce.scrollWidth,ce.offsetWidth) : ce.offsetWidth) - (parseInt($(ce).css("borderLeftWidth"),10) || 0) - (parseInt($(ce).css("paddingRight"),10) || 0) - this.helperProportions.width - this.margins.left,
co.top+(over ? Math.max(ce.scrollHeight,ce.offsetHeight) : ce.offsetHeight) - (parseInt($(ce).css("borderTopWidth"),10) || 0) - (parseInt($(ce).css("paddingBottom"),10) || 0) - this.helperProportions.height - this.margins.top
];
} else if(o.containment.constructor == Array) {
this.containment = o.containment;
}
},
_convertPositionTo: function(d, pos) {
if(!pos) pos = this.position;
var mod = d == "absolute" ? 1 : -1;
var o = this.options, scroll = this.cssPosition == 'absolute' && !(this.scrollParent[0] != document && $.ui.contains(this.scrollParent[0], this.offsetParent[0])) ? this.offsetParent : this.scrollParent, scrollIsRootNode = (/(html|body)/i).test(scroll[0].tagName);
return {
top: (
pos.top 
+ this.offset.relative.top * mod 
+ this.offset.parent.top * mod 
- ($.browser.safari && this.cssPosition == 'fixed' ? 0 : ( this.cssPosition == 'fixed' ? -this.scrollParent.scrollTop() : ( scrollIsRootNode ? 0 : scroll.scrollTop() ) ) * mod)
),
left: (
pos.left 
+ this.offset.relative.left * mod 
+ this.offset.parent.left * mod 
- ($.browser.safari && this.cssPosition == 'fixed' ? 0 : ( this.cssPosition == 'fixed' ? -this.scrollParent.scrollLeft() : scrollIsRootNode ? 0 : scroll.scrollLeft() ) * mod)
)
};
},
_generatePosition: function(event) {
var o = this.options, scroll = this.cssPosition == 'absolute' && !(this.scrollParent[0] != document && $.ui.contains(this.scrollParent[0], this.offsetParent[0])) ? this.offsetParent : this.scrollParent, scrollIsRootNode = (/(html|body)/i).test(scroll[0].tagName);




if(this.cssPosition == 'relative' && !(this.scrollParent[0] != document && this.scrollParent[0] != this.offsetParent[0])) {
this.offset.relative = this._getRelativeOffset();
}
var pageX = event.pageX;
var pageY = event.pageY;

if(this.originalPosition) { 
if(this.containment) {
if(event.pageX - this.offset.click.left < this.containment[0]) pageX = this.containment[0] + this.offset.click.left;
if(event.pageY - this.offset.click.top < this.containment[1]) pageY = this.containment[1] + this.offset.click.top;
if(event.pageX - this.offset.click.left > this.containment[2]) pageX = this.containment[2] + this.offset.click.left;
if(event.pageY - this.offset.click.top > this.containment[3]) pageY = this.containment[3] + this.offset.click.top;
}
if(o.grid) {
var top = this.originalPageY + Math.round((pageY - this.originalPageY) / o.grid[1]) * o.grid[1];
pageY = this.containment ? (!(top - this.offset.click.top < this.containment[1] || top - this.offset.click.top > this.containment[3]) ? top : (!(top - this.offset.click.top < this.containment[1]) ? top - o.grid[1] : top + o.grid[1])) : top;
var left = this.originalPageX + Math.round((pageX - this.originalPageX) / o.grid[0]) * o.grid[0];
pageX = this.containment ? (!(left - this.offset.click.left < this.containment[0] || left - this.offset.click.left > this.containment[2]) ? left : (!(left - this.offset.click.left < this.containment[0]) ? left - o.grid[0] : left + o.grid[0])) : left;
}
}
return {
top: (
pageY 
- this.offset.click.top 
- this.offset.relative.top 
- this.offset.parent.top 
+ ($.browser.safari && this.cssPosition == 'fixed' ? 0 : ( this.cssPosition == 'fixed' ? -this.scrollParent.scrollTop() : ( scrollIsRootNode ? 0 : scroll.scrollTop() ) ))
),
left: (
pageX 
- this.offset.click.left 
- this.offset.relative.left 
- this.offset.parent.left 
+ ($.browser.safari && this.cssPosition == 'fixed' ? 0 : ( this.cssPosition == 'fixed' ? -this.scrollParent.scrollLeft() : scrollIsRootNode ? 0 : scroll.scrollLeft() ))
)
};
},
_clear: function() {
this.helper.removeClass("ui-draggable-dragging");
if(this.helper[0] != this.element[0] && !this.cancelHelperRemoval) this.helper.remove();

this.helper = null;
this.cancelHelperRemoval = false;
},

_trigger: function(type, event, ui) {
ui = ui || this._uiHash();
$.ui.plugin.call(this, type, [event, ui]);
if(type == "drag") this.positionAbs = this._convertPositionTo("absolute"); 
return $.widget.prototype._trigger.call(this, type, event, ui);
},
plugins: {},
_uiHash: function(event) {
return {
helper: this.helper,
position: this.position,
absolutePosition: this.positionAbs, 
offset: this.positionAbs
};
}
}));
$.extend($.ui.draggable, {
version: "1.7.1",
eventPrefix: "drag",
defaults: {
addClasses: true,
appendTo: "parent",
axis: false,
cancel: ":input,option",
connectToSortable: false,
containment: false,
cursor: "auto",
cursorAt: false,
delay: 0,
distance: 1,
grid: false,
handle: false,
helper: "original",
iframeFix: false,
opacity: false,
refreshPositions: false,
revert: false,
revertDuration: 500,
scope: "default",
scroll: true,
scrollSensitivity: 20,
scrollSpeed: 20,
snap: false,
snapMode: "both",
snapTolerance: 20,
stack: false,
zIndex: false
}
});
$.ui.plugin.add("draggable", "connectToSortable", {
start: function(event, ui) {
var inst = $(this).data("draggable"), o = inst.options,
uiSortable = $.extend({}, ui, { item: inst.element });
inst.sortables = [];
$(o.connectToSortable).each(function() {
var sortable = $.data(this, 'sortable');
if (sortable && !sortable.options.disabled) {
inst.sortables.push({
instance: sortable,
shouldRevert: sortable.options.revert
});
sortable._refreshItems();	
sortable._trigger("activate", event, uiSortable);
}
});
},
stop: function(event, ui) {

var inst = $(this).data("draggable"),
uiSortable = $.extend({}, ui, { item: inst.element });
$.each(inst.sortables, function() {
if(this.instance.isOver) {
this.instance.isOver = 0;
inst.cancelHelperRemoval = true; 
this.instance.cancelHelperRemoval = false; 

if(this.shouldRevert) this.instance.options.revert = true;

this.instance._mouseStop(event);
this.instance.options.helper = this.instance.options._helper;

if(inst.options.helper == 'original')
this.instance.currentItem.css({ top: 'auto', left: 'auto' });
} else {
this.instance.cancelHelperRemoval = false; 
this.instance._trigger("deactivate", event, uiSortable);
}
});
},
drag: function(event, ui) {
var inst = $(this).data("draggable"), self = this;
var checkPos = function(o) {
var dyClick = this.offset.click.top, dxClick = this.offset.click.left;
var helperTop = this.positionAbs.top, helperLeft = this.positionAbs.left;
var itemHeight = o.height, itemWidth = o.width;
var itemTop = o.top, itemLeft = o.left;
return $.ui.isOver(helperTop + dyClick, helperLeft + dxClick, itemTop, itemLeft, itemHeight, itemWidth);
};
$.each(inst.sortables, function(i) {

this.instance.positionAbs = inst.positionAbs;
this.instance.helperProportions = inst.helperProportions;
this.instance.offset.click = inst.offset.click;
if(this.instance._intersectsWith(this.instance.containerCache)) {

if(!this.instance.isOver) {
this.instance.isOver = 1;



this.instance.currentItem = $(self).clone().appendTo(this.instance.element).data("sortable-item", true);
this.instance.options._helper = this.instance.options.helper; 
this.instance.options.helper = function() { return ui.helper[0]; };
event.target = this.instance.currentItem[0];
this.instance._mouseCapture(event, true);
this.instance._mouseStart(event, true, true);

this.instance.offset.click.top = inst.offset.click.top;
this.instance.offset.click.left = inst.offset.click.left;
this.instance.offset.parent.left -= inst.offset.parent.left - this.instance.offset.parent.left;
this.instance.offset.parent.top -= inst.offset.parent.top - this.instance.offset.parent.top;
inst._trigger("toSortable", event);
inst.dropped = this.instance.element; 

inst.currentItem = inst.element;
this.instance.fromOutside = inst;
}

if(this.instance.currentItem) this.instance._mouseDrag(event);
} else {


if(this.instance.isOver) {
this.instance.isOver = 0;
this.instance.cancelHelperRemoval = true;

this.instance.options.revert = false;

this.instance._trigger('out', event, this.instance._uiHash(this.instance));
this.instance._mouseStop(event, true);
this.instance.options.helper = this.instance.options._helper;

this.instance.currentItem.remove();
if(this.instance.placeholder) this.instance.placeholder.remove();
inst._trigger("fromSortable", event);
inst.dropped = false; 
}
};
});
}
});
$.ui.plugin.add("draggable", "cursor", {
start: function(event, ui) {
var t = $('body'), o = $(this).data('draggable').options;
if (t.css("cursor")) o._cursor = t.css("cursor");
t.css("cursor", o.cursor);
},
stop: function(event, ui) {
var o = $(this).data('draggable').options;
if (o._cursor) $('body').css("cursor", o._cursor);
}
});
$.ui.plugin.add("draggable", "iframeFix", {
start: function(event, ui) {
var o = $(this).data('draggable').options;
$(o.iframeFix === true ? "iframe" : o.iframeFix).each(function() {
$('<div class="ui-draggable-iframeFix" style="background: #fff;"></div>')
.css({
width: this.offsetWidth+"px", height: this.offsetHeight+"px",
position: "absolute", opacity: "0.001", zIndex: 1000
})
.css($(this).offset())
.appendTo("body");
});
},
stop: function(event, ui) {
$("div.ui-draggable-iframeFix").each(function() { this.parentNode.removeChild(this); }); 
}
});
$.ui.plugin.add("draggable", "opacity", {
start: function(event, ui) {
var t = $(ui.helper), o = $(this).data('draggable').options;
if(t.css("opacity")) o._opacity = t.css("opacity");
t.css('opacity', o.opacity);
},
stop: function(event, ui) {
var o = $(this).data('draggable').options;
if(o._opacity) $(ui.helper).css('opacity', o._opacity);
}
});
$.ui.plugin.add("draggable", "scroll", {
start: function(event, ui) {
var i = $(this).data("draggable");
if(i.scrollParent[0] != document && i.scrollParent[0].tagName != 'HTML') i.overflowOffset = i.scrollParent.offset();
},
drag: function(event, ui) {
var i = $(this).data("draggable"), o = i.options, scrolled = false;
if(i.scrollParent[0] != document && i.scrollParent[0].tagName != 'HTML') {
if(!o.axis || o.axis != 'x') {
if((i.overflowOffset.top + i.scrollParent[0].offsetHeight) - event.pageY < o.scrollSensitivity)
i.scrollParent[0].scrollTop = scrolled = i.scrollParent[0].scrollTop + o.scrollSpeed;
else if(event.pageY - i.overflowOffset.top < o.scrollSensitivity)
i.scrollParent[0].scrollTop = scrolled = i.scrollParent[0].scrollTop - o.scrollSpeed;
}
if(!o.axis || o.axis != 'y') {
if((i.overflowOffset.left + i.scrollParent[0].offsetWidth) - event.pageX < o.scrollSensitivity)
i.scrollParent[0].scrollLeft = scrolled = i.scrollParent[0].scrollLeft + o.scrollSpeed;
else if(event.pageX - i.overflowOffset.left < o.scrollSensitivity)
i.scrollParent[0].scrollLeft = scrolled = i.scrollParent[0].scrollLeft - o.scrollSpeed;
}
} else {
if(!o.axis || o.axis != 'x') {
if(event.pageY - $(document).scrollTop() < o.scrollSensitivity)
scrolled = $(document).scrollTop($(document).scrollTop() - o.scrollSpeed);
else if($(window).height() - (event.pageY - $(document).scrollTop()) < o.scrollSensitivity)
scrolled = $(document).scrollTop($(document).scrollTop() + o.scrollSpeed);
}
if(!o.axis || o.axis != 'y') {
if(event.pageX - $(document).scrollLeft() < o.scrollSensitivity)
scrolled = $(document).scrollLeft($(document).scrollLeft() - o.scrollSpeed);
else if($(window).width() - (event.pageX - $(document).scrollLeft()) < o.scrollSensitivity)
scrolled = $(document).scrollLeft($(document).scrollLeft() + o.scrollSpeed);
}
}
if(scrolled !== false && $.ui.ddmanager && !o.dropBehaviour)
$.ui.ddmanager.prepareOffsets(i, event);
}
});
$.ui.plugin.add("draggable", "snap", {
start: function(event, ui) {
var i = $(this).data("draggable"), o = i.options;
i.snapElements = [];
$(o.snap.constructor != String ? ( o.snap.items || ':data(draggable)' ) : o.snap).each(function() {
var $t = $(this); var $o = $t.offset();
if(this != i.element[0]) i.snapElements.push({
item: this,
width: $t.outerWidth(), height: $t.outerHeight(),
top: $o.top, left: $o.left
});
});
},
drag: function(event, ui) {
var inst = $(this).data("draggable"), o = inst.options;
var d = o.snapTolerance;
var x1 = ui.offset.left, x2 = x1 + inst.helperProportions.width,
y1 = ui.offset.top, y2 = y1 + inst.helperProportions.height;
for (var i = inst.snapElements.length - 1; i >= 0; i--){
var l = inst.snapElements[i].left, r = l + inst.snapElements[i].width,
t = inst.snapElements[i].top, b = t + inst.snapElements[i].height;

if(!((l-d < x1 && x1 < r+d && t-d < y1 && y1 < b+d) || (l-d < x1 && x1 < r+d && t-d < y2 && y2 < b+d) || (l-d < x2 && x2 < r+d && t-d < y1 && y1 < b+d) || (l-d < x2 && x2 < r+d && t-d < y2 && y2 < b+d))) {
if(inst.snapElements[i].snapping) (inst.options.snap.release && inst.options.snap.release.call(inst.element, event, $.extend(inst._uiHash(), { snapItem: inst.snapElements[i].item })));
inst.snapElements[i].snapping = false;
continue;
}
if(o.snapMode != 'inner') {
var ts = Math.abs(t - y2) <= d;
var bs = Math.abs(b - y1) <= d;
var ls = Math.abs(l - x2) <= d;
var rs = Math.abs(r - x1) <= d;
if(ts) ui.position.top = inst._convertPositionTo("relative", { top: t - inst.helperProportions.height, left: 0 }).top - inst.margins.top;
if(bs) ui.position.top = inst._convertPositionTo("relative", { top: b, left: 0 }).top - inst.margins.top;
if(ls) ui.position.left = inst._convertPositionTo("relative", { top: 0, left: l - inst.helperProportions.width }).left - inst.margins.left;
if(rs) ui.position.left = inst._convertPositionTo("relative", { top: 0, left: r }).left - inst.margins.left;
}
var first = (ts || bs || ls || rs);
if(o.snapMode != 'outer') {
var ts = Math.abs(t - y1) <= d;
var bs = Math.abs(b - y2) <= d;
var ls = Math.abs(l - x1) <= d;
var rs = Math.abs(r - x2) <= d;
if(ts) ui.position.top = inst._convertPositionTo("relative", { top: t, left: 0 }).top - inst.margins.top;
if(bs) ui.position.top = inst._convertPositionTo("relative", { top: b - inst.helperProportions.height, left: 0 }).top - inst.margins.top;
if(ls) ui.position.left = inst._convertPositionTo("relative", { top: 0, left: l }).left - inst.margins.left;
if(rs) ui.position.left = inst._convertPositionTo("relative", { top: 0, left: r - inst.helperProportions.width }).left - inst.margins.left;
}
if(!inst.snapElements[i].snapping && (ts || bs || ls || rs || first))
(inst.options.snap.snap && inst.options.snap.snap.call(inst.element, event, $.extend(inst._uiHash(), { snapItem: inst.snapElements[i].item })));
inst.snapElements[i].snapping = (ts || bs || ls || rs || first);
};
}
});
$.ui.plugin.add("draggable", "stack", {
start: function(event, ui) {
var o = $(this).data("draggable").options;
var group = $.makeArray($(o.stack.group)).sort(function(a,b) {
return (parseInt($(a).css("zIndex"),10) || o.stack.min) - (parseInt($(b).css("zIndex"),10) || o.stack.min);
});
$(group).each(function(i) {
this.style.zIndex = o.stack.min + i;
});
this[0].style.zIndex = o.stack.min + group.length;
}
});
$.ui.plugin.add("draggable", "zIndex", {
start: function(event, ui) {
var t = $(ui.helper), o = $(this).data("draggable").options;
if(t.css("zIndex")) o._zIndex = t.css("zIndex");
t.css('zIndex', o.zIndex);
},
stop: function(event, ui) {
var o = $(this).data("draggable").options;
if(o._zIndex) $(ui.helper).css('zIndex', o._zIndex);
}
});
})(jQuery);

;jQuery.effects || (function($) {
$.effects = {
version: "1.7.1",

save: function(element, set) {
for(var i=0; i < set.length; i++) {
if(set[i] !== null) element.data("ec.storage."+set[i], element[0].style[set[i]]);
}
},

restore: function(element, set) {
for(var i=0; i < set.length; i++) {
if(set[i] !== null) element.css(set[i], element.data("ec.storage."+set[i]));
}
},
setMode: function(el, mode) {
if (mode == 'toggle') mode = el.is(':hidden') ? 'show' : 'hide'; 
return mode;
},
getBaseline: function(origin, original) { 

var y, x;
switch (origin[0]) {
case 'top': y = 0; break;
case 'middle': y = 0.5; break;
case 'bottom': y = 1; break;
default: y = origin[0] / original.height;
};
switch (origin[1]) {
case 'left': x = 0; break;
case 'center': x = 0.5; break;
case 'right': x = 1; break;
default: x = origin[1] / original.width;
};
return {x: x, y: y};
},

createWrapper: function(element) {

if (element.parent().is('.ui-effects-wrapper'))
return element.parent();

var props = { width: element.outerWidth(true), height: element.outerHeight(true), 'float': element.css('float') };
element.wrap('<div class="ui-effects-wrapper" style="font-size:100%;background:transparent;border:none;margin:0;padding:0"></div>');
var wrapper = element.parent();

if (element.css('position') == 'static') {
wrapper.css({ position: 'relative' });
element.css({ position: 'relative'} );
} else {
var top = element.css('top'); if(isNaN(parseInt(top,10))) top = 'auto';
var left = element.css('left'); if(isNaN(parseInt(left,10))) left = 'auto';
wrapper.css({ position: element.css('position'), top: top, left: left, zIndex: element.css('z-index') }).show();
element.css({position: 'relative', top: 0, left: 0 });
}
wrapper.css(props);
return wrapper;
},
removeWrapper: function(element) {
if (element.parent().is('.ui-effects-wrapper'))
return element.parent().replaceWith(element);
return element;
},
setTransition: function(element, list, factor, value) {
value = value || {};
$.each(list, function(i, x){
unit = element.cssUnit(x);
if (unit[0] > 0) value[x] = unit[0] * factor + unit[1];
});
return value;
},

animateClass: function(value, duration, easing, callback) {
var cb = (typeof easing == "function" ? easing : (callback ? callback : null));
var ea = (typeof easing == "string" ? easing : null);
return this.each(function() {
var offset = {}; var that = $(this); var oldStyleAttr = that.attr("style") || '';
if(typeof oldStyleAttr == 'object') oldStyleAttr = oldStyleAttr["cssText"]; 
if(value.toggle) { that.hasClass(value.toggle) ? value.remove = value.toggle : value.add = value.toggle; }

var oldStyle = $.extend({}, (document.defaultView ? document.defaultView.getComputedStyle(this,null) : this.currentStyle));
if(value.add) that.addClass(value.add); if(value.remove) that.removeClass(value.remove);
var newStyle = $.extend({}, (document.defaultView ? document.defaultView.getComputedStyle(this,null) : this.currentStyle));
if(value.add) that.removeClass(value.add); if(value.remove) that.addClass(value.remove);

for(var n in newStyle) {
if( typeof newStyle[n] != "function" && newStyle[n] 
&& n.indexOf("Moz") == -1 && n.indexOf("length") == -1 
&& newStyle[n] != oldStyle[n] 
&& (n.match(/color/i) || (!n.match(/color/i) && !isNaN(parseInt(newStyle[n],10)))) 
&& (oldStyle.position != "static" || (oldStyle.position == "static" && !n.match(/left|top|bottom|right/))) 
) offset[n] = newStyle[n];
}
that.animate(offset, duration, ea, function() { 

if(typeof $(this).attr("style") == 'object') { $(this).attr("style")["cssText"] = ""; $(this).attr("style")["cssText"] = oldStyleAttr; } else $(this).attr("style", oldStyleAttr);
if(value.add) $(this).addClass(value.add); if(value.remove) $(this).removeClass(value.remove);
if(cb) cb.apply(this, arguments);
});
});
}
};
function _normalizeArguments(a, m) {
var o = a[1] && a[1].constructor == Object ? a[1] : {}; if(m) o.mode = m;
var speed = a[1] && a[1].constructor != Object ? a[1] : (o.duration ? o.duration : a[2]); 
speed = $.fx.off ? 0 : typeof speed === "number" ? speed : $.fx.speeds[speed] || $.fx.speeds._default;
var callback = o.callback || ( $.isFunction(a[1]) && a[1] ) || ( $.isFunction(a[2]) && a[2] ) || ( $.isFunction(a[3]) && a[3] );
return [a[0], o, speed, callback];
}

$.fn.extend({

_show: $.fn.show,
_hide: $.fn.hide,
__toggle: $.fn.toggle,
_addClass: $.fn.addClass,
_removeClass: $.fn.removeClass,
_toggleClass: $.fn.toggleClass,

effect: function(fx, options, speed, callback) {
return $.effects[fx] ? $.effects[fx].call(this, {method: fx, options: options || {}, duration: speed, callback: callback }) : null;
},
show: function() {
if(!arguments[0] || (arguments[0].constructor == Number || (/(slow|normal|fast)/).test(arguments[0])))
return this._show.apply(this, arguments);
else {
return this.effect.apply(this, _normalizeArguments(arguments, 'show'));
}
},
hide: function() {
if(!arguments[0] || (arguments[0].constructor == Number || (/(slow|normal|fast)/).test(arguments[0])))
return this._hide.apply(this, arguments);
else {
return this.effect.apply(this, _normalizeArguments(arguments, 'hide'));
}
},
toggle: function(){
if(!arguments[0] || (arguments[0].constructor == Number || (/(slow|normal|fast)/).test(arguments[0])) || (arguments[0].constructor == Function))
return this.__toggle.apply(this, arguments);
else {
return this.effect.apply(this, _normalizeArguments(arguments, 'toggle'));
}
},
addClass: function(classNames, speed, easing, callback) {
return speed ? $.effects.animateClass.apply(this, [{ add: classNames },speed,easing,callback]) : this._addClass(classNames);
},
removeClass: function(classNames,speed,easing,callback) {
return speed ? $.effects.animateClass.apply(this, [{ remove: classNames },speed,easing,callback]) : this._removeClass(classNames);
},
toggleClass: function(classNames,speed,easing,callback) {
return ( (typeof speed !== "boolean") && speed ) ? $.effects.animateClass.apply(this, [{ toggle: classNames },speed,easing,callback]) : this._toggleClass(classNames, speed);
},
morph: function(remove,add,speed,easing,callback) {
return $.effects.animateClass.apply(this, [{ add: add, remove: remove },speed,easing,callback]);
},
switchClass: function() {
return this.morph.apply(this, arguments);
},

cssUnit: function(key) {
var style = this.css(key), val = [];
$.each( ['em','px','%','pt'], function(i, unit){
if(style.indexOf(unit) > 0)
val = [parseFloat(style), unit];
});
return val;
}
});


$.each(['backgroundColor', 'borderBottomColor', 'borderLeftColor', 'borderRightColor', 'borderTopColor', 'color', 'outlineColor'], function(i,attr){
$.fx.step[attr] = function(fx) {
if ( fx.state == 0 ) {
fx.start = getColor( fx.elem, attr );
fx.end = getRGB( fx.end );
}
fx.elem.style[attr] = "rgb(" + [
Math.max(Math.min( parseInt((fx.pos * (fx.end[0] - fx.start[0])) + fx.start[0],10), 255), 0),
Math.max(Math.min( parseInt((fx.pos * (fx.end[1] - fx.start[1])) + fx.start[1],10), 255), 0),
Math.max(Math.min( parseInt((fx.pos * (fx.end[2] - fx.start[2])) + fx.start[2],10), 255), 0)
].join(",") + ")";
};
});




function getRGB(color) {
var result;

if ( color && color.constructor == Array && color.length == 3 )
return color;

if (result = /rgb\(\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*\)/.exec(color))
return [parseInt(result[1],10), parseInt(result[2],10), parseInt(result[3],10)];

if (result = /rgb\(\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\%\s*\)/.exec(color))
return [parseFloat(result[1])*2.55, parseFloat(result[2])*2.55, parseFloat(result[3])*2.55];

if (result = /#([a-fA-F0-9]{2})([a-fA-F0-9]{2})([a-fA-F0-9]{2})/.exec(color))
return [parseInt(result[1],16), parseInt(result[2],16), parseInt(result[3],16)];

if (result = /#([a-fA-F0-9])([a-fA-F0-9])([a-fA-F0-9])/.exec(color))
return [parseInt(result[1]+result[1],16), parseInt(result[2]+result[2],16), parseInt(result[3]+result[3],16)];

if (result = /rgba\(0, 0, 0, 0\)/.exec(color))
return colors['transparent'];

return colors[$.trim(color).toLowerCase()];
}
function getColor(elem, attr) {
var color;
do {
color = $.curCSS(elem, attr);

if ( color != '' && color != 'transparent' || $.nodeName(elem, "body") )
break;
attr = "backgroundColor";
} while ( elem = elem.parentNode );
return getRGB(color);
};



var colors = {
aqua:[0,255,255],
azure:[240,255,255],
beige:[245,245,220],
black:[0,0,0],
blue:[0,0,255],
brown:[165,42,42],
cyan:[0,255,255],
darkblue:[0,0,139],
darkcyan:[0,139,139],
darkgrey:[169,169,169],
darkgreen:[0,100,0],
darkkhaki:[189,183,107],
darkmagenta:[139,0,139],
darkolivegreen:[85,107,47],
darkorange:[255,140,0],
darkorchid:[153,50,204],
darkred:[139,0,0],
darksalmon:[233,150,122],
darkviolet:[148,0,211],
fuchsia:[255,0,255],
gold:[255,215,0],
green:[0,128,0],
indigo:[75,0,130],
khaki:[240,230,140],
lightblue:[173,216,230],
lightcyan:[224,255,255],
lightgreen:[144,238,144],
lightgrey:[211,211,211],
lightpink:[255,182,193],
lightyellow:[255,255,224],
lime:[0,255,0],
magenta:[255,0,255],
maroon:[128,0,0],
navy:[0,0,128],
olive:[128,128,0],
orange:[255,165,0],
pink:[255,192,203],
purple:[128,0,128],
violet:[128,0,128],
red:[255,0,0],
silver:[192,192,192],
white:[255,255,255],
yellow:[255,255,0],
transparent: [255,255,255]
};


$.easing.jswing = $.easing.swing;
$.extend($.easing,
{
def: 'easeOutQuad',
swing: function (x, t, b, c, d) {

return $.easing[$.easing.def](x, t, b, c, d);
},
easeInQuad: function (x, t, b, c, d) {
return c*(t/=d)*t + b;
},
easeOutQuad: function (x, t, b, c, d) {
return -c *(t/=d)*(t-2) + b;
},
easeInOutQuad: function (x, t, b, c, d) {
if ((t/=d/2) < 1) return c/2*t*t + b;
return -c/2 * ((--t)*(t-2) - 1) + b;
},
easeInCubic: function (x, t, b, c, d) {
return c*(t/=d)*t*t + b;
},
easeOutCubic: function (x, t, b, c, d) {
return c*((t=t/d-1)*t*t + 1) + b;
},
easeInOutCubic: function (x, t, b, c, d) {
if ((t/=d/2) < 1) return c/2*t*t*t + b;
return c/2*((t-=2)*t*t + 2) + b;
},
easeInQuart: function (x, t, b, c, d) {
return c*(t/=d)*t*t*t + b;
},
easeOutQuart: function (x, t, b, c, d) {
return -c * ((t=t/d-1)*t*t*t - 1) + b;
},
easeInOutQuart: function (x, t, b, c, d) {
if ((t/=d/2) < 1) return c/2*t*t*t*t + b;
return -c/2 * ((t-=2)*t*t*t - 2) + b;
},
easeInQuint: function (x, t, b, c, d) {
return c*(t/=d)*t*t*t*t + b;
},
easeOutQuint: function (x, t, b, c, d) {
return c*((t=t/d-1)*t*t*t*t + 1) + b;
},
easeInOutQuint: function (x, t, b, c, d) {
if ((t/=d/2) < 1) return c/2*t*t*t*t*t + b;
return c/2*((t-=2)*t*t*t*t + 2) + b;
},
easeInSine: function (x, t, b, c, d) {
return -c * Math.cos(t/d * (Math.PI/2)) + c + b;
},
easeOutSine: function (x, t, b, c, d) {
return c * Math.sin(t/d * (Math.PI/2)) + b;
},
easeInOutSine: function (x, t, b, c, d) {
return -c/2 * (Math.cos(Math.PI*t/d) - 1) + b;
},
easeInExpo: function (x, t, b, c, d) {
return (t==0) ? b : c * Math.pow(2, 10 * (t/d - 1)) + b;
},
easeOutExpo: function (x, t, b, c, d) {
return (t==d) ? b+c : c * (-Math.pow(2, -10 * t/d) + 1) + b;
},
easeInOutExpo: function (x, t, b, c, d) {
if (t==0) return b;
if (t==d) return b+c;
if ((t/=d/2) < 1) return c/2 * Math.pow(2, 10 * (t - 1)) + b;
return c/2 * (-Math.pow(2, -10 * --t) + 2) + b;
},
easeInCirc: function (x, t, b, c, d) {
return -c * (Math.sqrt(1 - (t/=d)*t) - 1) + b;
},
easeOutCirc: function (x, t, b, c, d) {
return c * Math.sqrt(1 - (t=t/d-1)*t) + b;
},
easeInOutCirc: function (x, t, b, c, d) {
if ((t/=d/2) < 1) return -c/2 * (Math.sqrt(1 - t*t) - 1) + b;
return c/2 * (Math.sqrt(1 - (t-=2)*t) + 1) + b;
},
easeInElastic: function (x, t, b, c, d) {
var s=1.70158;var p=0;var a=c;
if (t==0) return b; if ((t/=d)==1) return b+c; if (!p) p=d*.3;
if (a < Math.abs(c)) { a=c; var s=p/4; }
else var s = p/(2*Math.PI) * Math.asin (c/a);
return -(a*Math.pow(2,10*(t-=1)) * Math.sin( (t*d-s)*(2*Math.PI)/p )) + b;
},
easeOutElastic: function (x, t, b, c, d) {
var s=1.70158;var p=0;var a=c;
if (t==0) return b; if ((t/=d)==1) return b+c; if (!p) p=d*.3;
if (a < Math.abs(c)) { a=c; var s=p/4; }
else var s = p/(2*Math.PI) * Math.asin (c/a);
return a*Math.pow(2,-10*t) * Math.sin( (t*d-s)*(2*Math.PI)/p ) + c + b;
},
easeInOutElastic: function (x, t, b, c, d) {
var s=1.70158;var p=0;var a=c;
if (t==0) return b; if ((t/=d/2)==2) return b+c; if (!p) p=d*(.3*1.5);
if (a < Math.abs(c)) { a=c; var s=p/4; }
else var s = p/(2*Math.PI) * Math.asin (c/a);
if (t < 1) return -.5*(a*Math.pow(2,10*(t-=1)) * Math.sin( (t*d-s)*(2*Math.PI)/p )) + b;
return a*Math.pow(2,-10*(t-=1)) * Math.sin( (t*d-s)*(2*Math.PI)/p )*.5 + c + b;
},
easeInBack: function (x, t, b, c, d, s) {
if (s == undefined) s = 1.70158;
return c*(t/=d)*t*((s+1)*t - s) + b;
},
easeOutBack: function (x, t, b, c, d, s) {
if (s == undefined) s = 1.70158;
return c*((t=t/d-1)*t*((s+1)*t + s) + 1) + b;
},
easeInOutBack: function (x, t, b, c, d, s) {
if (s == undefined) s = 1.70158;
if ((t/=d/2) < 1) return c/2*(t*t*(((s*=(1.525))+1)*t - s)) + b;
return c/2*((t-=2)*t*(((s*=(1.525))+1)*t + s) + 2) + b;
},
easeInBounce: function (x, t, b, c, d) {
return c - $.easing.easeOutBounce (x, d-t, 0, c, d) + b;
},
easeOutBounce: function (x, t, b, c, d) {
if ((t/=d) < (1/2.75)) {
return c*(7.5625*t*t) + b;
} else if (t < (2/2.75)) {
return c*(7.5625*(t-=(1.5/2.75))*t + .75) + b;
} else if (t < (2.5/2.75)) {
return c*(7.5625*(t-=(2.25/2.75))*t + .9375) + b;
} else {
return c*(7.5625*(t-=(2.625/2.75))*t + .984375) + b;
}
},
easeInOutBounce: function (x, t, b, c, d) {
if (t < d/2) return $.easing.easeInBounce (x, t*2, 0, c, d) * .5 + b;
return $.easing.easeOutBounce (x, t*2-d, 0, c, d) * .5 + c*.5 + b;
}
});

})(jQuery);

(function($) {
$.effects.drop = function(o) {
return this.queue(function() {

var el = $(this), props = ['position','top','left','opacity'];

var mode = $.effects.setMode(el, o.options.mode || 'hide'); 
var direction = o.options.direction || 'left'; 

$.effects.save(el, props); el.show(); 
$.effects.createWrapper(el); 
var ref = (direction == 'up' || direction == 'down') ? 'top' : 'left';
var motion = (direction == 'up' || direction == 'left') ? 'pos' : 'neg';
var distance = o.options.distance || (ref == 'top' ? el.outerHeight({margin:true}) / 2 : el.outerWidth({margin:true}) / 2);
if (mode == 'show') el.css('opacity', 0).css(ref, motion == 'pos' ? -distance : distance); 

var animation = {opacity: mode == 'show' ? 1 : 0};
animation[ref] = (mode == 'show' ? (motion == 'pos' ? '+=' : '-=') : (motion == 'pos' ? '-=' : '+=')) + distance;

el.animate(animation, { queue: false, duration: o.duration, easing: o.options.easing, complete: function() {
if(mode == 'hide') el.hide(); 
$.effects.restore(el, props); $.effects.removeWrapper(el); 
if(o.callback) o.callback.apply(this, arguments); 
el.dequeue();
}});
});
};
})(jQuery);

(function($) {
$.effects.puff = function(o) {
return this.queue(function() {

var el = $(this);

var options = $.extend(true, {}, o.options);
var mode = $.effects.setMode(el, o.options.mode || 'hide'); 
var percent = parseInt(o.options.percent,10) || 150; 
options.fade = true; 
var original = {height: el.height(), width: el.width()}; 

var factor = percent / 100;
el.from = (mode == 'hide') ? original : {height: original.height * factor, width: original.width * factor};

options.from = el.from;
options.percent = (mode == 'hide') ? percent : 100;
options.mode = mode;

el.effect('scale', options, o.duration, o.callback);
el.dequeue();
});
};
$.effects.scale = function(o) {
return this.queue(function() {

var el = $(this);

var options = $.extend(true, {}, o.options);
var mode = $.effects.setMode(el, o.options.mode || 'effect'); 
var percent = parseInt(o.options.percent,10) || (parseInt(o.options.percent,10) == 0 ? 0 : (mode == 'hide' ? 0 : 100)); 
var direction = o.options.direction || 'both'; 
var origin = o.options.origin; 
if (mode != 'effect') { 
options.origin = origin || ['middle','center'];
options.restore = true;
}
var original = {height: el.height(), width: el.width()}; 
el.from = o.options.from || (mode == 'show' ? {height: 0, width: 0} : original); 

var factor = { 
y: direction != 'horizontal' ? (percent / 100) : 1,
x: direction != 'vertical' ? (percent / 100) : 1
};
el.to = {height: original.height * factor.y, width: original.width * factor.x}; 
if (o.options.fade) { 
if (mode == 'show') {el.from.opacity = 0; el.to.opacity = 1;};
if (mode == 'hide') {el.from.opacity = 1; el.to.opacity = 0;};
};

options.from = el.from; options.to = el.to; options.mode = mode;

el.effect('size', options, o.duration, o.callback);
el.dequeue();
});
};
$.effects.size = function(o) {
return this.queue(function() {

var el = $(this), props = ['position','top','left','width','height','overflow','opacity'];
var props1 = ['position','top','left','overflow','opacity']; 
var props2 = ['width','height','overflow']; 
var cProps = ['fontSize'];
var vProps = ['borderTopWidth', 'borderBottomWidth', 'paddingTop', 'paddingBottom'];
var hProps = ['borderLeftWidth', 'borderRightWidth', 'paddingLeft', 'paddingRight'];

var mode = $.effects.setMode(el, o.options.mode || 'effect'); 
var restore = o.options.restore || false; 
var scale = o.options.scale || 'both'; 
var origin = o.options.origin; 
var original = {height: el.height(), width: el.width()}; 
el.from = o.options.from || original; 
el.to = o.options.to || original; 

if (origin) { 
var baseline = $.effects.getBaseline(origin, original);
el.from.top = (original.height - el.from.height) * baseline.y;
el.from.left = (original.width - el.from.width) * baseline.x;
el.to.top = (original.height - el.to.height) * baseline.y;
el.to.left = (original.width - el.to.width) * baseline.x;
};
var factor = { 
from: {y: el.from.height / original.height, x: el.from.width / original.width},
to: {y: el.to.height / original.height, x: el.to.width / original.width}
};
if (scale == 'box' || scale == 'both') { 
if (factor.from.y != factor.to.y) { 
props = props.concat(vProps);
el.from = $.effects.setTransition(el, vProps, factor.from.y, el.from);
el.to = $.effects.setTransition(el, vProps, factor.to.y, el.to);
};
if (factor.from.x != factor.to.x) { 
props = props.concat(hProps);
el.from = $.effects.setTransition(el, hProps, factor.from.x, el.from);
el.to = $.effects.setTransition(el, hProps, factor.to.x, el.to);
};
};
if (scale == 'content' || scale == 'both') { 
if (factor.from.y != factor.to.y) { 
props = props.concat(cProps);
el.from = $.effects.setTransition(el, cProps, factor.from.y, el.from);
el.to = $.effects.setTransition(el, cProps, factor.to.y, el.to);
};
};
$.effects.save(el, restore ? props : props1); el.show(); 
$.effects.createWrapper(el); 
el.css('overflow','hidden').css(el.from); 

if (scale == 'content' || scale == 'both') { 
vProps = vProps.concat(['marginTop','marginBottom']).concat(cProps); 
hProps = hProps.concat(['marginLeft','marginRight']); 
props2 = props.concat(vProps).concat(hProps); 
el.find("*[width]").each(function(){
child = $(this);
if (restore) $.effects.save(child, props2);
var c_original = {height: child.height(), width: child.width()}; 
child.from = {height: c_original.height * factor.from.y, width: c_original.width * factor.from.x};
child.to = {height: c_original.height * factor.to.y, width: c_original.width * factor.to.x};
if (factor.from.y != factor.to.y) { 
child.from = $.effects.setTransition(child, vProps, factor.from.y, child.from);
child.to = $.effects.setTransition(child, vProps, factor.to.y, child.to);
};
if (factor.from.x != factor.to.x) { 
child.from = $.effects.setTransition(child, hProps, factor.from.x, child.from);
child.to = $.effects.setTransition(child, hProps, factor.to.x, child.to);
};
child.css(child.from); 
child.animate(child.to, o.duration, o.options.easing, function(){
if (restore) $.effects.restore(child, props2); 
}); 
});
};

el.animate(el.to, { queue: false, duration: o.duration, easing: o.options.easing, complete: function() {
if(mode == 'hide') el.hide(); 
$.effects.restore(el, restore ? props : props1); $.effects.removeWrapper(el); 
if(o.callback) o.callback.apply(this, arguments); 
el.dequeue();
}});
});
};
})(jQuery);

(function($) {
$.effects.slide = function(o) {
return this.queue(function() {

var el = $(this), props = ['position','top','left'];

var mode = $.effects.setMode(el, o.options.mode || 'show'); 
var direction = o.options.direction || 'left'; 

$.effects.save(el, props); el.show(); 
$.effects.createWrapper(el).css({overflow:'hidden'}); 
var ref = (direction == 'up' || direction == 'down') ? 'top' : 'left';
var motion = (direction == 'up' || direction == 'left') ? 'pos' : 'neg';
var distance = o.options.distance || (ref == 'top' ? el.outerHeight({margin:true}) : el.outerWidth({margin:true}));
if (mode == 'show') el.css(ref, motion == 'pos' ? -distance : distance); 

var animation = {};
animation[ref] = (mode == 'show' ? (motion == 'pos' ? '+=' : '-=') : (motion == 'pos' ? '-=' : '+=')) + distance;

el.animate(animation, { queue: false, duration: o.duration, easing: o.options.easing, complete: function() {
if(mode == 'hide') el.hide(); 
$.effects.restore(el, props); $.effects.removeWrapper(el); 
if(o.callback) o.callback.apply(this, arguments); 
el.dequeue();
}});
});
};
})(jQuery);
