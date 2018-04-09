#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This scripts provide a gst-launch wrapper, used for streaming HMSU radio shows.
Author: targy@hmsu.org
"""
import time
import datetime
import subprocess
import shlex
import click


class IceStream:
    """IceStream"""

    def __init__(self, **kwargs):
        """__init__"""

        self.__bitrates = [96, 128, 192, 320]
        self.gst = kwargs.get('gst')
        self.__params = kwargs

    def cmd(self):
        """cmd"""

        cmd = '{gst} {source} ! queue ! audioconvert ! lamemp3enc bitrate={bitrate} '

        if self.__params['bitrate'] not in self.__bitrates:
            raise Exception('Allowd bitrates are: {}'.format(self.__bitrates))

        # save_to
        cmd += '! tee name=t t. ! queue '

        cmd += '! shout2send ip={ip} port={port} password="{password}" mount=/bass -t genre="{genre}" '
        cmd += 'streamname="{streamname}" description="{desc}" '

        # save_to
        self.__params['save_to'] = '{}_{}.mp3'.format(
            self.__params.get('streamname'), self.__params.get('desc')).replace(' ', '_')
        cmd += 't. ! queue ! filesink location={save_to}'

        return cmd.format(**self.__params)

    def execute(self, cmd):
        """execute"""

        cmd = shlex.split(cmd)

        try:

            with subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:

                click.secho('+++ Connecting to server: {ip} on port: {port} ...'.format(**self.__params), fg='cyan')

                for line in p.stdout:
                    line = line.replace('\n', '')

                    if line.startswith('WARNING'):
                        click.secho('!!! ' + line, fg='yellow')

                    else:
                        click.secho('*** INFO ' + line, fg='green')

                error = p.stderr.readlines()

        except FileNotFoundError:
            # we got this exception in case gst-launch is doesn't installed
            raise FileNotFoundError('gst-launch-1.0 is not installed')

        else:

            if p.returncode != 0:

                error_info = '--- ERROR: {}: {} on port: {}'.format(
                    error[0].split(':')[-1].strip(), self.__params.get('ip'), self.__params.get('port'))

                error_add = error[-1].split(':')[-1].strip().split('=')[-1]

                click.secho('{} -- {}, {}'.format(datetime.datetime.now(), error_info, error_add), fg='red')

                return False

@click.command()
@click.option('--gst', default='gst1-launch-1.0', help='gst-launch executable')
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

    ices = IceStream(**kwargs)
    result = ices.execute(ices.cmd())

    if result is False:
        time.sleep(3)
        ices.execute(ices.cmd())

if __name__ == "__main__":
    main()
