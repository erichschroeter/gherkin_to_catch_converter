import unittest

from gherkin_to_catch import gherkin_to_catch

class TestGherkinToCatch1Scenario2When1ThenPer(unittest.TestCase):
	example_scenario = """Feature: System faults and warnings

Scenario: Verify the system faults are asserted after 2000 milliseconds

	Given I have a System
	When the 'System Flag X' is 'asserted'
	Then the 'System Fault A' is 'asserted'

	When 2000 milliseconds elapse
	Then the 'System Fault B' is 'asserted'
"""
	def test_generate_gherkin_scenario(self):
		scenarios = gherkin_to_catch.parse_gherkin_scenarios(self.example_scenario)
		steps = gherkin_to_catch.parse_gherkin_scenario(scenarios[0])
		catch2_text = gherkin_to_catch.generate_catch_scenario(steps)
		expected_text = """SCENARIO( "Verify the system faults are asserted after 2000 milliseconds" ){
GIVEN( "I have a System" ){
WHEN( "the 'System Flag X' is 'asserted'" ){
THEN( "the 'System Fault A' is 'asserted'" ){
}
}
WHEN( "2000 milliseconds elapse" ){
THEN( "the 'System Fault B' is 'asserted'" ){
}
}
}
}
"""
		self.assertEquals(catch2_text, expected_text)
