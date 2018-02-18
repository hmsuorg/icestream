#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This scripts provide a gst-launch wrapper, used for streaming HMSU radio shows.
Author: targy@hmsu.org
"""
import sys
import subprocess
import shlex
import shutil
import click


class IceStream:
    """IceStream"""

    def __init__(self, **kwargs):
        """__init__"""

        encoders_mux = {
            'vorbisenc': 'oggmux',
            'lamemp3enc': 'id3v2mux'
        }

        bitrates = [96, 128, 192, 320]

        gst = shutil.which('gst-launch-1.0')
        kwargs['ext'] = 'm3u'

        if not gst:
            click.secho('gst-launch-1.0 is required, please install it first', fg='red')
            sys.exit(-1)

        kwargs['gst'] = gst

        if kwargs.get('encoder') in encoders_mux:
            kwargs['mux'] = encoders_mux[kwargs.get('encoder')]
        else:
            click.secho('Unavailable encoder: {}'.format(kwargs.get('encoder')))
            sys.exit(-1)

        cmd = '{gst} {source} ! queue ! audioconvert ! {encoder} bitrate={bitrate} '

        if kwargs['bitrate'] not in bitrates:
            click.secho('Allowd bitrates are: {}'.format(bitrates))
            sys.exit(-2)

        if kwargs['encoder'] == 'vorbisenc':

            kwargs['bitrate'] = int(kwargs.get('bitrate') * 1000)
            cmd += '! {mux} ! shout2send '
            kwargs['ext'] = 'ogg'

        else:
            # we do not need mux here ...
            cmd += '! shout2send '

        cmd += 'ip={ip} port={port} password="{password}" mount=/bass.{ext} -t genre="{genre}" '
        cmd += 'streamname="{streamname}" description="{desc}"'
        self.cmd = shlex.split(cmd.format(**kwargs))

    def execute(self):
        """execute"""
        return subprocess.run(self.cmd)

@click.command()
@click.option('--source', default='alsasrc', help='gst-launch source, default is alsasrc')
@click.option('--encoder', default='lamemp3enc', help='gst-launch encoder, default is lamemp3enc')
@click.option('--bitrate', default=192, help='gst-launch encoder bitrate, default is 192kbps')
@click.option('--ip', default='radio2.hmsu.org',
              help='icecast ip or hostname default is radio2.hmsu.org')
@click.option('--port', default=8000, help='icecast port default is 8000')
@click.option('--password', help='icecast password')
@click.option('--genre', default='drum and bass',
              help='icecast metadata - stream genre, default is dnb')
@click.option('--streamname', default='HMSU Radio',
              help='icecast metadata - stream name, defautl is HMSU Radio')
@click.option('--desc', help='icecast metadata - stream description aka tcodnb')
def main(**kwargs):
    print(IceStream(**kwargs).execute())

if __name__ == "__main__":
    main()
