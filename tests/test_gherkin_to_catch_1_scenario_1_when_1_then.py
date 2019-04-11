import unittest

from gherkin_to_catch import gherkin_to_catch

class TestGherkinToCatch1Scenario1When1Then(unittest.TestCase):
	example_scenario = """Feature: System faults and warnings

Scenario: Verify the system warnings are asserted after 2000 milliseconds

	Given I have a System
	When the 'System Flag X' is 'asserted'
	Then the 'System Warning A' is 'asserted'
"""
	def test_generate_gherkin_scenario(self):
		scenarios = gherkin_to_catch.parse_gherkin_scenarios(self.example_scenario)
		steps = gherkin_to_catch.parse_gherkin_scenario(scenarios[0])
		catch2_text = gherkin_to_catch.generate_catch_scenario(steps)
		expected_text = """SCENARIO( "Verify the system warnings are asserted after 2000 milliseconds" ){
GIVEN( "I have a System" ){
WHEN( "the 'System Flag X' is 'asserted'" ){
THEN( "the 'System Warning A' is 'asserted'" ){
}
}
}
}
"""
		self.assertEquals(catch2_text, expected_text)
