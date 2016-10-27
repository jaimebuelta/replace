# replace

Replace text in directories

A command line tool to replace text easily and recursively in directories


Usage
-----

    python replace.py [-h] [dir] input_file output_file

It replaces the content of input_file with the content of output_file, 
respecting the indentation level in all the files in `dir`.

For example, for

*input_file*

    self.assertRaises(Error, call, param1, param2)

*output_file*

    with self.assertRaises():
        call(param1, param2)

it will replace occurrences of input for output in all files


Limitations
-----------
- Works only with full lines
- Very early development
- For more syntax aware refactors, take a look at undebt (http://undebt.readthedocs.io/en/latest/)
- Only indentation with spaces, no tabs

To Dos
------
- More tests
- Properly packetize it and make a script
- Use parse (https://github.com/r1chardj0n3s/parse) to allow better control
over replacement, it will probably be never super awesome, but will add tons
of flexibility
- Maye unify the input and output files to replace
