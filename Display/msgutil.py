import json

from string import Template

##########
# Define templates
##########

display_template = Template('''
{
    "type":"display",
    "displaytype":"WeatherHAT",
    "data":"${data}",
    "child":[${child}]
}
''')

def create_message(msg_type, data, child):
    if msg_type == "display":
        return display_template.substitute(data=data, child=child)
    else:
        return ""