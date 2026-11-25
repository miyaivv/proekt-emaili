#!/bin/env python3

import sys
import json
import re
from string import Template
from cmd_parser import CommandLineParser
from sender import Sender

cmd_parser = CommandLineParser("email-sender")
if not cmd_parser.IsValid:
    sys.exit()

sender = Sender()

template = None
data = None
with open(cmd_parser.TemplateFilePath, 'r', encoding="utf-8") as template_file:
    template = template_file.read()

with open(cmd_parser.DataFilePath, 'r') as data_file:
    data = json.load(data_file)

matches = re.findall(r'\$(\w+)', template)
for entry in data:
    (email, fields), = entry.items()
    name = fields[matches[0]]
    amount = fields[matches[1]]
    text = Template(template).substitute(fields)
   

    sender.send_email(
     sender.service,
     to=email,
     subject="Unpaid lunch - test",
     body=text)
      



