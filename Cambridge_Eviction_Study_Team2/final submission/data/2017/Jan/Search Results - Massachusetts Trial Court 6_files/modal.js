/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
 
/**
 * Javascript modal window
 * Licensed under the Apache License, Version 2.0
 * @author Matej Knopp
 */

/**
 * In case wicket-ajax.js is not yet loaded, create 
 * Wicket namespace and Wicket.Class.create. 
 */  
if (typeof(Wicket) == "undefined") {
	Wicket = { };
}


if (Wicket.Class == null) {
	Wicket.Class = {
		create: function() {
			return function() {
				this.initialize.apply(this, arguments);
			}
		}
	};
}

if (Wicket.Object == null) {
	Wicket.Object = { };
}

if (Wicket.Object.extend == null) {
	Wicket.Object.extend = function(destination, source) {
		for (property in source) {
			destination[property] = source[property];
		}
		return destination;
	}
}

/**
 * Supporting code for getting mouse move and mouse up events from iframes.
 * The problem when dragging a div with an iframe is that when the mouse cursor
 * gets over an iframe, all mouse events are received by the iframe's document. (IE and FF)
 * 
 * This code can recursively traverse all iframes in document and temporatily forward
 * events from their documents to parent document. 
 */ 
Wicket.Iframe = { 
	
	/**
	 * Returns the horizontal position of given element (in pixels).
	 */
	findPosX: function(e) { 
		if (e.offsetParent) {
			var c = 0;
			while (e.offsetParent) {
				c += e.offsetLeft
				e = e.offsetParent;
			}
			return c;
		} else if (e.x) {
			return e.x;
		} else {
			return 0;
		}	
	},

	/**
	 * Returns the vertical position of given element (in pixels).
	 */	
	findPosY: function(e) {
		if (e.offsetParent) {
			var c = 0;
			while (e.offsetParent) {
				c += e.offsetTop
				e = e.offsetParent;
			}
			return c;
		} else if (e.y) {
			return e.y;
		} else {
			return 0;
		}				
	},

	/**
	 * Forwards the events from iframe to the parent document (works recursively).
	 * @param {Document} doc - document to which the events will be forwardeded   
	 * @param {HTMLElement} iframe - source iframe 
	 * @param {Array} revertList - list to which altered iframes will be added 
	 */
	forwardEvents: function(doc, iframe, revertList) {
		try {
			var idoc = iframe.contentWindow.document;
			idoc.old_onmousemove = idoc.onmousemove;
			idoc.onmousemove = function(evt) {
				if (evt == null)
					evt = iframe.contentWindow.event;
				var e = new Object();						
				
				var dx = 0;
				var dy = 0;				
				if (Wicket.Browser.isIE() || Wicket.Browser.isGecko) {
					dx = Wicket.Window.getScrollX();
					dy = Wicket.Window.getScrollY();
				}
										
				e.clientX = evt.clientX + Wicket.Iframe.findPosX(iframe) - dx;
				e.clientY = evt.clientY + Wicket.Iframe.findPosY(iframe) - dy;		
				doc.onmousemove(e);			
			}	
			idoc.old_onmouseup = idoc.old_onmousemove;
			idoc.onmouseup = function(evt) {
				if (evt == null)
					evt = iframe.contentWindow.event;
				var e = new Object();

				var dx = 0;
				var dy = 0;				
				if (Wicket.Browser.isIE() || Wicket.Browser.isGecko()) {
					dx = Wicket.Window.getScrollX();
					dy = Wicket.Window.getScrollY();
				}
				
				e.clientX = evt.clientX + Wicket.Iframe.findPosX(iframe) - dx;
				e.clientY = evt.clientY + Wicket.Iframe.findPosY(iframe) - dy;			
				doc.onmouseup(e);	
			}	
			revertList.push(iframe);
			Wicket.Iframe.documentFix(idoc, revertList);
		} catch (ignore) {
		}		
	},

	/**
	 * Reverts the changes made to the given iframe.
	 * @param {HTMLElement} iframe
	 */
	revertForward: function(iframe) {
		var idoc = iframe.contentWindow.document;
		idoc.onmousemove = idoc.old_onmousemove;
		idoc.onmouseup = idoc.old_onmouseup;
		idoc.old_onmousemove = null;
		idoc.old_onmouseup = null;
	},

	/**
	 * Forward events from all iframes of the given document (recursive)
	 * @param {Document} doc - document to be fixed
	 * @param {Array} revertList - all affected iframes will be stored here
	 */
	documentFix: function(doc, revertList) {
		var iframes = doc.getElementsByTagName("iframe");	
		for (var i = 0; i < iframes.length; ++i) {
			var iframe = iframes[i];		
			if (iframe.tagName != null)					
				Wicket.Iframe.forwardEvents(doc, iframe, revertList);		
		}
	},

	/**
	 * Reverts the changes made to each iframe in the given array.
	 * @param {Array} revertList
	 */
	documentRevert: function(revertList) {
		for (var i = 0; i < revertList.length; ++i) {
			var iframe = revertList[i];
			Wicket.Iframe.revertForward(iframe);
		}
	}	
}

/**
 * Draggable (and optionally resizable) window that can either hold a div
 * or an iframe. 
 */
Wicket.Window = Wicket.Class.create();

/**
 * Display confirmation dialog if the user is about to leave a page (IE and FF).
 */
Wicket.Window.unloadConfirmation = true;

/**
 * Creates a wicket window instance. The advantage of using this is
 * that in case an iframe modal window is opened in an already displayed 
 * iframe modal window, the new window is created as a top-level window.
 * 
 */
Wicket.Window.create = function(settings) {
	var win;
	
	// if it is an iframe window...
	if (typeof(settings.src) != "undefined" && Wicket.Browser.isKHTML() == false) {
		// attempt to get class crom parent
		try {		
			win = window.parent.Wicket.Window;			
		} catch (ignore) {		
		}
	}
	
	// no parent...
	if (typeof(win) == "undefined") {
		win = Wicket.Window;
	}
	
	// create and return instance
	return new win(settings);
}

/**
 * Returns the current top level window (null if none).
 */
Wicket.Window.get = function() {
	var win = null;
	
	if (typeof(Wicket.Window.current) != "undefined") {
		win = Wicket.Window.current;
	} else 
	{
		try {
			win = window.parent.Wicket.Window.current;
		} catch (ignore) {
		}
	}
	return win;
} 


/**
 * Closes the current wicket open window. This method is supposed to 
 * be called from inside the window (therefore it checks window.parent).
 */
Wicket.Window.close = function() {
	
	var win;
	try {		
		win = window.parent.Wicket.Window;
	} catch (ignore) {		
	}
	
	if (typeof(win) != "undefined" && typeof(win.current) != "undefined") {
		// we can't call close directly, because it will delete our window,
		// so we will schedule it as timeout for parent's window
		window.parent.setTimeout(function() {
			win.current.close();			
		}, 0);
	}
}

Wicket.Window.prototype = { 

	/**
	 * Creates a new window instance.
	 * Note:
	 *   Width refers to the width of entire window (including frame).
	 *   Height refers to the height of user content. 
	 * 
	 * @param {Object} settings - map that contains window settings. the default
	 *                            values are below - together with description
	 */
	initialize: function(settings) {
				
		// override default settings with user settings
		this.settings = Wicket.Object.extend({
			
			minWidth: 200,  /* valid only if resizable */
			minHeight: 150, /* valid only if resizable */
			
			className: "w_blue", /* w_silver */
			
			width: 600,  /* initial width */
			height: 300, /* may be null for non-iframe, non-resizable window (automatic height) */
			
			resizable: true,
			
			widthUnit: "px", /* valid only if not resizable */
			heightUnit: "px", /* valid only if not resizable */
		
			src: null,     /* iframe src - this takes precedence over the "element" property */
			element: null, /* content element (for non-iframe window) */
			
			iframeName: null, /* name of the iframe */				
		
			cookieId: null, /* id of position (and size if resizable) cookie */
		
			title: null, /* window title. if null and window content is iframe, title of iframe document will be used. */
			
			containerId: null, /* CVESVC-2362, ZLiu, 09/27/2017 previous defined div markup ID that will be replaced by real content */
		
			onCloseButton: function() {				
				/* On firefox on Linux, at least, we need to blur() textfields, etc.
				 * to get it to update its DOM model. Otherwise you'll lose any changes
				 * made to the current form component you're editing.
				 */ 
				this.caption.getElementsByTagName("a")[0].focus();
				this.caption.getElementsByTagName("a")[0].blur();
				this.close();
				return false;
			}.bind(this), /* called when close button is clicked */
			
			onClose: function() { }, /* called when window is closed */
		
			mask: "semi-transparent" /* or "transparent" */
			
		}, settings || { });
		
	},
		
	
	/**
	 * Returns true if the window is iframe-based.
	 */
	isIframe: function() {
		return this.settings.src != null;
	},
	
	/**
	 * Creates the DOM elements of the window.
	 */
	createDOM: function() {
		var idWindow = this.newId();
		var idClassElement = this.newId();
		var idCaption = this.newId();
		var idFrame = this.newId();
		var idTop = this.newId();
		var idTopLeft = this.newId();
		var idTopRight = this.newId();
		var idLeft = this.newId();
		var idRight = this.newId();
		var idBottomLeft = this.newId();
		var idBottomRight = this.newId();
		var idBottom = this.newId();
		var idCaptionText = this.newId();
		
		// CVESVC-2362, ZLiu, 09/28/2017 use previous defined element ID
		if (this.settings.containerId != null) {
			idWindow = this.settings.containerId;
		}
		
		var markup = Wicket.Window.getMarkup(idWindow, idClassElement, idCaption, idFrame, 
		             idTop, idTopLeft, idTopRight, idLeft, idRight, idBottomLeft, idBottomRight, 
					 idBottom, idCaptionText, this.isIframe());								
		
		
		var element = document.createElement("div");
		
		// CVESVC-2362, ZLiu, 09/28/2017 Remove previous defined element first
		if (this.settings.containerId != null) {
			var oldEle = document.getElementById(this.settings.containerId);
			if (oldEle != null) {
				var oldParent = oldEle.parentElement;
				if (oldParent != null) {
				 try {
					 oldParent.removeChild(oldEle);
				 } catch (exception) {   }
				}
			}
		}
		
		document.body.appendChild(element);		
		Wicket.replaceOuterHtml(element, markup);
				
		var _ = function(name) { return document.getElementById(name); }
		
		this.window = _(idWindow);
		this.classElement = _(idClassElement);			
		this.caption = _(idCaption);
		this.content = _(idFrame);
		this.top = _(idTop);
		this.topLeft = _(idTopLeft);
		this.topRight = _(idTopRight);
		this.left = _(idLeft);
		this.right = _(idRight);
		this.bottomLeft = _(idBottomLeft);
		this.bottomRight = _(idBottomRight);	
		this.bottom = _(idBottom);
		this.captionText = _(idCaptionText);
				
		if (Wicket.Browser.isIE()) {
			// IE stupid 3px bug - not fixed even in IE7 quirks!
			if (Wicket.Browser.isIE7() == false || Wicket.Browser.isIEQuirks()) {
				this.topLeft.style.marginRight = "-3px";
				this.topRight.style.marginLeft = "-3px";
				this.bottomLeft.style.marginRight = "-3px";
				this.bottomRight.style.marginLeft = "-3px";
			}								
		} 			
		
		// HACK - IE doesn't support position:fixed. Gecko does, however for a reason
		// we need to have background position: absolute, which makes the movement of 
		// the window really jerky if the window stays position: fixed
		if (Wicket.Browser.isIE() || Wicket.Browser.isGecko()) {
			this.window.style.position = "absolute";
		}
		
		// fix the cursors
		if (this.settings.resizable == false) {
			this.top.style.cursor =  this.topLeft.style.cursor = this.topRight.style.cursor =
			this.bottom.style.cursor = this.bottomLeft.style.cursor = this.bottomRight.style.cursor = 
			this.left.style.cursor = this.right.style.cursor = "default";
		}				
	},

	/**
	 * Creates the new uniqe id for window element.
	 */ 
	newId: function() {
		return "_wicket_window_" + Wicket.Window.idCounter++;
	},
	
	
	/**
	 * Binds the handler to the drag event on given element.
	 */
	bind: function(element, handler) {
		Wicket.Drag.init(element, this.onBegin.bind(this), this.onEnd.bind(this), handler.bind(this)); 
	},

	/**
	 * Unbinds the handler from a drag event on given element.
	 */	
	unbind: function(element) {
		Wicket.Drag.clean(element);
	},
	
	/**
	 * Binds the event handlers to the elements.
	 */
	bindInit: function() {
		this.bind(this.caption, this.onMove);
		
		if (this.settings.resizable) {		
			this.bind(this.bottomRight, this.onResizeBottomRight);
			this.bind(this.bottomLeft, this.onResizeBottomLeft);
			this.bind(this.bottom, this.onResizeBottom);
			this.bind(this.left, this.onResizeLeft);
			this.bind(this.right, this.onResizeRight);
			this.bind(this.topLeft, this.onResizeTopLeft);		
			this.bind(this.topRight, this.onResizeTopRight);
			this.bind(this.top, this.onResizeTop);
		} else {
			this.bind(this.bottomRight, this.onMove);
			this.bind(this.bottomLeft, this.onMove);
			this.bind(this.bottom, this.onMove);
			this.bind(this.left, this.onMove);
			this.bind(this.right, this.onMove);
			this.bind(this.topLeft, this.onMove);		
			this.bind(this.topRight, this.onMove);
			this.bind(this.top, this.onMove);
		}	
				
		this.caption.getElementsByTagName("a")[0].onclick = this.settings.onCloseButton.bind(this);
	},

	/**
	 * Unbinds the event handlers.
	 */
	bindClean: function() {				
		this.unbind(this.caption);
		this.unbind(this.bottomRight);
		this.unbind(this.bottomLeft);
		this.unbind(this.bottom);
		this.unbind(this.left);
		this.unbind(this.right);
		this.unbind(this.topLeft);		
		this.unbind(this.topRight);
		this.unbind(this.top);
		
		this.caption.getElementsByTagName("a")[0].onclick = null;
	},
	
	/**
	 * Returns the content document
	 */
	getContentDocument: function() {
		if (this.isIframe() == true) {
			return this.content.contentWindow.document;
		} else {
			return document;
		}
	},

	/**
	 * Places the window to the center of the viewport.
	 */	
	center: function() {
		var scTop = 0;
		var scLeft = 0;

		if (Wicket.Browser.isIE() || Wicket.Browser.isGecko()) 	{
			scLeft = Wicket.Window.getScrollX();
			scTop = Wicket.Window.getScrollY();
		}
		
		var width = Wicket.Window.getViewportWidth();
		var height = Wicket.Window.getViewportHeight();
		
		var modalWidth = this.window.offsetWidth;
		var modalHeight = this.window.offsetHeight;
		
		if (modalWidth > width - 10) { 
			this.window.style.width = (width - 10) + "px"; 
			modalWidth = this.window.offsetWidth; 
		} 
		if (modalHeight > height - 40) { 
			this.content.style.height = (height - 40) + "px"; 
			modalHeight = this.window.offsetHeight; 
		} 
		
		var left = (width / 2) - (modalWidth / 2) + scLeft;
		var top = (height / 2) - (modalHeight / 2) + scTop;
		if (left < 0) left = 0;
		if (top < 0) top = 0;
		
		this.window.style.left = left + "px";
		this.window.style.top = top + "px";
	},
	
	cookieKey: "wicket-modal-window-positions",
	cookieExp: 31,
	
	findPositionString: function(remove) {
		var cookie = Wicket.Cookie.get(this.cookieKey);
	
		var entries = cookie != null ? cookie.split("|") : new Array();
		
		for (var i = 0; i < entries.length; ++i) {
			if (entries[i].indexOf(this.settings.cookieId + "::") == 0) {
				var string = entries[i];
				if (remove) {
					entries.splice(i, 1);					
					Wicket.Cookie.set(this.cookieKey, entries.join("|"), this.cookieExp);
										
				}
				return string;
			}
		}
		return null;
	},
	
	/**
	 * Saves the position (and size if resizable) as a cookie.
	 */
	savePosition: function() {
	   this.savePositionAs(this.window.style.left, this.window.style.top, this.window.style.width, this.content.style.height);
	},
	
	savePositionAs: function(x, y, width, height) {
		if (typeof(this.settings.cookieId) != "undefined" &&  this.settings.cookieId != null) {
	
			this.findPositionString(true);
			
			if (cookie == null || cookie.length == 0)
				cookie = "";
			else
				cookie = cookie + "|";
			
			var cookie = this.settings.cookieId;
			cookie += "::";
			
			cookie += x + ",";
			cookie += y + ",";
			cookie += width + ",";
			cookie += height;
					
			var rest = Wicket.Cookie.get(this.cookieKey);
			if (rest != null) {
				cookie += "|" + rest;
			}
			Wicket.Cookie.set(this.cookieKey, cookie, this.cookieExp);
			
		};
	},
	
	/**
	 * Restores the position (and size if resizable) from the cookie.
	 */
	loadPosition: function() {
		if (typeof(this.settings.cookieId) != "undefined" && this.settings.cookieId != null) {
			
			var string = this.findPositionString(false);
			
			if (string != null) {
				var array = string.split("::");
				var positions = array[1].split(",");
				if (positions.length == 4) {					
					this.window.style.left = positions[0];
					this.window.style.top = positions[1];
					this.window.style.width = positions[2];
					this.content.style.height = positions[3];
				}
			}
		}
	},
	
	
	/**
	 * Creates the mask accordingly to the settings.
	 */
	createMask: function() {
		if (this.settings.mask == "transparent")
			this.mask = new Wicket.Window.Mask(true);
		else if (this.settings.mask == "semi-transparent")
			this.mask = new Wicket.Window.Mask(false);
						
		if (typeof(this.mask) != "undefined") {
			this.mask.show();
		}		
	},
	
	/**
	 * Destroys the mask.
	 */
	destroyMask: function() {
		this.mask.hide();	
		this.mask = null;
	},
	
	/**
	 * Loads the content 
	 */
	load: function() {
		if (this.settings.title == null)
			this.update = window.setInterval(this.updateTitle.bind(this), 100);

		// opera seems to have problem accessing contentWindow here
		if (Wicket.Browser.isOpera()) {
			this.content.onload = function() {
				this.content.contentWindow.name = this.settings.iframeName;
			}.bind(this);
		} else {
			this.content.contentWindow.name = this.settings.iframeName;
		}
		
		try
		{
			this.content.contentWindow.location.replace(this.settings.src);
		}
		catch(ignore)
		{
			this.content.src = this.settings.src;
		}		
	},
	
	/**
	 * Shows the window. 
	 */
	show: function() {					
		
		// create the DOM elements
		this.createDOM();
		
		// set the class of window (blue or silver by default)
		this.classElement.className = this.settings.className;
		
		// is it an iframe window?
		if (this.isIframe()) {
			// load the file
			this.load();
		} else {
			// it's an element content
			
			// is the element specified?
			if (this.settings.element == null) {
				throw "Either src or element must be set.";
			}
			
			// reparent the element
			this.oldParent = this.settings.element.parentNode;
			this.settings.element.parentNode.removeChild(this.settings.element);
			this.content.appendChild(this.settings.element);
			
			// set the overflow style so that scrollbars are shown when the element is bigger than window
			this.content.style.overflow="auto";
		}
		
		// bind the events
		this.bindInit();

		// if the title is specified set it
		if (this.settings.title != null)
			this.captionText.innerHTML = this.settings.title;


		// initial width and height
		this.window.style.width = this.settings.width + (this.settings.resizable ? "px" : this.settings.widthUnit);
		
		if (this.settings.height != null)
			this.content.style.height = this.settings.height + (this.settings.resizable ? "px" : this.settings.heightUnit);

		// center the window
		this.center();
		
		// load position from cookie
		this.loadPosition();

		var doShow = function() {
			this.adjustOpenWindowZIndexesOnShow();
			this.window.style.visibility="visible";
			
		}.bind(this);
				
		this.adjustOpenWindowsStatusOnShow();

		// show the window
		if (Wicket.Browser.isGecko() && this.isIframe()) {
			// HACK
			// gecko flickers when showing the window
			// unless the showing is postponed a little
			window.setTimeout(function() { doShow(); }, 0);
		} else {
			doShow();
		}

		// if the content supports focus and blur it, which means
		// that the already focused element will lose it's focus
		if (this.content.focus) {
			this.content.focus();
			this.content.blur();
		}
		// preserve old unload hanler
		this.old_onunload = window.onunload;
		
		// new unload handler - close the window to prevent memory leaks in ie
		window.onunload = function() {
			this.close(true);
			if (this.old_onunload != null)
				return this.old_onunload();
		}.bind(this);
		
		// preserve old beforeunload handler
		this.old_onbeforeunload = window.onbeforeunload;
		
		if (Wicket.Window.unloadConfirmation == true) {
			// new beforeunload handler - ask user before reloading window
			window.onbeforeunload = function() {
				return "Reloading this page will cause the modal window to disappear.";
			}
		}
		
		// create the mask that covers the background
		this.createMask();
		
		// CVESVC-2362, ZLiu, 09/28/2017 set focus on the opened content
		if (this.settings.containerId != null) {
			var contentEle = document.getElementById(this.settings.containerId);
			if (contentEle != null) {
				contentEle.focus();
			}
		}
	},
	
	adjustOpenWindowZIndexesOnShow: function() {
		// if there is a previous window
		if ((this.oldWindow != null) && (typeof(this.oldWindow) != "undefined")) {
			// lower it's z-index so that it's moved under the mask
			this.oldWindow.window.style.zIndex = Wicket.Window.Mask.zIndex - 1;
		}
	},
	
	adjustOpenWindowsStatusOnShow: function() {
		// is there a window displayed already?
		if (Wicket.Window.current != null) {
			// save the reference to it
			this.oldWindow = Wicket.Window.current;
		}
		// keep reference to this window
		Wicket.Window.current = this;
	},
	
	/**
	 * Returns true if the window can be closed.
	 */
	canClose: function() {
		return true;
	},
	
	/**
	 * Prevent user from closing the window if there's another (nested) modal window in the iframe. 
	 */
	canCloseInternal: function() {
		try {
			if (this.isIframe() == true) {
				var current = this.content.contentWindow.Wicket.Window.current;
				if (typeof(current) != "undefined" && current != null) {
					alert('You can\'t close this modal window. Close the top-level modal window first.');
					return false;
				}
			}
		} catch (ignore) {
		}
		return true;
	},
	
	/**
	 * Closes the window.
	 * @param {Boolean} force - internal argument 
	 */
	close: function(force) {
							
		// can user close the window?
		if (force != true && (!this.canClose() || !this.canCloseInternal()))
			return;		
		
		// if the update handler was set clean it
		if (typeof(this.update) != "undefined")
			window.clearInterval(this.update);

		// clean event bindings
		this.bindClean();
		
		// hide elements
		this.window.style.display = "none";		
		
		// if the window has a div content, the div is reparented to it's old parent 
		if (typeof(this.oldParent) != "undefined") {		
			try {	
				this.content.removeChild(this.settings.element);
				this.oldParent.appendChild(this.settings.element);
				this.oldParent = null;
			} catch (ignore) {
			}
		}
		
		// remove the elements from document
		this.window.parentNode.removeChild(this.window);
		
		// clean references to elements
		this.window = this.classElement = this.caption = this.bottomLeft = this.bottomRight = this.bottom =
		this.left = this.right = this.topLeft = this.topRight = this.top = this.captionText = null;
					
		// restore old unload handler					
		window.onunload = this.old_onunload;
		this.old_onunload = null;			
		
		// restore old beforeunload handler
		window.onbeforeunload = this.old_onbeforeunload;
		this.old_onbeforeunload = null;
		
		// hids and cleanup the mask
		this.destroyMask();
		
		if (force != true) {
			// call onclose handler
			this.settings.onClose();
		}

		this.adjustOpenWindowsStatusAndZIndexesOnClose();
		
		if (Wicket.Browser.isIE()) {
			// There's a strange focus problem in IE that disables focus on entire page,
			// unless something focuses an input
			var e = document.createElement("input");
			var x = Wicket.Window.getScrollX();
			var y = Wicket.Window.getScrollY();
			e.style.position = "absolute";
			e.style.left = x + "px";
			e.style.top = y + "px";
			document.body.appendChild(e);
			e.focus();
			document.body.removeChild(e);
		}						
	},
	
	adjustOpenWindowsStatusAndZIndexesOnClose: function() {
		// if there was a window shown before this one
		if (this.oldWindow != null) {
			// set the old as current
			Wicket.Window.current = this.oldWindow;
			// increase it's z-index so that it's moved above the mask
			Wicket.Window.current.window.style.zIndex = Wicket.Window.Mask.zIndex + 1;
			this.oldWindow = null; 
		} else {
			// remove reference to the window
			Wicket.Window.current = null;
		}
	},
	
	/**
	 * Cleans the internal state of the window
	 */
	destroy: function() {
		this.settings = null;
	},
	
		
	/**
	 * If the window is Iframe, updates the title with iframe's document title.
	 */
	updateTitle: function() {		
		try {			
			if (this.content.contentWindow.document.title != null) {
				if (this.captionText.innerHTML != this.content.contentWindow.document.title) {													
					this.captionText.innerHTML = this.content.contentWindow.document.title;
					
					// konqueror doesn't refresh caption text properly
					if (Wicket.Browser.isKHTML()) {
						this.captionText.style.display = 'none';
						window.setTimeout(function() { this.captionText.style.display="block";}.bind(this), 0);
					}

				}
			}
		} catch (ignore) {
				Wicket.Log.info(ignore);
		}
	},


	/**
	 * Called when dragging has started. 
	 */
	onBegin: function(object) {
		if (this.isIframe() && (Wicket.Browser.isGecko() || Wicket.Browser.isIE())) {
			this.revertList = new Array();				
			Wicket.Iframe.documentFix(document, this.revertList);
		}			 			 			
	},
	
	/**
	 * Called when dragging has ended.
	 */
	onEnd: function(object) {
		if (typeof(this.revertList) != "undefined" && this.revertList != null) {
			Wicket.Iframe.documentRevert(this.revertList); 
			this.revertList = null;
			if (Wicket.Browser.isKHTML() || this.content.style.visibility=='hidden') {			
				this.content.style.visibility='hidden';
				window.setTimeout(function() { this.content.style.visibility='visible'; }.bind(this),  0 );
			}
			this.revertList = null;
		}
						
		this.savePosition();
	},

	/**
	 * Called when window is moving (draggin the caption).	 
	 */	
	onMove: function(object, deltaX, deltaY) {
		var w = this.window;
		this.left_ = parseInt(w.style.left, 10) + deltaX;
		this.top_ = parseInt(w.style.top, 10) + deltaY;
		
		if (this.left_ < 0)
			this.left_ = 0;
		if (this.top_ < 0)
			this.top_ = 0;							
			
		w.style.left = this.left_ + "px";
		w.style.top = this.top_ + "px";
		
		this.moving();
	},
	
	/**
	 * Called when window is being moved
	 */
	moving: function() {
	},
	
	/**
	 * Called when window is resizing.
	 */
	resizing: function() {	
	},	
	
	/**
	 * Ensures that the size of window is not smaller than minimal size.
	 */
	clipSize : function(swapX, swapY) {
		this.res = [0, 0];

		if (this.width < this.settings.minWidth) {
			this.left_ -= this.settings.minWidth - this.width;
			this.res[0] = this.settings.minWidth - this.width;
			this.width = this.settings.minWidth;
		}
		
		if (this.height < this.settings.minHeight) {
			this.top_ -= this.settings.minHeight - this.height;
			this.res[1] = this.settings.minHeight - this.height;
			this.height = this.settings.minHeight;
		}
		
		if (swapX == true)
			this.res[0] = -this.res[0];
		if (swapY == true)
			this.res[1] = -this.res[1];
	},
	
	//
	// These methods are handlers for parts of window frame
	//
	
	onResizeBottomRight: function(object, deltaX, deltaY) {
		var w = this.window;
		var f = this.content;
		
		this.width = parseInt(w.style.width, 10) + deltaX;
		this.height = parseInt(f.style.height, 10) + deltaY;
								
		this.clipSize();											
											
		w.style.width = this.width + "px";
		f.style.height = this.height + "px";
		
		this.resizing();
		
		return this.res;
	},
	
	onResizeBottomLeft: function(object, deltaX, deltaY) {
		var w = this.window;
		var f = this.content;
		
		this.width = parseInt(w.style.width, 10) - deltaX;
		this.height = parseInt(f.style.height, 10) + deltaY;
		this.left_ = parseInt(w.style.left, 10) + deltaX;
		
		this.clipSize(true);
		
		w.style.width = this.width + "px";
		w.style.left = this.left_ + "px";
		f.style.height = this.height  + "px";
		
		this.moving();
		this.resizing();

		return this.res;
	},	
	
	onResizeBottom: function(object, deltaX, deltaY) {
		var f = this.content;					
		this.height = parseInt(f.style.height, 10) + deltaY;
		
		this.clipSize();
					
		f.style.height = this.height + "px";
		
		this.resizing();
		
		return this.res;			
	},

	onResizeLeft: function(object, deltaX, deltaY) {
		var w = this.window;

		this.width = parseInt(w.style.width, 10) - deltaX;
		this.left_ = parseInt(w.style.left, 10) + deltaX;
		
		this.clipSize(true);
		
		w.style.width = this.width + "px";
		w.style.left = this.left_ + "px";
		
		this.moving();
		this.resizing();
		
		return this.res;
	},

	onResizeRight: function(object, deltaX, deltaY) {
		var w = this.window;
		
		this.width = parseInt(w.style.width, 10) + deltaX;
		
		this.clipSize();
											
		w.style.width = this.width + "px";

		this.resizing();
			
		return this.res;
	},

	onResizeTopLeft: function(object, deltaX, deltaY) {
		var w = this.window;
		var f = this.content;
		
		this.width = parseInt(w.style.width, 10) - deltaX;
		this.height = parseInt(f.style.height, 10) - deltaY;
		this.left_ = parseInt(w.style.left, 10) + deltaX;
		this.top_ =  parseInt(w.style.top, 10) + deltaY;
		
		this.clipSize(true, true);
		
		w.style.width = this.width + "px";
		w.style.left = this.left_ + "px";
		f.style.height = this.height  + "px";
		w.style.top = this.top_ + "px";
		
		this.moving();
		this.resizing();
									
		return this.res;
	},	

	onResizeTopRight: function(object, deltaX, deltaY) {
		var w = this.window;
		var f = this.content;
		
		this.width = parseInt(w.style.width, 10) + deltaX;
		this.height = parseInt(f.style.height, 10) - deltaY;
		this.top_ = parseInt(w.style.top, 10) + deltaY;
		
		this.clipSize(false, true);
		
		w.style.width = this.width + "px";
		f.style.height = this.height  + "px";
		w.style.top = this.top_ + "px";
		
		this.moving();
		this.resizing();
						
		return this.res;
	},	
	
	onResizeTop: function(object, deltaX, deltaY) {
		var f = this.content;
		var w = this.window;
		
		this.height = parseInt(f.style.height, 10) - deltaY;
		this.top_ = parseInt(w.style.top, 10) + deltaY;
		
		this.clipSize(false, true);
		
		f.style.height = this.height  + "px";
		w.style.top = this.top_ + "px";
		
		this.moving();
		this.resizing();
						
		return this.res;
	}
}

/**
 * Counter for generating unique component ids.
 */
Wicket.Window.idCounter = 0;

/**
 * Returns the modal window markup with specified element identifiers.
 */
Wicket.Window.getMarkup = function(idWindow, idClassElement, idCaption, idContent, idTop, idTopLeft, idTopRight, idLeft, idRight, idBottomLeft, idBottomRight, idBottom, idCaptionText, isFrame) {
	var s =
			"<div class=\"wicket-modal\" id=\""+idWindow+"\" tabindex=\"-1\" aria-live=\"assertive\" aria-atomic=\"true\" aria-relevant=\"all\" style=\"top: 10px; left: 10px; width: 100px;\"><form style='background-color:transparent;padding:0px;margin:0px;border-width:0px;position:static'>"+
			"<div id=\""+idClassElement+"\">"+
				
				"<div class=\"w_top_1\">"+

				"<div class=\"w_topLeft\" id=\""+idTopLeft+"\">"+
				"</div>"+				

				"<div class=\"w_topRight\" id=\""+idTopRight+"\">"+
				"</div>"+

				"<div class=\"w_top\" id='"+idTop+"'>"+									
				"</div>"+

				"</div>"+
								
				"<div class=\"w_left\" id='"+idLeft+"'>"+
					"<div class=\"w_right_1\">"+
						"<div class=\"w_right\" id='"+idRight+"'>"+
							"<div class=\"w_content_1\" onmousedown=\"if (Wicket.Browser.isSafari()) { event.ignore = true; }  else { Wicket.stopEvent(event); } \">"+																			
								"<div class=\"w_caption\"  id=\""+idCaption+"\">"+
									"<a class=\"w_close\" href=\"#\"><span class=\"visually-hidden\">close</span></a>"+									
									"<span id=\""+idCaptionText+"\" class=\"w_captionText\"></span>"+
								"</div>"+
							
								"<div class=\"w_content_2\">"+
								"<div class=\"w_content_3\">"+
		 							"<div class=\"w_content\">";
				if (isFrame) {
					s+= "<iframe";
					if (Wicket.Browser.isIELessThan7()) {
						s+= " src=\"about:blank\""
 					}
					s+= " frameborder=\"0\" id=\""+idContent+"\" allowtransparency=\"false\" style=\"height: 200px\" class=\"wicket_modal\"></iframe>";
				} else {
					s+=
										"<div id='"+idContent+"' class='w_content_container'></div>";
				}
					s+= 						
									"</div>"+
								"</div>"+
								"</div>"+
							"</div>"+
						"</div>"+
					"</div>"+
				"</div>"+


				"<div class=\"w_bottom_1\" id=\""+idBottom+"\">"+					
					
					"<div class=\"w_bottomRight\"  id=\""+idBottomRight+"\">"+
					"</div>"+
					
					"<div class=\"w_bottomLeft\" id=\""+idBottomLeft+"\">"+
					"</div>"+

					"<div class=\"w_bottom\" id=\""+idBottom+"1\">"+				
					"</div>"+				


				"</div>"+				


			"</div>"+
		"</form></div>";
		
		return s;
}
	

/**
 * Transparent or semi-transparent masks that prevents user from interacting
 * with the portion of page behind a window.  
 */
Wicket.Window.Mask = Wicket.Class.create();

Wicket.Window.Mask.zIndex = 20000;

Wicket.Window.Mask.prototype = {
			
	/**
	 * Creates the mask.
	 * Created mask is not visible immediately. You have to call <code>show()</code> to
	 * make it visible.
	 * @param {boolean} transparent - whether the mask should be transparent (true) or 
	 *                                semi-transparent (false).
	 */
	initialize: function(transparent) {
		this.transparent = transparent;		
	},
	
	/**
	 * Shows the mask.
	 */
	show: function() {				
		
		// if the mask is not alrady shown...
		if (typeof(Wicket.Window.Mask.element) == "undefined" ||
			Wicket.Window.Mask.element == null) {		
		
			// crate the mask element and add  it to document
			var e = document.createElement("div");
			document.body.appendChild(e);							
			
			// set the proper css class name 
			if (this.transparent) {
				e.className = "wicket-mask-transparent";
			} else {
				e.className = "wicket-mask-dark";
			}					
		
			e.style.zIndex = Wicket.Window.Mask.zIndex;

			// HACK - KHTML doesn't support colors with alpha transparency
			// if the mask is not transparent we have to either
			// make the background image visible (setting color to transparent) - for KHTML
			// or make the background-image invisible (setting it to null) - for other browsers												
			if (this.transparent == false) {
				if (Wicket.Browser.isKHTML() == false) {			
					e.style.backgroundImage = "none";
				} else {
					e.style.backgroundColor = "transparent";
				}
			}

			// HACK - it really sucks that we have to set this to absolute even for gecko.
			// however background with position:fixed makes the text cursor in textfieds
			// in modal window disappear
			if (Wicket.Browser.isIE() || Wicket.Browser.isGecko()) {
				e.style.position = "absolute";
			}

			// set the element							 							
			this.element = e;
					
			// preserver old handlers
			this.old_onscroll = window.onscroll;
			this.old_onresize = window.onresize;
			
			// set new handlers
			window.onscroll = this.onScrollResize.bind(this);
			window.onresize = this.onScrollResize.bind(this);
			
			// fix the mask position
			this.onScrollResize(true);
						
			// set a static reference to mask
			Wicket.Window.Mask.element = e;			
		} else {
			// mask is already shown - don't hide it
			this.dontHide = true; 			
		}
		
		this.shown=true;
		this.focusDisabled=false;
				
		this.disableCoveredContent();
	},
	
	/**
	 * Hides the mask.
	 */
	hide: function() {			

		// cancel any pending tasks
		this.cancelPendingTasks();
		
		// if the mask is visible and we can hide it
		if (typeof(Wicket.Window.Mask.element) != "undefined" && typeof(this.dontHide) == "undefined") {
	
			// remove element from document	
			document.body.removeChild(this.element);
			this.element = null;
			
			// restore old handlers
			window.onscroll = this.old_onscroll;
			window.onresize = this.old_onresize;
						
			Wicket.Window.Mask.element = null;
		}
		
		this.shown=false;
		
		this.reenableCoveredContent();
		
	},
	
	// disable user interaction for content that is covered by the mask
	disableCoveredContent: function() {
		var doc = document;
		var old = Wicket.Window.current.oldWindow;
		if (typeof(old) != "undefined" && old != null) {
			doc = old.getContentDocument();
		}

		this.doDisable(doc, Wicket.Window.current);
	},
	
	tasks: [],
	startTask: function (fn, delay) {
		var taskId=setTimeout(function() { fn(); this.clearTask(taskId); }.bind(this), delay);
		this.tasks.push(taskId);
	},
	clearTask: function (taskId) {
		var index=-1;
		for (var i=0;i<this.tasks.length;i++) {
			if (this.tasks[i]==taskId) {
				index=i;break;
			}
		}
		if (index>=0) {
			this.tasks.splice(index,1);
		}
	},
	cancelPendingTasks: function() {
		while (this.tasks.length>0) {
			var taskId=this.tasks.shift();
			clearTimeout(taskId);
		}
	},
	
	// disable user interaction for content that is covered by the mask inside the given document, taking into consideration that this modal window is or not in an iframe
	// and has the given content
	doDisable: function(doc, win) {
		this.startTask(function() {this.hideSelectBoxes(doc, win)}.bind(this), 300);
		this.startTask(function() {this.disableTabs(doc, win)}.bind(this), 400);
		this.startTask(function() {this.disableFocus(doc, win)}.bind(this), 1000);
	},
	
	// reenable user interaction for content that was covered by the mask
	reenableCoveredContent: function() {
		// show old select boxes (ie only)
		this.showSelectBoxes();

		// restore tab order
		this.restoreTabs();

		// revert onfocus handlers
		this.enableFocus();
	},
	
	/**
	 * Used to update the position (ie) and size (ie, opera) of the mask.
	 */
	onScrollResize: function(dontChangePosition) {							
		// if the iframe is not position:fixed fix it's position
		if (this.element.style.position == "absolute") {
		
			var w = Wicket.Window.getViewportWidth();
			var h = Wicket.Window.getViewportHeight();
	
			var scTop = 0;
			var scLeft = 0;	 	
	 
 			scLeft = Wicket.Window.getScrollX();
			scTop = Wicket.Window.getScrollY();
	 		
			this.element.style.top = scTop + "px";
			this.element.style.left = scLeft + "px";
	
			if (document.all) { // opera or explorer
				this.element.style.width = w;
			}	
			this.element.style.height = h;		
		} 		
	},

	/**
	 * Returns true if 'element' is a child (anywhere in hierarchy) of 'parent'
	 */ 
	isParent: function(element, parent) {		
		if (element.parentNode == parent)
			return true;
		if (typeof(element.parentNode) == "undefined" ||
			element.parentNode == document.body)
			return false;
		return this.isParent(element.parentNode, parent);			
	},


	/**
	 * For internet explorer hides the select boxes (because they
	 * have always bigger z-order than any other elements).
	 */
	hideSelectBoxes : function(doc, win) {				
		if (!this.shown) {
			return;
		}
		
		if (Wicket.Browser.isIE() && Wicket.Browser.isIE7() == false) {
			this.boxes = new Array();
			var selects = doc.getElementsByTagName("select");
			for (var i = 0; i < selects.length; i++) {				
				var element = selects[i];
				
				// if this is not an iframe window and the select is child of window content,
				// don't hide it					
				if (win.isIframe() == false && this.isParent(element, win.content)) {
					continue;
				}				
				
				if (element.style.visibility != "hidden") {
					element.style.visibility = "hidden";
					this.boxes.push(element);
				}				
			}
		}
	},
	
	/**
	 * Shows the select boxes if they were hidden. 
	 */
	showSelectBoxes: function() {
		if (typeof (this.boxes) != "undefined") {
			for (var i = 0; i < this.boxes.length; ++i) {
				var element = this.boxes[i];
				element.style.visibility="visible";
			}
			this.boxes = null;
		}		
	},
	
	/**
	 * Disable focus on element and all it's children.	 
	 */
	disableFocusElement: function(element, revertList, win) {
				
		if (typeof(win) != "undefined" &&
			win != null &&
			win.window != element) {								
				
			revertList.push([element, element.onfocus]);
			element.onfocus = function() { element.blur(); }			
			
			for (var i = 0; i < element.childNodes.length; ++i) {
				this.disableFocusElement(element.childNodes[i], revertList, win);
			}
		}
	},
	
	/**
	 * Disable focus on all elements in document
	 */
	disableFocus: function(doc, win) {
		if (!this.shown) {
			return;
		}
		// explorer doesn't need this, because for IE disableTabs() is called.
		// plus in IE this causes problems because it scrolls document		);
		if (Wicket.Browser.isIE() == false) {			
			this.focusRevertList = new Array();			
			var body = doc.getElementsByTagName("body")[0];			
			for (var i = 0; i < body.childNodes.length; ++i) {		
				this.disableFocusElement(body.childNodes[i], this.focusRevertList, win);
			}
		}
		this.focusDisabled=true;
	},
	
	/**
	 * Enables focus on all elements where the focus has been disabled.
	 */
	enableFocus: function() {
		if (this.focusDisabled==false) {
			return;
		}
		
		if (typeof(this.focusRevertList) != "undefined") {						
			for (var i = 0; i < this.focusRevertList.length; ++i) {
				var item = this.focusRevertList[i];
				item[0].onfocus = item[1];
			}
		}
		this.focusRevertList = null;
	},	
	
	
	/**
	 * Disable tab indexes (ie).
	 */
	disableTabs: function (doc, win) {
		if (!this.shown) {
			return;
		}
		
		if (typeof (this.tabbableTags) == "undefined") this.tabbableTags = new Array("A","BUTTON","TEXTAREA","INPUT","IFRAME", "SELECT");
		if (Wicket.Browser.isIE()) {
			this.disabledTabsRevertList = new Array();
			for (var j = 0; j < this.tabbableTags.length; j++) {
				var tagElements = doc.getElementsByTagName(this.tabbableTags[j]);
				for (var k = 0 ; k < tagElements.length; k++) {
					// if this is not an iframe window and the element is child of window content,
					// don't disable tab on it
					if (win.isIframe() == true || this.isParent(tagElements[k], win.content) == false) {
						var element = tagElements[k];
						element.hiddenTabIndex = element.tabIndex;
						element.tabIndex="-1";
						this.disabledTabsRevertList.push(element);
					}
				}
			}
		}
	},

	/**
	 * Restore tab indexes if they were disabled.
	 */
	restoreTabs: function() {
		if (typeof (this.disabledTabsRevertList) != "undefined" && this.disabledTabsRevertList != null) {
			for (var i = 0; i < this.disabledTabsRevertList.length; ++i) {
				var element = this.disabledTabsRevertList[i];
				if (typeof(element.hiddenTabIndex) != 'undefined') {
					element.tabIndex = element.hiddenTabIndex;
					try { delete element.hiddenTabIndex; } catch (e) { element.hiddenTabIndex = undefined; }
				}
			}
			this.disabledTabsRevertList = null;
		}
	}

}

/**
 * Returns the height of visible area.
 */
Wicket.Window.getViewportHeight = function() {
	if (typeof(window.innerHeight) != "undefined") 
		return window.innerHeight;
	
	if (document.compatMode == 'CSS1Compat') 
		return document.documentElement.clientHeight;
		
	if (document.body) 
		return document.body.clientHeight;
		 
	return undefined; 
}

/**
 * Returns the width of visible area.
 */
Wicket.Window.getViewportWidth =  function() {
	if (typeof(window.innerWidth) != "undefined") 
		return window.innerWidth;
		 
	if (document.compatMode == 'CSS1Compat') 
		return document.documentElement.clientWidth; 
		
	if (document.body) 
		return document.body.clientWidth;
		 
	return undefined;
}

/**
 * Returns the horizontal scroll offset
 */
Wicket.Window.getScrollX = function() {
	var iebody = (document.compatMode && document.compatMode != "BackCompat") ? document.documentElement : document.body	
	return document.all? iebody.scrollLeft : pageXOffset
}

/**
 * Returns the vertical scroll offset
 */
Wicket.Window.getScrollY = function() {
	var iebody = (document.compatMode && document.compatMode != "BackCompat") ? document.documentElement : document.body	
	return document.all? iebody.scrollTop : pageYOffset
}

/**
 * Convenience methods for getting and setting cookie values.
 */
Wicket.Cookie = {	

	/**
	 * Returns the value for cookie of given name.
	 * @param {String} name - name of cookie
	 */
	get: function(name) {
		if (document.cookie.length > 0) {
			var start = document.cookie.indexOf (name + "=");
  			if (start != -1) { 
				start = start + name.length + 1;
				end = document.cookie.indexOf(";", start);
				if (end == -1) { 
					end = document.cookie.length;
				}
				return unescape(document.cookie.substring(start,end))
			}
  		} else {
			return null
		}
	},

	/**
	 * Sets the value for cookie of given name.
	 * @param {Object} name - name of cookie
	 * @param {Object} value - new value
	 * @param {Object} expiredays - how long will the cookie be persisted
	 */
	set: function(name, value, expiredays) {
		var exdate = new Date();
		exdate.setDate(exdate.getDate() + expiredays);
		document.cookie = name + "=" + escape(value) + ((expiredays==null) ? "" : ";expires="+exdate);
	}
};

