Django Auto Ajax
================

NOTE: This application works only with Jinja2 templates using the **django_jinja** package (https://github.com/niwibe/django-jinja).

## Installation
You can install Django Auto Ajax with [PIP](http://www.pip-installer.org/):
```bash
pip install git+git://github.com/visipedia/django-auto-ajax
```

Add `django_auto_ajax` to your `INSTALLED_APPS`.

Add the following to your settings:
```python
JINJA2_LOADER = 'django_auto_ajax.loaders.Loader'

JINJA2_EXTENSIONS = {
  'django_auto_ajax.extensions.SnippetsExtension',
}
```

Include `django_auto_ajax/js/ajax.js` to your page.

## Usage

### Ajaxify your pages
To ajaxify all your links with class `ajax` add the following to your JavaScript file:
```js
$('a[href].ajax').live('click', function (event) {
	event.preventDefault();
	$.get(this.href);
});
```

To ajaxify all your forms with class `ajax` add the followint to your JavaScript file:
```js
$("form.ajax").live('submit', function () {
	$(this).ajaxSubmit();
	return false;
});
```

### Usage in templates
To mark the pieces of template that you want to reload with AJAX use:
```html
{% snippet 'snippet-name' %}
Any piece of template here...
{% endsnippet %}
```

Snippets can be anywhere, can be nested, etc., but each must have globally unique name.

### Server side
In your views add `from django_auto_ajax.response import *` and use it instead of Django's render/response/redirect methods.

To say which pices of template should be repainted on AJAX request use:
```python
invalidate(request, 'snippet-name')
```

To return response from your views use the following methods.

**A normal response:**
```python
return response(request, 'myapp/mytemplate.jinja', data=data)
```
In case of non-AJAX request the template will be rendered normally. In case of AJAX request only the invalidated snippets will be rendered.

**Pure AJAX response:**
```python
return ajax_response(data=data)
```

**Redirect:**
```python
return redirect(...) # same parameters as Django's redirect
```
