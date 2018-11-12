"""
usage:
  migrate_bdd.py -h
  migrate_bdd.py -v
  migrate_bdd.py [--include=<text>] [--output=<output_file>] <feature_file>

options:
  -h, --help            Print this menu
  -v, --version         Print the version
  -o, --output=<file>   The migrated output C++ file.
  --include=<text>      The include line text. [default: <catch.hpp>]


To format the code output from this script the following is recommended:

    astyle --style=allman --indent=tab=4 <output_file>
"""

import os
import re

from docopt import docopt

def build_catch_scenario(text):
	return 'SCENARIO( "{}" )'.format(text)

def build_catch_given(text):
	return 'GIVEN( "{}" )'.format(text)

def build_catch_when(text):
	return 'WHEN( "{}" )'.format(text)

def build_catch_then(text):
	return 'THEN( "{}" )'.format(text)

def parse_gherkin_scenario(scenario_text):
	lines = scenario_text.splitlines()
	steps_count = 0
	steps = []
	previous_keyword = ''
	previous_step = {}

	steps.append({'keyword': 'SCENARIO', 'value': lines[0].strip()})
	steps_count += 1

	for line in lines:
		if line.strip().upper().startswith('GIVEN'):
			previous_keyword = 'GIVEN'
			value = line.split('Given', 1)[1].strip()
			previous_step = {'keyword': 'GIVEN', 'value': value}
			steps.append(previous_step)
			steps_count += 1
		elif line.strip().upper().startswith('WHEN'):
			previous_keyword = 'WHEN'
			value = line.split('When', 1)[1].strip()
			previous_step = {'keyword': 'WHEN', 'value': value}
			steps.append(previous_step)
			steps_count += 1
		elif line.strip().upper().startswith('THEN'):
			previous_keyword = 'THEN'
			value = line.split('Then', 1)[1].strip()
			previous_step = {'keyword': 'THEN', 'value': value}
			steps.append(previous_step)
			steps_count += 1
		elif line.strip().upper().startswith('AND'):
			value = line.split('And', 1)[1].strip()
			if previous_keyword == 'GIVEN':
				steps.append({'keyword': 'GIVEN', 'value': value})
			elif previous_keyword == 'WHEN':
				steps.append({'keyword': 'WHEN', 'value': value})
			elif previous_keyword == 'THEN':
				steps.append({'keyword': 'THEN', 'value': value})
		else:
			# Guard against empty lines.
			if line:
				if len(steps) > 1:
					# A continuation of the previous step broken into multiple lines.
					value = line.strip()
					previous_step['value'] += '\\n"\n"{}'.format(value)
					#steps[steps_count-1]['value'] += '\\n"\n"{}'.format(value)

	return steps

def generate_catch_scenario(steps):
	given_depth = 0
	when_depth = 0
	catch_str = ''
	for step in steps:
		if step['keyword'] == 'GIVEN':
			given_depth += 1
			catch_str += '{}{{\n'.format(build_catch_given(step['value']))
		elif step['keyword'] == 'WHEN':
			when_depth += 1
			catch_str += '{}{{\n'.format(build_catch_when(step['value']))
		elif step['keyword'] == 'THEN':
			catch_str += '{}{{\n}}\n'.format(build_catch_then(step['value']))
			for i in range(when_depth):
				catch_str += '}\n'
				when_depth -= 1
		elif step['keyword'] == 'SCENARIO':
			catch_str += '{}{{\n'.format(build_catch_scenario(step['value']))
	for i in range(given_depth):
		catch_str += '}\n'
		given_depth -= 1
	# Close out the Scenario.
	catch_str += '}\n'
	return catch_str

def main():
	args = docopt(__doc__, version="1.0")
	#print(args)

	if not args['--output']:
		base, ext = os.path.splitext(args['<feature_file>'])
		args['--output'] = base + '.cpp'

	with open(args['<feature_file>'], "r") as feature_file:
		data = feature_file.read()

		scenarios = re.findall(r'(?<=Scenario:)(.*?)(?=Scenario:|\Z)', data, re.DOTALL)

		steps = parse_gherkin_scenario(scenarios[0])

		with open(args['--output'], 'w+') as outfile:
			outfile.write('#include {}\n'.format(args['--include']))
			for scenario in scenarios:
				steps = parse_gherkin_scenario(scenario)
				catch_str = generate_catch_scenario(steps)
				outfile.write(catch_str)

if __name__ == "__main__":
	main()
