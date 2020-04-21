/*
 * jQuery UI Window based on Dialog 1.7.2
 *
 * Copyright (c) 2009 AUTHORS.txt (http://jqueryui.com/about)
 * Dual licensed under the MIT (MIT-LICENSE.txt)
 * and GPL (GPL-LICENSE.txt) licenses.
 *
 * http://docs.jquery.com/UI/Dialog
 *
 * Depends:
 *	ui.core.js
 *	ui.draggable.js
 *	ui.resizable.js
 */
(function($) {

var setDataSwitch = {
		dragStart: "start.draggable",
		drag: "drag.draggable",
		dragStop: "stop.draggable",
		maxHeight: "maxHeight.resizable",
		minHeight: "minHeight.resizable",
		maxWidth: "maxWidth.resizable",
		minWidth: "minWidth.resizable",
		resizeStart: "start.resizable",
		resize: "drag.resizable",
		resizeStop: "stop.resizable"
	},

	uiWindowClasses =
		'ui-dialog ' +
		'ui-widget ' +
		'ui-widget-content ' +
		'ui-corner-all ',

	uiWindowMinimizedClasses =
		'ui-window-minimized ' +
		'ui-widget ' +
		'ui-widget-content ' +
		'ui-corner-all ';

$.widget("ui.window", {

	_init: function() {
		this.originalTitle = this.element.attr('title');

		var self = this,
			options = this.options,

			title = options.title || this.originalTitle || '&nbsp;',
			titleId = $.ui.window.getTitleId(this.element),
			elementId = $.ui.window.getElementId(this.element),
                  heightBeforeMax = options.height,
                  widthBeforeMax = options.width,
                  topBeforeMax = 0,
                  leftBeforeMax = 0,
                  heightBeforeMin = options.height,
                  widthBeforeMin = options.width,
                  topBeforeMin = 0,
                  leftBeforeMin = 0,

			uiWindowMinimized = (this.uiWindowMinimized = $('<div/>'))
				.appendTo(document.body)
				.hide()
				.addClass(uiWindowMinimizedClasses)
				.css({
					position: 'absolute',
					zIndex: options.zIndex
				})
				.attr({
					role: 'minimized',
                    'id': elementId + '-minimized',
					'aria-labelledby': elementId + '-minimized'
				}),

			uiWindowMinimizedIcon = $('<a href="#"/>')
				.addClass('ui-window-minimized-icon')
				.attr('title', options.iconText)
				.attr('role', 'button')
				.hover(
					function() {
						uiWindowMinimizedIcon.addClass('ui-state-hover');
					},
					function() {
						uiWindowMinimizedIcon.removeClass('ui-state-hover');
					}
				)
				.focus(function() {
					uiWindowMinimizedIcon.addClass('ui-state-focus');
				})
				.blur(function() {
					uiWindowMinimizedIcon.removeClass('ui-state-focus');
				})
				.mousedown(function(ev) {
					ev.stopPropagation();
				})
				.click(function(event) {
					self.showMinimized();
					return false;
				})
				.appendTo(uiWindowMinimized),

			uiWindowMinimizedIconText = (this.uiWindowMinimizedIconText = $('<span/>'))
				.attr('id', elementId + '-minimized-text')
				.text(title)
				.appendTo(uiWindowMinimizedIcon),

			uiWindow = (this.uiWindow = $('<div/>'))
				.appendTo(document.body)
				.hide()
				.addClass(uiWindowClasses + options.dialogClass)
				.data('uiWindowObj', self)
				.css({
					position: 'absolute',
					overflow: 'hidden',
					zIndex: options.zIndex
				})
				// setting tabIndex makes the div focusable
				// setting outline to 0 prevents a border on focus in Mozilla
				.attr('tabIndex', -1).css('outline', 0).keydown(function(event) {
					(options.closeOnEscape && event.keyCode
						&& event.keyCode == $.ui.keyCode.ESCAPE && self.close(event));
				})
				.attr({
					role: 'window',
                    'id': elementId + '-window',
					'aria-labelledby': elementId
				}),

			uiWindowContent = this.element
				.show()
				.removeAttr('title')
				.addClass(
					'ui-dialog-content ' +
					'ui-widget-content')
				.appendTo(uiWindow),

			uiWindowTitlebar = (this.uiWindowTitlebar = $('<div></div>'))
				.addClass(
					'ui-dialog-titlebar ' +
					'ui-widget-header ' +
					'ui-corner-all ' +
					'ui-helper-clearfix'
				)
				.dblclick(function(event) {
					if (self.options.maximizable) {
                        if (uiWindowTitlebarRes.is(':visible')) {
                            uiWindowTitlebarRes.click();
                        } else {
                            uiWindowTitlebarMax.click();
                        }
					}
					return false;
				})
				.prependTo(uiWindow),

			uiWindowTitlebarMin = $('<a href="#"/>')
				.addClass(
					'ui-window-titlebar-min ' +
					'ui-corner-all'
				)
				.attr('title', options.minimizeText)
				.attr('role', 'button')
				.hover(
					function() {
						uiWindowTitlebarMin.addClass('ui-state-hover');
					},
					function() {
						uiWindowTitlebarMin.removeClass('ui-state-hover');
					}
				)
				.focus(function() {
					uiWindowTitlebarMin.addClass('ui-state-focus');
				})
				.blur(function() {
					uiWindowTitlebarMin.removeClass('ui-state-focus');
				})
				.mousedown(function(ev) {
					ev.stopPropagation();
				})
				.click(function(event) {
					self.minimize();
					return false;
				})
				.appendTo(uiWindowTitlebar),

			uiWindowTitlebarMinText = (this.uiWindowTitlebarMinText = $('<span/>'))
				.addClass(
					'ui-icon ' +
					'ui-icon-minus'
				)
				.text(options.minimizeText)
				.appendTo(uiWindowTitlebarMin),

			uiWindowTitlebarMax = (this.uiWindowTitlebarMax = $('<a href="#"/>'))
				.addClass(
					'ui-window-titlebar-max ' +
					'ui-corner-all'
				)
				.attr('title', options.maximizeText)
				.attr('role', 'button')
				.hover(
					function() {
						uiWindowTitlebarMax.addClass('ui-state-hover');
					},
					function() {
						uiWindowTitlebarMax.removeClass('ui-state-hover');
					}
				)
				.focus(function() {
					uiWindowTitlebarMax.addClass('ui-state-focus');
				})
				.blur(function() {
					uiWindowTitlebarMax.removeClass('ui-state-focus');
				})
				.mousedown(function(ev) {
					ev.stopPropagation();
				})
				.click(function(event) {
					self.maximize();
					return false;
				})
				.appendTo(uiWindowTitlebar),

			uiWindowTitlebarMaxText = (this.uiWindowTitlebarMaxText = $('<span/>'))
				.addClass(
					'ui-icon ' +
					'ui-icon-extlink'
				)
				.text(options.maximizeText)
				.appendTo(uiWindowTitlebarMax),

			uiWindowTitlebarRes = (this.uiWindowTitlebarRes = $('<a href="#"/>'))
				.addClass(
					'ui-window-titlebar-max ' +
					'ui-corner-all'
				)
				.attr('title', options.restoreText)
				.attr('role', 'button')
                        .hide()
				.hover(
					function() {
						uiWindowTitlebarRes.addClass('ui-state-hover');
					},
					function() {
						uiWindowTitlebarRes.removeClass('ui-state-hover');
					}
				)
				.focus(function() {
					uiWindowTitlebarRes.addClass('ui-state-focus');
				})
				.blur(function() {
					uiWindowTitlebarRes.removeClass('ui-state-focus');
				})
				.mousedown(function(ev) {
					ev.stopPropagation();
				})
				.click(function(event) {
					self.restore();
					return false;
				})
				.appendTo(uiWindowTitlebar),

			uiWindowTitlebarResText = (this.uiWindowTitlebarResText = $('<span/>'))
				.addClass(
					'ui-icon ' +
					'ui-icon-newwin'
				)
				.text(options.restoreText)
				.appendTo(uiWindowTitlebarRes),

			uiWindowTitlebarClose = $('<a href="#"/>')
				.addClass(
					'ui-dialog-titlebar-close ' +
					'ui-corner-all'
				)
				.attr('title', options.closeText)
				.attr('role', 'button')
				.hover(
					function() {
						uiWindowTitlebarClose.addClass('ui-state-hover');
					},
					function() {
						uiWindowTitlebarClose.removeClass('ui-state-hover');
					}
				)
				.focus(function() {
					uiWindowTitlebarClose.addClass('ui-state-focus');
				})
				.blur(function() {
					uiWindowTitlebarClose.removeClass('ui-state-focus');
				})
				.mousedown(function(ev) {
					ev.stopPropagation();
				})
				.click(function(event) {
					self.close(event);
					return false;
				})
				.appendTo(uiWindowTitlebar),

			uiWindowTitlebarCloseText = (this.uiWindowTitlebarCloseText = $('<span/>'))
				.addClass(
					'ui-icon ' +
					'ui-icon-close'
				)
				.text(options.closeText)
				.appendTo(uiWindowTitlebarClose),

			uiWindowTitle = $('<span/>')
				.addClass('ui-dialog-title')
				.attr('id', titleId)
				.html(title)
				.prependTo(uiWindowTitlebar);

		uiWindowTitlebar.find("*").add(uiWindowTitlebar).disableSelection();
		uiWindowMinimizedIcon.find("*").add(uiWindowMinimizedIcon).disableSelection();

		if (!options.minimizable) {
			uiWindowTitlebarMin.hide();
		}

		if (!options.maximizable) {
			uiWindowTitlebarMax.hide();
		}

		if (!options.closable) {
            uiWindowTitlebarClose.hide();
        }

		(options.draggable && $.fn.draggable && this._makeDraggable());
		(options.resizable && $.fn.resizable && this._makeResizable());

        this._createButtons(options.buttons);
		this._isOpen = false;

		(options.bgiframe && $.fn.bgiframe && uiWindow.bgiframe());
		(options.autoOpen && this.open());
	},

	destroy: function() {
		(this.overlay && this.overlay.destroy());
		this.uiWindow.hide();
		this.element
			.unbind('.window')
			.removeData('window')
			.removeClass('ui-dialog-content ui-widget-content')
			.hide().appendTo('body');
		this.uiWindow.remove();

		(this.originalTitle && this.element.attr('title', this.originalTitle));
	},

	close: function(event) {
		var self = this;

		if (false === self._trigger('beforeclose', event)) {
			return;
		}

		(self.overlay && self.overlay.destroy());
		self.uiWindow.unbind('keypress.ui-dialog');

		(self.options.hide
			? self.uiWindow.hide(self.options.hide, function() {
				self._trigger('close', event);
			})
			: self.uiWindow.hide() && self._trigger('close', event));

		$.ui.window.overlay.resize();

		self._isOpen = false;

		// adjust the maxZ to allow other modal dialogs to continue to work (see #4309)
		if (self.options.modal) {
			var maxZ = 0;
			$('.ui-dialog').each(function() {
				if (this != self.uiWindow[0]) {
					maxZ = Math.max(maxZ, $(this).css('z-index'));
				}
			});
			$.ui.window.maxZ = maxZ;
		}
	},

	isOpen: function() {
		return this._isOpen;
	},

	maximize: function() {
        var maxParent = window;
        if (this.options.container && this.options.container.offset()
      		  && ((this.options.container.offset().left > 0)
      				  || (this.options.container.offset().top > 0))
      		  && ((this.options.container.height() > 0)
      				  || (this.options.container.width() > 0))) {
      	  maxParent = this.options.container;
        }
        this.heightBeforeMax = this.uiWindow.height();
        this.setHeight(this.options.maxHeight? this.options.maxHeight : $(maxParent).height() - 20);
        this.widthBeforeMax = this.uiWindow.width();
        this.setWidth(this.options.maxWidth? this.options.maxWidth : $(maxParent).width() - 30);
        this.leftBeforeMax = this.uiWindow.offset().left;
        this.topBeforeMax = this.uiWindow.offset().top;
        var maxLeft = 0;
        var maxTop = 0;
        if (maxParent != window) {
            maxLeft = $(maxParent).offset().left;
            maxTop = $(maxParent).offset().top;
        }
        this.setPosition([maxLeft + 10, maxTop + 10]);
        this.setSize();
		this.moveToTop(true);
		this.uiWindowTitlebarRes.show();
        this.uiWindowTitlebarMax.hide();
	},

	restore: function() {
		this.setHeight(this.heightBeforeMax);
		this.setWidth(this.widthBeforeMax);
		this.setPosition([this.leftBeforeMax, this.topBeforeMax]);
       	this.setSize();
       	this.uiWindowTitlebarMax.show();
       	this.uiWindowTitlebarRes.hide();
	},

	minimize: function() {
		this.heightBeforeMin = this.uiWindow.height();
		this.widthBeforeMin = this.uiWindow.width();
		this.leftBeforeMin = this.uiWindow.offset().left;
		this.topBeforeMin = this.uiWindow.offset().top;
		this.uiWindow.hide();
        var minLeft = this.options.minimizePosition? (this.options.minimizePosition.left? this.options.minimizePosition.left : this.options.minimizePosition.offset().left) : this.leftBeforeMin;
        var minTop = this.options.minimizePosition? (this.options.minimizePosition.top? this.options.minimizePosition.top : this.options.minimizePosition.offset().top) : this.topBeforeMin;
        this.uiWindowMinimized.css({left: minLeft, top: minTop});
        this.uiWindowMinimized.show();
        if (this.options.onMinimize) {
            this.options.onMinimize(this.uiWindowMinimized);
        }
	},

	hideMinimized: function() {
		this.uiWindowMinimized.hide();
	},

	showMinimized: function() {
		this.uiWindowMinimized.hide();
        this.uiWindow.show();
		this.moveToTop(true);
	},

	// the force parameter allows us to move modal dialogs to their correct
	// position on open
	moveToTop: function(force, event) {

		if ((this.options.modal && !force)
			|| (!this.options.stack && !this.options.modal)) {
			return this._trigger('focus', event);
		}

		if (this.options.zIndex > $.ui.window.maxZ) {
			$.ui.window.maxZ = this.options.zIndex;
		}
		(this.overlay && this.overlay.$el.css('z-index', $.ui.window.overlay.maxZ = ++$.ui.window.maxZ));

		//Save and then restore scroll since Opera 9.5+ resets when parent z-Index is changed.
		//  http://ui.jquery.com/bugs/ticket/3193
		var saveScroll = { scrollTop: this.element.attr('scrollTop'), scrollLeft: this.element.attr('scrollLeft') };
		this.uiWindow.css('z-index', ++$.ui.window.maxZ);
		this.element.attr(saveScroll);
		this._trigger('focus', event);
	},

	open: function() {
		if (this._isOpen) { return; }

		var options = this.options,
			uiWindow = this.uiWindow;

		this.overlay = options.modal ? new $.ui.window.overlay(this) : null;
		(uiWindow.next().length && uiWindow.appendTo('body'));
		this.setSize();
		this.setPosition(options.position);
		uiWindow.show(options.show);
		this.moveToTop(true);

		// prevent tabbing out of modal dialogs
		(options.modal && uiWindow.bind('keypress.ui-dialog', function(event) {
			if (event.keyCode != $.ui.keyCode.TAB) {
				return;
			}

			var tabbables = $(':tabbable', this),
				first = tabbables.filter(':first')[0],
				last  = tabbables.filter(':last')[0];

			if (event.target == last && !event.shiftKey) {
				setTimeout(function() {
					first.focus();
				}, 1);
			} else if (event.target == first && event.shiftKey) {
				setTimeout(function() {
					last.focus();
				}, 1);
			}
		}));

		// set focus to the first tabbable element in the content area or the first button
		// if there are no tabbable elements, set focus on the dialog itself
		$([])
			.add(uiWindow.find('.ui-dialog-content :tabbable:first'))
			.add(uiWindow.find('.ui-dialog-buttonpane :tabbable:first'))
			.add(uiWindow)
			.filter(':first')
			.focus();

		this._trigger('open');
		this._isOpen = true;
	},

    setHeight: function(value) {
		this.options.height = value;
        this.uiWindow.height(value);
	},

    setWidth: function(value) {
		this.options.width = value;
        this.uiWindow.width(value);
	},

	setPosition: function(pos) {
		this.options.position = pos;
		this._position(pos);
	},

	setSize: function() {
		this._size();
	},

	_createButtons: function(buttons) {
		var self = this,
			hasButtons = false,
			uiWindowButtonPane = $('<div></div>')
				.addClass(
					'ui-dialog-buttonpane ' +
					'ui-widget-content ' +
					'ui-helper-clearfix'
				);

		// if we already have a button pane, remove it
		this.uiWindow.find('.ui-dialog-buttonpane').remove();

		(typeof buttons == 'object' && buttons !== null &&
			$.each(buttons, function() { return !(hasButtons = true); }));
		if (hasButtons) {
			$.each(buttons, function(name, fn) {
				$('<button type="button"></button>')
					.addClass(
						'ui-state-default ' +
						'ui-corner-all'
					)
					.text(name)
					.click(function() { fn.apply(self.element[0], arguments); })
					.hover(
						function() {
							$(this).addClass('ui-state-hover');
						},
						function() {
							$(this).removeClass('ui-state-hover');
						}
					)
					.focus(function() {
						$(this).addClass('ui-state-focus');
					})
					.blur(function() {
						$(this).removeClass('ui-state-focus');
					})
					.appendTo(uiWindowButtonPane);
			});
			uiWindowButtonPane.appendTo(this.uiWindow);
		}
	},

	_makeDraggable: function() {
		var self = this,
			options = this.options,
			heightBeforeDrag;

		this.uiWindow.draggable({
			cancel: '.ui-dialog-content',
			handle: '.ui-dialog-titlebar',
			containment: 'document',
			start: function() {
				heightBeforeDrag = options.height;
				$(this).height($(this).height()).addClass("ui-dialog-dragging");
				(options.dragStart && options.dragStart.apply(self.element[0], arguments));
			},
			drag: function() {
				(options.drag && options.drag.apply(self.element[0], arguments));
			},
			stop: function() {
				$(this).removeClass("ui-dialog-dragging").height(heightBeforeDrag);
				(options.dragStop && options.dragStop.apply(self.element[0], arguments));
				$.ui.window.overlay.resize();
			}
		});
	},

	_makeResizable: function(handles) {
		handles = (handles === undefined ? this.options.resizable : handles);
		var self = this,
			options = this.options,
			resizeHandles = typeof handles == 'string'
				? handles
				: 'n,e,s,w,se,sw,ne,nw';

		this.uiWindow.resizable({
			cancel: '.ui-dialog-content',
			alsoResize: this.element,
			maxWidth: options.maxWidth,
			maxHeight: options.maxHeight,
			minWidth: options.minWidth,
			minHeight: options.minHeight,
			start: function() {
				$(this).addClass("ui-dialog-resizing");
				(options.resizeStart && options.resizeStart.apply(self.element[0], arguments));
			},
			resize: function() {
				(options.resize && options.resize.apply(self.element[0], arguments));
			},
			handles: resizeHandles,
			stop: function() {
				$(this).removeClass("ui-dialog-resizing");
				options.height = $(this).height();
				options.width = $(this).width();
				(options.resizeStop && options.resizeStop.apply(self.element[0], arguments));
				$.ui.window.overlay.resize();
			}
		})
		.find('.ui-resizable-se').addClass('ui-icon ui-icon-grip-diagonal-se');
	},

	_position: function(pos) {
		var wnd = $(window), doc = $(document),
			pTop = doc.scrollTop(), pLeft = doc.scrollLeft(),
			minTop = pTop;

		if ($.inArray(pos, ['center','top','right','bottom','left']) >= 0) {
			pos = [
				pos == 'right' || pos == 'left' ? pos : 'center',
				pos == 'top' || pos == 'bottom' ? pos : 'middle'
			];
		}
		if (pos.constructor != Array) {
			pos = ['center', 'middle'];
		}
		if (pos[0].constructor == Number) {
			pLeft += pos[0];
		} else {
			switch (pos[0]) {
				case 'left':
					pLeft += 0;
					break;
				case 'right':
					pLeft += wnd.width() - this.uiWindow.outerWidth();
					break;
				default:
				case 'center':
					pLeft += (wnd.width() - this.uiWindow.outerWidth()) / 2;
			}
		}
		if (pos[1].constructor == Number) {
			pTop += pos[1];
		} else {
			switch (pos[1]) {
				case 'top':
					pTop += 0;
					break;
				case 'bottom':
					pTop += wnd.height() - this.uiWindow.outerHeight();
					break;
				default:
				case 'middle':
					pTop += (wnd.height() - this.uiWindow.outerHeight()) / 2;
			}
		}

		// prevent the dialog from being too high (make sure the titlebar
		// is accessible)
		pTop = Math.max(pTop, minTop);
		this.uiWindow.css({top: pTop, left: pLeft});
	},

	_setData: function(key, value){
		(setDataSwitch[key] && this.uiWindow.data(setDataSwitch[key], value));
		switch (key) {
			case "buttons":
				this._createButtons(value);
				break;
			case "iconText":
				this.uiWindowMinimizedIcon.attr('title', value);
				break;
			case "minimizeText":
				this.uiWindowTitlebarMinText.text(value);
				this.uiWindowTitlebarMinText.attr('title', value)
				break;
			case "maximizeText":
				this.uiWindowTitlebarMaxText.text(value);
				this.uiWindowTitlebarMaxText.attr('title', value)
				break;
			case "restoreText":
				this.uiWindowTitlebarResText.text(value);
				this.uiWindowTitlebarResText.attr('title', value)
				break;
			case "closeText":
				this.uiWindowTitlebarCloseText.text(value);
				this.uiWindowTitlebarCloseText.attr('title', value)
				break;
			case "dialogClass":
				this.uiWindow
					.removeClass(this.options.dialogClass)
					.addClass(uiWindowClasses + value);
				break;
			case "draggable":
				(value
					? this._makeDraggable()
					: this.uiWindow.draggable('destroy'));
				break;
			case "resizable":
				var uiWindow = this.uiWindow,
					isResizable = this.uiWindow.is(':data(resizable)');

				// currently resizable, becoming non-resizable
				(isResizable && !value && uiWindow.resizable('destroy'));

				// currently resizable, changing handles
				(isResizable && typeof value == 'string' &&
					uiWindow.resizable('option', 'handles', value));

				// currently non-resizable, becoming resizable
				(isResizable || this._makeResizable(value));
				break;
			case "title":
				$(".ui-dialog-title", this.uiWindowTitlebar).html(value || '&nbsp;');
				$('#' + $.ui.window.getTitleId(this.element) + '-minimized-text').text(value);
				break;
		}

		$.widget.prototype._setData.apply(this, arguments);
	},

	_size: function() {
		/* If the user has resized the dialog, the .ui-dialog and .ui-dialog-content
		 * divs will both have width and height set, so we need to reset them
		 */
		var options = this.options;

		// reset content sizing
		this.element.css({
			height: 0,
			minHeight: 0,
			width: 'auto'
		});

		// reset wrapper sizing
		// determine the height of all the non-content elements
		var nonContentHeight = this.uiWindow.css({
				height: 'auto',
				width: options.width
			})
			.height();

		this.element
			.css({
				minHeight: Math.max(options.minHeight - nonContentHeight, 0),
				height: options.height == 'auto'
					? 'auto'
					: Math.max(options.height - nonContentHeight, 0)
			});
	}
});

$.extend($.ui.window, {
	version: "1.7.2",
	defaults: {
		autoOpen: true,
		bgiframe: false,
		buttons: {},
		iconText: 'show',
		minimizeText: 'minimize',
		maximizeText: 'maximize',
		restoreText: 'restore',
		closeOnEscape: true,
		closeText: 'close',
		minimizable: true,
		maximizable: true,
		closable: true,
		dialogClass: '',
		draggable: true,
		hide: null,
		height: 'auto',
		maxHeight: false,
		maxWidth: false,
		minHeight: 150,
		minWidth: 150,
		modal: false,
		position: 'center',
		minimizePosition: false,
		onMinimize: function() {},
		container: false,
		resizable: true,
		show: null,
		stack: true,
		title: '',
		width: 300,
		zIndex: 1000
	},

	getter: 'isOpen',

	uuid: 0,
	maxZ: 0,

	setElementUIWindow: function($el) {
		$el.uiwindow = this;
	},

	getElementId: function($el) {
		return ($el.attr('id') || ++this.uuid);
	},

	getTitleId: function($el) {
		return 'ui-dialog-title-' + $.ui.window.getElementId($el);
	},

	overlay: function(dialog) {
		this.$el = $.ui.window.overlay.create(dialog);
	}
});

$.extend($.ui.window.overlay, {
	instances: [],
	maxZ: 0,
	events: $.map('focus,mousedown,mouseup,keydown,keypress,click'.split(','),
		function(event) { return event + '.dialog-overlay'; }).join(' '),
	create: function(dialog) {
		if (this.instances.length === 0) {
			// prevent use of anchors and inputs
			// we use a setTimeout in case the overlay is created from an
			// event that we're going to be cancelling (see #2804)
			setTimeout(function() {
				// handle $(el).dialog().dialog('close') (see #4065)
				if ($.ui.window.overlay.instances.length) {
					$(document).bind($.ui.window.overlay.events, function(event) {
						var dialogZ = $(event.target).parents('.ui-dialog').css('zIndex') || 0;
						return (dialogZ > $.ui.window.overlay.maxZ);
					});
				}
			}, 1);

			// allow closing by pressing the escape key
			$(document).bind('keydown.dialog-overlay', function(event) {
				(dialog.options.closeOnEscape && event.keyCode
						&& event.keyCode == $.ui.keyCode.ESCAPE && dialog.close(event));
			});

			// handle window resize
			$(window).bind('resize.dialog-overlay', $.ui.window.overlay.resize);
		}

		var $el = $('<div></div>').appendTo(document.body)
			.addClass('ui-widget-overlay').css({
				width: this.width(),
				height: this.height()
			});

		(dialog.options.bgiframe && $.fn.bgiframe && $el.bgiframe());

		this.instances.push($el);
		return $el;
	},

	destroy: function($el) {
		this.instances.splice($.inArray(this.instances, $el), 1);

		if (this.instances.length === 0) {
			$([document, window]).unbind('.dialog-overlay');
		}

		$el.remove();

		// adjust the maxZ to allow other modal dialogs to continue to work (see #4309)
		var maxZ = 0;
		$.each(this.instances, function() {
			maxZ = Math.max(maxZ, this.css('z-index'));
		});
		this.maxZ = maxZ;
	},

	height: function() {
		// handle IE 6
		if ($.browser.msie && $.browser.version < 7) {
			var scrollHeight = Math.max(
				document.documentElement.scrollHeight,
				document.body.scrollHeight
			);
			var offsetHeight = Math.max(
				document.documentElement.offsetHeight,
				document.body.offsetHeight
			);

			if (scrollHeight < offsetHeight) {
				return $(window).height() + 'px';
			} else {
				return scrollHeight + 'px';
			}
		// handle "good" browsers
		} else {
			return $(document).height() + 'px';
		}
	},

	width: function() {
		// handle IE 6
		if ($.browser.msie && $.browser.version < 7) {
			var scrollWidth = Math.max(
				document.documentElement.scrollWidth,
				document.body.scrollWidth
			);
			var offsetWidth = Math.max(
				document.documentElement.offsetWidth,
				document.body.offsetWidth
			);

			if (scrollWidth < offsetWidth) {
				return $(window).width() + 'px';
			} else {
				return scrollWidth + 'px';
			}
		// handle "good" browsers
		} else {
			return $(document).width() + 'px';
		}
	},

	resize: function() {
		/* If the dialog is draggable and the user drags it past the
		 * right edge of the window, the document becomes wider so we
		 * need to stretch the overlay. If the user then drags the
		 * dialog back to the left, the document will become narrower,
		 * so we need to shrink the overlay to the appropriate size.
		 * This is handled by shrinking the overlay before setting it
		 * to the full document size.
		 */
		var $overlays = $([]);
		$.each($.ui.window.overlay.instances, function() {
			$overlays = $overlays.add(this);
		});

		$overlays.css({
			width: 0,
			height: 0
		}).css({
			width: $.ui.window.overlay.width(),
			height: $.ui.window.overlay.height()
		});
	}
});

$.extend($.ui.window.overlay.prototype, {
	destroy: function() {
		$.ui.window.overlay.destroy(this.$el);
	}
});

})(jQuery);
