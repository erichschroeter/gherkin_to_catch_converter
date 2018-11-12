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

    astyle --style=allman --indent=tab=4 <output_file>

[0]: https://docs.cucumber.io/gherkin/reference/
[1]: https://github.com/catchorg/Catch2
[2]: https://www.python.org/downloads/
[3]: https://github.com/docopt/docopt
[4]: http://astyle.sourceforge.net/
