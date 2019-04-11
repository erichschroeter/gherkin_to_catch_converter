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

    astyle --style=allman --indent=tab=4 <input_file>

"""

import os
import re

from docopt import docopt

def build_catch_scenario(text):
	return 'SCENARIO( "{}" )'.format(text)

def build_catch_given(text):
	return 'GIVEN( "{}" )'.format(text)

def build_catch_and_given(text):
	return 'AND_GIVEN( "{}" )'.format(text)

def build_catch_when(text):
	return 'WHEN( "{}" )'.format(text)

def build_catch_and_when(text):
	return 'AND_WHEN( "{}" )'.format(text)

def build_catch_then(text):
	return 'THEN( "{}" )'.format(text)

def build_catch_and_then(text):
	return 'AND_THEN( "{}" )'.format(text)

def parse_gherkin_scenario(scenario_text):
	lines = scenario_text.splitlines()
	steps_count = 0
	steps = []
	previous_keyword = ''
	previous_step = {}
	pattern_GIVEN = re.compile(r'^GIVEN\s*', re.I)
	pattern_WHEN = re.compile(r'^WHEN\s*', re.I)
	pattern_THEN = re.compile(r'^THEN\s*', re.I)
	pattern_AND = re.compile(r'^AND\s*', re.I)

	steps.append({'keyword': 'SCENARIO', 'value': lines[0].strip()})
	steps_count += 1

	for line in lines:
		trimmed_line = line.strip()
		# Guard against empty lines.
		if trimmed_line:
			if pattern_GIVEN.match(trimmed_line):
				previous_keyword = 'GIVEN'
				value = pattern_GIVEN.split(trimmed_line)[1]
				previous_step = {'keyword': 'GIVEN', 'value': value}
				steps.append(previous_step)
				steps_count += 1
			elif pattern_WHEN.match(trimmed_line):
				previous_keyword = 'WHEN'
				value = pattern_WHEN.split(trimmed_line)[1]
				previous_step = {'keyword': 'WHEN', 'value': value}
				steps.append(previous_step)
				steps_count += 1
			elif pattern_THEN.match(trimmed_line):
				previous_keyword = 'THEN'
				value = pattern_THEN.split(trimmed_line)[1]
				previous_step = {'keyword': 'THEN', 'value': value}
				steps.append(previous_step)
				steps_count += 1
			elif pattern_AND.match(trimmed_line):
				value = pattern_AND.split(trimmed_line)[1]
				if previous_keyword == 'GIVEN':
					steps.append({'keyword': 'GIVEN', 'value': value})
				elif previous_keyword == 'WHEN':
					steps.append({'keyword': 'WHEN', 'value': value})
				elif previous_keyword == 'THEN':
					steps.append({'keyword': 'THEN', 'value': value})
			else:
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
	previous_step = ''
	for step in steps:
		if step['keyword'] == 'GIVEN':
			if previous_step == 'GIVEN':
				catch_str = catch_str.rstrip('{\n}\n')
				catch_str += '\n{}{{\n'.format(build_catch_and_given(step['value']))
			else:
				given_depth += 1
				catch_str += '{}{{\n'.format(build_catch_given(step['value']))
		elif step['keyword'] == 'WHEN':
			if previous_step == 'WHEN':
				catch_str = catch_str.rstrip('{\n}\n')
				catch_str += '\n{}{{\n'.format(build_catch_and_when(step['value']))
			else:
				when_depth += 1
				catch_str += '{}{{\n'.format(build_catch_when(step['value']))
				previous_step = 'WHEN'
		elif step['keyword'] == 'THEN':
			if previous_step == 'THEN':
				catch_str = catch_str.rstrip('{\n}\n')
				catch_str += '\n{}{{\n}}\n'.format(build_catch_and_then(step['value']))
			else:
				catch_str += '{}{{\n}}\n'.format(build_catch_then(step['value']))
				for i in range(when_depth):
					catch_str += '}\n'
					when_depth -= 1
				previous_step = 'THEN'
		elif step['keyword'] == 'SCENARIO':
			catch_str += '{}{{\n'.format(build_catch_scenario(step['value']))
	for i in range(given_depth):
		catch_str += '}\n'
		given_depth -= 1
	# Close out the Scenario.
	catch_str += '}\n'
	return catch_str

def parse_gherkin_scenarios(gherkin_string):
		return re.findall(r'(?<=Scenario:)(.*?)(?=Scenario:|\Z)', gherkin_string, re.DOTALL)

def main():
	args = docopt(__doc__, version="1.0")
	#print(args)

	if not args['--output']:
		base, ext = os.path.splitext(args['<feature_file>'])
		args['--output'] = base + '.cpp'

	with open(args['<feature_file>'], "r") as feature_file:
		data = feature_file.read()

		scenarios = parse_gherkin_scenarios(data)

		steps = parse_gherkin_scenario(scenarios[0])

		with open(args['--output'], 'w+') as outfile:
			outfile.write('#include {}\n'.format(args['--include']))
			for scenario in scenarios:
				steps = parse_gherkin_scenario(scenario)
				catch_str = generate_catch_scenario(steps)
				outfile.write(catch_str)

if __name__ == "__main__":
	main()
