import json

from string import Template

##########
# Define templates
##########

weather_template = Template('{"type":"weather","data":${data},"child":[${child}]}')

location_template = Template('''
{
    "type":"location",
    "loctype":"${loctype}",
    "data":${data},
    "child":[${child}]
}
''')

def create_message(msg_type, data, child):
    if msg_type == "weather":
        return weather_template.substitute(data=data, child=child)
    else:
        return ""
