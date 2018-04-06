#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This scripts provide a gst-launch wrapper, used for streaming HMSU radio shows.
Author: targy@hmsu.org
"""
import subprocess
import shlex
import shutil
import click


class IceStream:
    """IceStream"""

    def __init__(self, **kwargs):
        """__init__"""

        self.__bitrates = [96, 128, 192, 320]
        self.gst = shutil.which(kwargs.get('gst'))

        if not self.gst:
            self.gst = '/usr/bin/gst-launch-1.0'

        kwargs['gst'] = self.gst
        kwargs['encoder'] = 'lamemp3enc'

        self.__params = kwargs

    def cmd(self):
        """cmd"""

        cmd = '{gst} {source} ! queue ! audioconvert ! {encoder} bitrate={bitrate} '

        if self.__params['bitrate'] not in self.__bitrates:
            raise Exception('Allowd bitrates are: {}'.format(self.__bitrates))

        # save_to
        cmd += '! tee name=t t. ! queue '

        cmd += '! shout2send '

        cmd += 'ip={ip} port={port} password="{password}" mount=/bass -t genre="{genre}" '
        cmd += 'streamname="{streamname}" description="{desc}" '

        # save_to
        self.__params['save_to'] = '{}_{}.mp3'.format(
            self.__params.get('streamname'), self.__params.get('desc')).replace(' ', '_')
        cmd += 't. ! queue ! filesink location={save_to}'

        cmd = shlex.split(cmd.format(**self.__params))
        return cmd

    def execute(self):
        """execute"""
        return subprocess.run(self.cmd())

@click.command()
@click.option('--source', default='alsasrc', help='gst-launch source, default is alsasrc')
@click.option('--bitrate', default=128, help='gst-launch encoder bitrate, default is 128kbps')
@click.option('--ip', default='radio.hmsu.org',
              help='icecast ip or hostname default is radio.hmsu.org')
@click.option('--port', default=8000, help='icecast port default is 8000')
@click.option('--password', help='icecast password')
@click.option('--genre', default='drum and bass',
              help='icecast metadata - stream genre, default is dnb')
@click.option('--streamname', default='HMSU Online Radio',
              help='icecast metadata - stream name, defautl is HMSU Radio')
@click.option('--desc', default='The Colours Of Drum and Bass', help='icecast metadata - stream description aka tcodnb')
def main(**kwargs):
    kwargs['gst'] = 'gst-launch-1.0'
    return IceStream(**kwargs).execute()

if __name__ == "__main__":
    print(main())
