import unittest

from gherkin_to_catch import gherkin_to_catch

class TestGherkinToCatch2Scenario2When2Then(unittest.TestCase):
	example_scenario = """Feature: System faults and warnings

Scenario: Verify the system faults are asserted after 2000 milliseconds

	Given I have a System
	When the 'System Flag X' is 'asserted'
	Then the 'System Fault A' is 'asserted'
	And the 'System Fault B' is 'deasserted'

	When 2000 milliseconds elapse
	Then the 'System Fault A' is 'deasserted'
	And the 'System Fault B' is 'asserted'

Scenario: Verify the system warnings are asserted after 1000 milliseconds

	Given I have a System
	When the 'System Flag Y' is 'asserted'
	Then the 'System Warning A' is 'deasserted'
	And the 'System Warning B' is 'asserted'

	When 2000 milliseconds elapse
	Then the 'System Warning A' is 'asserted'
	And the 'System Warning B' is 'deasserted'
"""
	def test_generate_gherkin_scenario(self):
		# scenarios = gherkin_to_catch.parse_gherkin_scenarios(self.example_scenario)
		# steps = gherkin_to_catch.parse_gherkin_scenario(scenarios[0])
		catch2_text = gherkin_to_catch.generate_catch_scenarios(self.example_scenario)
		expected_text = """SCENARIO( "Verify the system faults are asserted after 2000 milliseconds" ){
GIVEN( "I have a System" ){
WHEN( "the 'System Flag X' is 'asserted'" ){
THEN( "the 'System Fault A' is 'asserted'" ){
AND_THEN( "the 'System Fault B' is 'deasserted'" ){
}
}
}
WHEN( "2000 milliseconds elapse" ){
THEN( "the 'System Fault A' is 'deasserted'" ){
AND_THEN( "the 'System Fault B' is 'asserted'" ){
}
}
}
}
}
SCENARIO( "Verify the system warnings are asserted after 1000 milliseconds" ){
GIVEN( "I have a System" ){
WHEN( "the 'System Flag Y' is 'asserted'" ){
THEN( "the 'System Warning A' is 'deasserted'" ){
AND_THEN( "the 'System Warning B' is 'asserted'" ){
}
}
}
WHEN( "2000 milliseconds elapse" ){
THEN( "the 'System Warning A' is 'asserted'" ){
AND_THEN( "the 'System Warning B' is 'deasserted'" ){
}
}
}
}
}"""
		self.assertEquals(catch2_text, expected_text)
