This simple Python script takes a [Gherkin][0] feature file and generates a
C++ file using the [Catch2][1] single-header BDD library.

# Requirements

* [Python][2]
* [docopt][3] (used to parse command line)
* _(optional)_ [astyle][4] (to format the .cpp output file)

# Help

    usage:
      gherkin_to_catch.py -h
      gherkin_to_catch.py -v
      gherkin_to_catch.py [--include=<text>] [--output=<output_file>] <feature_file>
    
    options:
      -h, --help            Print this menu
      -v, --version         Print the version
      -o, --output=<file>   The migrated output C++ file.
      --include=<text>      The include line text. [default: <catch.hpp>]


To format the code output from this script the following is recommended:

    astyle --style=allman --indent=tab=4 <input_file>

# Example

Given the following example Gherkin file _Example.feature_:

    Feature: System faults and warnings
    
    Scenario: Verify the system faults are asserted after 2000 milliseconds
    
    	Given I have a System
    	When the 'System Flag X' is 'asserted'
    	Then the 'System Fault A' is 'asserted'
    
    	When 2000 milliseconds elapse
    	Then the 'System Fault B' is 'asserted'

The following command:

    python gherkin_to_catch.py Example.feature

Will produce the following _.cpp_ output file (styled with the Astyle command above):

    #include <catch.hpp>

    SCENARIO( "Verify the system faults are asserted after 2000 milliseconds" )
    {
    	GIVEN( "I have a System" )
    	{
    		WHEN( "the 'System Flag X' is 'asserted'" )
    		{
    			THEN( "the 'System Fault A' is 'asserted'" )
    			{
    			}
    		}
    		WHEN( "2000 milliseconds elapse" )
    		{
    			THEN( "the 'System Fault B' is 'asserted'" )
    			{
    			}
    		}
    	}
    }

[0]: https://docs.cucumber.io/gherkin/reference/
[1]: https://github.com/catchorg/Catch2
[2]: https://www.python.org/downloads/
[3]: https://github.com/docopt/docopt
[4]: http://astyle.sourceforge.net/
