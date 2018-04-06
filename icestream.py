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

        self.__bitrates = [96, 128, 192, 320]

        gst = shutil.which('gst-launch-1.0')

        if not gst:
            click.secho('gst-launch-1.0 is required, please install it first', fg='red')
            sys.exit(-1)

        kwargs['gst'] = gst
        self.__params = kwargs

    def cmd(self):
        """cmd"""

        cmd = '{gst} {source} ! queue ! audioconvert ! {encoder} bitrate={bitrate} '

        if self.__params['bitrate'] not in self.__bitrates:
            click.secho('Allowd bitrates are: {}'.format(self.__bitrates))
            sys.exit(-2)

        if self.__params['save_to']:
            cmd += '! tee name=t t. ! queue '

        cmd += '! shout2send '

        cmd += 'ip={ip} port={port} password="{password}" mount=/bass -t genre="{genre}" '
        cmd += 'streamname="{streamname}" description="{desc}" '

        if self.__params['save_to']:
            cmd += 't. ! queue ! filesink location={save_to}'

        cmd = shlex.split(cmd.format(**self.__params))
        return cmd

    def execute(self):
        """execute"""
        return subprocess.run(self.cmd())

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
@click.option('--save-to', help='save stream to file')
def main(**kwargs):
    print(IceStream(**kwargs).execute())

if __name__ == "__main__":
    main()
