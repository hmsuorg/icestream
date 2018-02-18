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

        gst = shutil.which('gst-launch-1.0')

        if not gst:
            click.secho('gst-launch-1.0 is required, please install it first', fg='red')
            sys.exit(1)

        kwargs['gst'] = gst

        cmd = '{gst} {source} ! queue ! audioconvert ! {encoder} ! oggmux ! shout2send '
        cmd += 'ip={ip} port={port} password="{password}" mount=/bass.ogg -t genre="{genre}" '
        cmd += 'streamname="{streamname}" description="{desc}"'
        self.cmd = shlex.split(cmd.format(**kwargs))

    def execute(self):
        """execute"""
        print(subprocess.run(self.cmd))

@click.command()
@click.option('--source', default='alsasrc', help='gst-launch source, default is alsasrc')
@click.option('--encoder', default='vorbisenc', help='gst-launch encoder, default is vorbisenc')
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
    IceStream(**kwargs).execute()

if __name__ == "__main__":
    main()
