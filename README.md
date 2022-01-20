# gkeeptomd

Google Keep json files converter to markdown.

The json files comes from Google Takeout

# Contributing

Setup python env.

Have python3 installed

    # Create python virtual env
    python3 -m venv .venv

    # Use virtual env
    source .venv/bin/activate

# How to run

Download the source code or the release file.

Have python 3 installed on your system and available in your path.

    usage: convert.py [-h] -i INPUT [-o OUTPUT] [-r] [-a] [-f] [--archivedoutput ARCHIVEDOUTPUT]

    Convert Google Takeout Keep files to Markdown.
    ----------------------------------------------
        convert.py -i some_exported_file.json --o converted.md
        convert.py -i /path/to/input -o /path/to/output -r -a

    optional arguments:
    -h, --help            show this help message and exit
    -i INPUT, --input INPUT
                            Path to input file or directory.
    -o OUTPUT, --output OUTPUT
                            Path to output file or directory.
    -r, --recursive       Directory only. Enable recursive convertion for directories. Not used for individual files. The subdirectories structures will be lost in the output folder.
    -a, --archived        Directory only. Separate archived notes to a separate directory. Default directory "archived"
    -f, --force           Force the file to be read if the extension is not .json. This may break the conversion.
    --archivedoutput ARCHIVEDOUTPUT
                            Path to archived output directory.
