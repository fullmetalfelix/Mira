from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Email, Length, EqualTo
from wtforms.widgets import HTMLString
from wtforms.widgets import html_params



## Renders a textfield input (text or password)
#
def Widget_textinput(field, **kwargs):
	
	#print(kwargs.keys())
	
	response = []
	if kwargs.get('hidden', False): cls = "flexrow hiddendiv"
	else: cls = "flexrow"
	response.append(u"<div class='{}'>\n".format(cls))
	
	lbl = u"\t<span class='control-label'>{}:</span>\n".format(field.label.text)
	response.append(lbl)
	
	mytype = u"text"
	if 'type' in kwargs.keys(): mytype = kwargs['type']
	inp = u"\t<input class='control-input' type='{}' id='{}' name='{}' ".format(mytype, field.name, field.name)
	inp += html_params(**kwargs)
	if field.data: inp = inp + u" value='{}'".format(field.data)
	inp = inp + u" />\n"
	response.append(inp)
	
	response.append(u"</div>\n")
	
	# error management
	if field.errors:
		for error in field.errors:
			response.append(u"<div class='flexrow'>\n")
			response.append(u"\t<span class='control-label'>Error:</span>\n")
			response.append(u"\t<span class='control-input error'>{}</span>\n".format(error))
			response.append(u"</div>\n")
		response.append(u"<hr class='thinline' />\n")
	
	response = ''.join(response)
	return HTMLString(response)


## Renders a selector input.
#
def Widget_selector(field, **kwargs):
	
	response = []
	if kwargs.get('hidden', False): cls = "flexrow hiddendiv"
	else: cls = "flexrow"
	response.append(u"<div class='{}'>\n".format(cls))
	
	lbl = u"\t<span class='control-label'>{}:</span>\n".format(field.label.text)
	response.append(lbl)
	
	mytype = u"text"
	if 'type' in kwargs.keys(): mytype = kwargs['type']
	inp = u"\t<select class='control-input' type='{}' id='{}' name='{}' ".format(mytype, field.name, field.name)
	inp += html_params(**kwargs)
	inp = inp + u" >\n"
	response.append(inp)
	
	#print(kwargs)
	for obj in field.iter_choices():
		#print(obj)
		val = obj[0]
		label = obj[1]
		response.append(u"\t\t<option value='{}'>{}</option>\n".format(val,label))
	response.append(u"\t</select>\n")
	response.append(u"</div>\n")
	
	# error management
	if field.errors:
		for error in field.errors:
			response.append(u"<div class='flexrow'>\n")
			response.append(u"\t<span class='control-label'>Error:</span>\n")
			response.append(u"\t<span class='control-input error'>{}</span>\n".format(error))
			response.append(u"</div>\n")
		response.append(u"<hr class='thinline' />\n")
	
	response = ''.join(response)
	return HTMLString(response)


## Renders a ultiline textarea input
#
def Widget_textarea(field, **kwargs):
	
	response = []
	if kwargs.get('hidden', False): cls = "flexrow hiddendiv"
	else: cls = "flexrow"
	response.append(u"<div class='{}'>\n".format(cls))
	
	lbl = u"\t<span class='control-label'>{}:</span>\n".format(field.label.text)
	response.append(lbl)
	
	inp = u"\t<textarea class='control-input' id='{0}' name='{0}' ".format(field.name)
	inp += html_params(**kwargs) + u" >"
	if field.data: inp = inp + u"{}".format(field.data)
	inp = inp + u"</textarea>\n"
	response.append(inp)
	
	response.append(u"</div>\n")
	
	# error management
	if field.errors:
		for error in field.errors:
			response.append(u"<div class='flexrow'>\n")
			response.append(u"\t<span class='control-label'>Error:</span>\n")
			response.append(u"\t<span class='control-input error'>{}</span>\n".format(error))
			response.append(u"</div>\n")
		response.append(u"<hr class='thinline' />\n")
	
	response = ''.join(response)
	return HTMLString(response)


def Widget_submitbutton(field, **kwargs):
	
	response = []
	if kwargs.get('hidden', False): cls = "flexrow hiddendiv"
	else: cls = "flexrow"
	response.append(u"<div class='{}'>\n".format(cls))
	
	# this adds some space so the button is on the right
	lbl = u"\t<span style='flex-grow: 2;'></span>\n"
	response.append(lbl)
	
	inp = u"\t<input class='button' id='{0}' name='{0}' type='submit' value='{1}'".format(field.name, field.label.text)
	inp += html_params(**kwargs) + u" />\n"
	response.append(inp)
	
	response.append(u"</div>\n")
	
	response = ''.join(response)
	return HTMLString(response)







