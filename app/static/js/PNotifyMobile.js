var _typeof =
  typeof Symbol === "function" && typeof Symbol.iterator === "symbol"
    ? function(obj) {
        return typeof obj;
      }
    : function(obj) {
        return obj &&
          typeof Symbol === "function" &&
          obj.constructor === Symbol &&
          obj !== Symbol.prototype
          ? "symbol"
          : typeof obj;
      };

var _extends =
  Object.assign ||
  function(target) {
    for (var i = 1; i < arguments.length; i++) {
      var source = arguments[i];
      for (var key in source) {
        if (Object.prototype.hasOwnProperty.call(source, key)) {
          target[key] = source[key];
        }
      }
    }
    return target;
  };

/* src/PNotifyMobile.html generated by Svelte v2.16.1 */
var PNotifyMobile = (function(PNotify) {
  "use strict";

  PNotify = PNotify && PNotify.__esModule ? PNotify["default"] : PNotify;

  function data() {
    return _extends(
      {
        _notice: null, // The PNotify notice.
        _options: {} // The options for the notice.
      },
      PNotify.modules.Mobile.defaults
    );
  }

  var methods = {
    initModule: function initModule(options) {
      var _this = this;

      this.set(options);

      var _get = this.get(),
        _notice = _get._notice;

      var origXY = null;
      var diffXY = null;
      var noticeWidthHeight = null;
      var noticeOpacity = null;
      var csspos = "left";
      var direction = "X";
      var span = "Width";

      _notice.on("touchstart", function(e) {
        if (!_this.get().swipeDismiss) {
          return;
        }

        var _notice$get = _notice.get(),
          stack = _notice$get.stack;

        if (stack !== false) {
          switch (stack.dir1) {
            case "up":
            case "down":
              csspos = "left";
              direction = "X";
              span = "Width";
              break;
            case "left":
            case "right":
              csspos = "top";
              direction = "Y";
              span = "Height";
              break;
          }
        }

        origXY = e.touches[0]["screen" + direction];
        noticeWidthHeight = _notice.refs.elem["scroll" + span];
        noticeOpacity = window.getComputedStyle(_notice.refs.elem)["opacity"];
        _notice.refs.container.style[csspos] = 0;
      });

      _notice.on("touchmove", function(e) {
        if (!origXY || !_this.get().swipeDismiss) {
          return;
        }

        var curXY = e.touches[0]["screen" + direction];

        diffXY = curXY - origXY;
        var opacity =
          (1 - Math.abs(diffXY) / noticeWidthHeight) * noticeOpacity;

        _notice.refs.elem.style.opacity = opacity;
        _notice.refs.container.style[csspos] = diffXY + "px";
      });

      _notice.on("touchend", function() {
        if (!origXY || !_this.get().swipeDismiss) {
          return;
        }

        _notice.refs.container.classList.add("ui-pnotify-mobile-animate-left");
        if (Math.abs(diffXY) > 40) {
          var goLeft =
            diffXY < 0 ? noticeWidthHeight * -2 : noticeWidthHeight * 2;
          _notice.refs.elem.style.opacity = 0;
          _notice.refs.container.style[csspos] = goLeft + "px";
          _notice.close();
        } else {
          _notice.refs.elem.style.removeProperty("opacity");
          _notice.refs.container.style.removeProperty(csspos);
        }
        origXY = null;
        diffXY = null;
        noticeWidthHeight = null;
        noticeOpacity = null;
      });

      _notice.on("touchcancel", function() {
        if (!origXY || !_this.get().swipeDismiss) {
          return;
        }

        _notice.refs.elem.style.removeProperty("opacity");
        _notice.refs.container.style.removeProperty(csspos);
        origXY = null;
        diffXY = null;
        noticeWidthHeight = null;
        noticeOpacity = null;
      });

      this.doMobileStyling();
    },
    update: function update() {
      this.doMobileStyling();
    },
    beforeOpen: function beforeOpen() {
      // Add an event listener to watch the window resizes.
      window.addEventListener("resize", this.get()._doMobileStylingBound);
    },
    afterClose: function afterClose() {
      // Remove the event listener.
      window.removeEventListener("resize", this.get()._doMobileStylingBound);

      // Remove any styling we added to close it.
      if (!this.get().swipeDismiss) {
        return;
      }

      var _get2 = this.get(),
        _notice = _get2._notice;

      _notice.refs.elem.style.removeProperty("opacity");
      _notice.refs.container.style.removeProperty("left");
      _notice.refs.container.style.removeProperty("top");
    },
    doMobileStyling: function doMobileStyling() {
      var _get3 = this.get(),
        _notice = _get3._notice;

      var _notice$get2 = _notice.get(),
        stack = _notice$get2.stack;

      if (this.get().styling) {
        if (stack !== false) {
          if (window.innerWidth <= 480) {
            if (!stack.mobileOrigSpacing1) {
              stack.mobileOrigSpacing1 = stack.spacing1;
            }
            stack.spacing1 = 0;
            if (!stack.mobileOrigFirstpos1) {
              stack.mobileOrigFirstpos1 = stack.firstpos1;
            }
            stack.firstpos1 = 0;
            if (!stack.mobileOrigSpacing2) {
              stack.mobileOrigSpacing2 = stack.spacing2;
            }
            stack.spacing2 = 0;
            if (!stack.mobileOrigFirstpos2) {
              stack.mobileOrigFirstpos2 = stack.firstpos2;
            }
            stack.firstpos2 = 0;
          } else {
            if (stack.mobileOrigSpacing1) {
              stack.spacing1 = stack.mobileOrigSpacing1;
              delete stack.mobileOrigSpacing1;
            }
            if (stack.mobileOrigFirstpos1) {
              stack.firstpos1 = stack.mobileOrigFirstpos1;
              delete stack.mobileOrigFirstpos1;
            }
            if (stack.mobileOrigSpacing2) {
              stack.spacing2 = stack.mobileOrigSpacing2;
              delete stack.mobileOrigSpacing2;
            }
            if (stack.mobileOrigFirstpos2) {
              stack.firstpos2 = stack.mobileOrigFirstpos2;
              delete stack.mobileOrigFirstpos2;
            }
          }
          switch (stack.dir1) {
            case "down":
              _notice.addModuleClass("ui-pnotify-mobile-top");
              break;
            case "up":
              _notice.addModuleClass("ui-pnotify-mobile-bottom");
              break;
            case "left":
              _notice.addModuleClass("ui-pnotify-mobile-right");
              break;
            case "right":
              _notice.addModuleClass("ui-pnotify-mobile-left");
              break;
          }
        }

        _notice.addModuleClass("ui-pnotify-mobile-able");
      } else {
        _notice.removeModuleClass(
          "ui-pnotify-mobile-able",
          "ui-pnotify-mobile-top",
          "ui-pnotify-mobile-bottom",
          "ui-pnotify-mobile-right",
          "ui-pnotify-mobile-left"
        );

        if (stack !== false) {
          if (stack.mobileOrigSpacing1) {
            stack.spacing1 = stack.mobileOrigSpacing1;
            delete stack.mobileOrigSpacing1;
          }
          if (stack.mobileOrigFirstpos1) {
            stack.firstpos1 = stack.mobileOrigFirstpos1;
            delete stack.mobileOrigFirstpos1;
          }
          if (stack.mobileOrigSpacing2) {
            stack.spacing2 = stack.mobileOrigSpacing2;
            delete stack.mobileOrigSpacing2;
          }
          if (stack.mobileOrigFirstpos2) {
            stack.firstpos2 = stack.mobileOrigFirstpos2;
            delete stack.mobileOrigFirstpos2;
          }
        }
      }
    }
  };

  function oncreate() {
    this.set({ _doMobileStylingBound: this.doMobileStyling.bind(this) });
  }

  function setup(Component) {
    Component.key = "Mobile";

    Component.defaults = {
      // Let the user swipe the notice away.
      swipeDismiss: true,
      // Styles the notice to look good on mobile.
      styling: true
    };

    Component.init = function(notice) {
      return new Component({ target: document.body });
    };

    // Register the module with PNotify.
    PNotify.modules.Mobile = Component;
  }

  function add_css() {
    var style = createElement("style");
    style.id = "svelte-49u8sj-style";
    style.textContent =
      "[ui-pnotify] .ui-pnotify-container{position:relative}[ui-pnotify] .ui-pnotify-mobile-animate-left{transition:left .1s ease}[ui-pnotify] .ui-pnotify-mobile-animate-top{transition:top .1s ease}@media(max-width: 480px){[ui-pnotify].ui-pnotify.ui-pnotify-mobile-able{font-size:1.2em;-webkit-font-smoothing:antialiased;-moz-font-smoothing:antialiased;-ms-font-smoothing:antialiased;font-smoothing:antialiased}body > [ui-pnotify].ui-pnotify.ui-pnotify-mobile-able{position:fixed}[ui-pnotify].ui-pnotify.ui-pnotify-mobile-able.ui-pnotify-mobile-top,[ui-pnotify].ui-pnotify.ui-pnotify-mobile-able.ui-pnotify-mobile-bottom{width:100% !important}[ui-pnotify].ui-pnotify.ui-pnotify-mobile-able.ui-pnotify-mobile-left,[ui-pnotify].ui-pnotify.ui-pnotify-mobile-able.ui-pnotify-mobile-right{height:100% !important}[ui-pnotify].ui-pnotify.ui-pnotify-mobile-able .ui-pnotify-shadow{-webkit-box-shadow:none;-moz-box-shadow:none;box-shadow:none}[ui-pnotify].ui-pnotify.ui-pnotify-mobile-able.ui-pnotify-mobile-top .ui-pnotify-shadow{border-bottom-width:5px}[ui-pnotify].ui-pnotify.ui-pnotify-mobile-able.ui-pnotify-mobile-bottom .ui-pnotify-shadow{border-top-width:5px}[ui-pnotify].ui-pnotify.ui-pnotify-mobile-able.ui-pnotify-mobile-left .ui-pnotify-shadow{border-right-width:5px}[ui-pnotify].ui-pnotify.ui-pnotify-mobile-able.ui-pnotify-mobile-right .ui-pnotify-shadow{border-left-width:5px}[ui-pnotify].ui-pnotify.ui-pnotify-mobile-able .ui-pnotify-container{-webkit-border-radius:0;-moz-border-radius:0;border-radius:0}[ui-pnotify].ui-pnotify.ui-pnotify-mobile-able.ui-pnotify-mobile-top .ui-pnotify-container,[ui-pnotify].ui-pnotify.ui-pnotify-mobile-able.ui-pnotify-mobile-bottom .ui-pnotify-container{width:auto !important}[ui-pnotify].ui-pnotify.ui-pnotify-mobile-able.ui-pnotify-mobile-left .ui-pnotify-container,[ui-pnotify].ui-pnotify.ui-pnotify-mobile-able.ui-pnotify-mobile-right .ui-pnotify-container{height:100% !important}}";
    append(document.head, style);
  }

  function create_main_fragment(component, ctx) {
    return {
      c: noop,

      m: noop,

      p: noop,

      d: noop
    };
  }

  function PNotifyMobile(options) {
    var _this2 = this;

    init(this, options);
    this._state = assign(data(), options.data);
    this._intro = true;

    if (!document.getElementById("svelte-49u8sj-style")) add_css();

    this._fragment = create_main_fragment(this, this._state);

    this.root._oncreate.push(function() {
      oncreate.call(_this2);
      _this2.fire("update", {
        changed: assignTrue({}, _this2._state),
        current: _this2._state
      });
    });

    if (options.target) {
      this._fragment.c();
      this._mount(options.target, options.anchor);

      flush(this);
    }
  }

  assign(PNotifyMobile.prototype, {
    destroy: destroy,
    get: get,
    fire: fire,
    on: on,
    set: set,
    _set: _set,
    _stage: _stage,
    _mount: _mount,
    _differs: _differs
  });
  assign(PNotifyMobile.prototype, methods);

  PNotifyMobile.prototype._recompute = noop;

  setup(PNotifyMobile);

  function createElement(name) {
    return document.createElement(name);
  }

  function append(target, node) {
    target.appendChild(node);
  }

  function noop() {}

  function init(component, options) {
    component._handlers = blankObject();
    component._slots = blankObject();
    component._bind = options._bind;
    component._staged = {};

    component.options = options;
    component.root = options.root || component;
    component.store = options.store || component.root.store;

    if (!options.root) {
      component._beforecreate = [];
      component._oncreate = [];
      component._aftercreate = [];
    }
  }

  function assign(tar, src) {
    for (var k in src) {
      tar[k] = src[k];
    }
    return tar;
  }

  function assignTrue(tar, src) {
    for (var k in src) {
      tar[k] = 1;
    }
    return tar;
  }

  function flush(component) {
    component._lock = true;
    callAll(component._beforecreate);
    callAll(component._oncreate);
    callAll(component._aftercreate);
    component._lock = false;
  }

  function destroy(detach) {
    this.destroy = noop;
    this.fire("destroy");
    this.set = noop;

    this._fragment.d(detach !== false);
    this._fragment = null;
    this._state = {};
  }

  function get() {
    return this._state;
  }

  function fire(eventName, data) {
    var handlers =
      eventName in this._handlers && this._handlers[eventName].slice();
    if (!handlers) return;

    for (var i = 0; i < handlers.length; i += 1) {
      var handler = handlers[i];

      if (!handler.__calling) {
        try {
          handler.__calling = true;
          handler.call(this, data);
        } finally {
          handler.__calling = false;
        }
      }
    }
  }

  function on(eventName, handler) {
    var handlers =
      this._handlers[eventName] || (this._handlers[eventName] = []);
    handlers.push(handler);

    return {
      cancel: function cancel() {
        var index = handlers.indexOf(handler);
        if (~index) handlers.splice(index, 1);
      }
    };
  }

  function set(newState) {
    this._set(assign({}, newState));
    if (this.root._lock) return;
    flush(this.root);
  }

  function _set(newState) {
    var oldState = this._state,
      changed = {},
      dirty = false;

    newState = assign(this._staged, newState);
    this._staged = {};

    for (var key in newState) {
      if (this._differs(newState[key], oldState[key]))
        changed[key] = dirty = true;
    }
    if (!dirty) return;

    this._state = assign(assign({}, oldState), newState);
    this._recompute(changed, this._state);
    if (this._bind) this._bind(changed, this._state);

    if (this._fragment) {
      this.fire("state", {
        changed: changed,
        current: this._state,
        previous: oldState
      });
      this._fragment.p(changed, this._state);
      this.fire("update", {
        changed: changed,
        current: this._state,
        previous: oldState
      });
    }
  }

  function _stage(newState) {
    assign(this._staged, newState);
  }

  function _mount(target, anchor) {
    this._fragment[this._fragment.i ? "i" : "m"](target, anchor || null);
  }

  function _differs(a, b) {
    return a != a
      ? b == b
      : a !== b ||
          (a &&
            (typeof a === "undefined" ? "undefined" : _typeof(a)) ===
              "object") ||
          typeof a === "function";
  }

  function blankObject() {
    return Object.create(null);
  }

  function callAll(fns) {
    while (fns && fns.length) {
      fns.shift()();
    }
  }
  return PNotifyMobile;
})(PNotify);
//# sourceMappingURL=PNotifyMobile.js.map
