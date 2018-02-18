### HMSU Icestrem

`icestream.py` is `CLI` tool, that play a role of wrapper, around gst-launch,
used form real time audio streaming, during HMSU Radio shows.

The tool requires `gstream` so you have to ensure it is installed.

For help type:

    $ icestream.py --help

Example usage

    $ icestream.py --password YOURPASSWORD --desc "HMSU Radio Show" --ip YOUR_ICECAST_SERVER_IP \
        --port 8888

the above command will create `lamemp3enc` and will stream the data to `YOUR_ICECAST_SERVE_IP` on port `8888`.

In case you want `vorbisenc`:

    $ icestream.py --encoder vorbisenc --password YOURPASSWORD \
        --desc "HMSU Radio Show" --ip YOUR_ICECAST_SERVER_IP --port 8888

the default bitrate is `192kbps` if you wish to change the value use the `--bitrate` option.
The valid values are: `96`, `128`, `192`, `320` `kbps`.

Author targy@hmsu.org
