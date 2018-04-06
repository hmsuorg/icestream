[![Build Status](https://travis-ci.org/hmsuorg/icestream.svg?branch=master)](https://travis-ci.org/hmsuorg/icestream)
[![PyPI](https://img.shields.io/pypi/pyversions/Django.svg)](https://travis-ci.org/hmsuorg/icestream)

### HMSU Online Radio - Icestream

`icestream.py` is `CLI` tool, that play a role of wrapper, around gst-launch,
used for real time audio streaming, during HMSU Radio shows.

The tool requires `gstream` so you have to ensure it is installed.

#### Installation

First let's clone the project:

    $ git clone https://github.com/hmsuorg/icestream

Next let's install it:

    $ cd icestream
    $ pip install .

#### Usage

For help type:

    $ icestream.py --help

Example usage:

    $ icestream.py --password YOURPASSWORD --desc "HMSU Radio Show" --ip YOUR_ICECAST_SERVER_IP \
        --port 8888

the above command will create `lamemp3enc` and will stream the data to `YOUR_ICECAST_SERVE_IP` on port `8888`.

the default bitrate is `128kbps` if you wish to change the value use the `--bitrate` option.
The valid values are: `96`, `128`, `192`, `320` `kbps`.

#### Testing

    $ python setyp.py test

or

    $ python -m unittest discover

for code coverage:

    $ pip install coverage
    $ coverage run --source=. -m unittest
    $ coverage report -m

#### Contributing

For new a feature we using a `git flow` workflow, so please follow it. When you are ready push your feature.
Then will be merged into a `develop` branch.

Author: **Dimitar Dimitrov** <targy@hmsu.org>
