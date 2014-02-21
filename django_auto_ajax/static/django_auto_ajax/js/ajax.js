var historySupported = window.history && window.history.pushState;
var historyPushEnabled = true;
var historyFirstPopped = false;

// register history popsate event
if (window.history) {
	$(window).on('popstate', function(event) {
		if (!historyFirstPopped) {
			historyFirstPopped = true;
			return;
		}
		historyFirstPopped = true;
		historyPushEnabled = false;
		$.get(window.document.location.href);
	});
}

var redrawFunctions = {};
function registerRedrawCallback(selector, func) {
	redrawFunctions[selector] = func;
}


function repaint(data) {

	// no data, do nothing
	if (!data || typeof data !== 'object') {
		return;
	}

	// redirect
	if ('redirect' in data && data.redirect) {
		// $.get(data.redirect); -- ajax redirect would probably be to "complicated"
		// in terms of which snippets we should reload
		window.location.href = data.redirect;
		return;
	}

	// url update
	if ('url' in data && data.url && window.history && historyPushEnabled) {
		history.pushState(null, null, data.url);
		historyFirstPopped = true;
	}
	historyPushEnabled = true;

	// redraw snippets
	if ('snippets' in data && data.snippets) {
		for (var name in data.snippets) {
			$("#snippet--" + name).html(data.snippets[name]);
		}
		$(document).trigger('ajaxLoad');
	}
}

jQuery.ajaxSetup({
	beforeSend: function(xhr, settings) {
		if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
			// Send the token to same-origin, relative URLs only.
			// Send the token only if the method warrants CSRF protection
			xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
		}
	},
	dataType: 'json',
	dataFilter: function(data, type) {
		if (type !== 'json') return data;
		jsonData = JSON.parse(data);
		repaint(jsonData);
		return (typeof data === 'object' && 'data' in jsonData) ? JSON.stringify(jsonData.data) : data;
	},
	cache: false
});



function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
	// test that a given url is a same-origin URL
	// url could be relative or scheme relative or absolute
	var host = document.location.host; // host + port
	var protocol = document.location.protocol;
	var sr_origin = '//' + host;
	var origin = protocol + sr_origin;
	// Allow absolute or scheme relative URLs to same origin
	return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
		(url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
		// or any other URL that isn't scheme relative or absolute i.e relative.
		!(/^(\/\/|http:|https:).*/.test(url));
}

/**
 * AJAX form plugin for jQuery
 *
 * @copyright  Copyright (c) 2009 Jan Marek
 * @license    MIT
 * @link       http://nettephp.com/cs/extras/ajax-form
 * @version    0.1
 */

jQuery.fn.extend({
	ajaxSubmit: function (callback) {
		var form;
		var sendValues = {};

		// submit button
		if (this.is(":submit")) {
			form = this.parents("form");
			sendValues[this.attr("name")] = this.val() || "";

		// form
		} else if (this.is("form")) {
			form = this;

		// invalid element, do nothing
		} else {
			return null;
		}

		// validation
		if (form.get(0).onsubmit && form.get(0).onsubmit() === false) return null;

		// get values
		var values = form.serializeArray();

		for (var i = 0; i < values.length; i++) {
			var name = values[i].name;

			// multi
			if (name in sendValues) {
				var val = sendValues[name];

				if (!(val instanceof Array)) {
					val = [val];
				}

				val.push(values[i].value);
				sendValues[name] = val;
			} else {
				sendValues[name] = values[i].value;
			}
		}

		// send ajax request
		var ajaxOptions = {
			url: form.attr("action"),
			data: sendValues,
			type: form.attr("method") || "get"
		};

		if (callback) {
			ajaxOptions.success = callback;
		}

		return jQuery.ajax(ajaxOptions);
	}
});
