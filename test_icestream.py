import unittest
from unittest.mock import MagicMock
import shutil
import shlex
import icestream

class TestIceStreamClick(unittest.TestCase):

    def setUp(self):
        self.__gst = 'gst-launch-1.0'

        self.__params = {
            'source': 'alsasrc',
            'bitrate': 128,
            'ip': 'radio.hmsu.org',
            'port': 8000,
            'password': None,
            'genre': 'drum and bass',
            'streamname': 'HMSU Online Radio',
            'desc': 'The Colours Of Drum and Bass',
            'gst': 'gst-launch-1.0'
        }


    def test_icestream_without_args(self):
        result = icestream.IceStream(**self.__params).cmd()
        result = shlex.split(result)
        self.assertEqual(result, shlex.split('{} alsasrc ! queue ! audioconvert ! lamemp3enc bitrate=128 ! tee name=t t. ! queue ! shout2send ip=radio.hmsu.org port=8000 password="None" mount=/bass -t genre="drum and bass" streamname="HMSU Online Radio" description="The Colours Of Drum and Bass" t. ! queue ! filesink location=HMSU_Online_Radio_The_Colours_Of_Drum_and_Bass.mp3'.format(self.__gst)))

    def test_icestream_password_args(self):
        self.__params['password'] = 'yourpassword'
        result = icestream.IceStream(**self.__params).cmd()
        result = shlex.split(result)
        self.assertEqual(result, shlex.split('{} alsasrc ! queue ! audioconvert ! lamemp3enc bitrate=128 ! tee name=t t. ! queue ! shout2send ip=radio.hmsu.org port=8000 password="yourpassword" mount=/bass -t genre="drum and bass" streamname="HMSU Online Radio" description="The Colours Of Drum and Bass" t. ! queue ! filesink location=HMSU_Online_Radio_The_Colours_Of_Drum_and_Bass.mp3'.format(self.__gst)))

    def test_icestream_password_bitrate_wrong_args(self):
        self.__params['password'] = 'yourpassword'
        self.__params['bitrate'] = 222
        with self.assertRaises(Exception) as context:
            icestream.IceStream(**self.__params).cmd()
        self.assertTrue('Allowd bitrates are' in str(context.exception))

    def test_icestream_password_bitrate_args(self):
        self.__params['password'] = 'yourpassword'
        self.__params['bitrate'] = 192
        result = icestream.IceStream(**self.__params).cmd()
        result = shlex.split(result)
        self.assertEqual(result, shlex.split('{} alsasrc ! queue ! audioconvert ! lamemp3enc bitrate=192 ! tee name=t t. ! queue ! shout2send ip=radio.hmsu.org port=8000 password="yourpassword" mount=/bass -t genre="drum and bass" streamname="HMSU Online Radio" description="The Colours Of Drum and Bass" t. ! queue ! filesink location=HMSU_Online_Radio_The_Colours_Of_Drum_and_Bass.mp3'.format(self.__gst)))

    def test_icestream_password_bitrate_ip_port_args(self):

        self.__params['password'] = 'yourpassword'
        self.__params['bitrate'] = 192
        self.__params['ip'] = 'radio2.hmsu.org'
        self.__params['port'] = 9999

        result = icestream.IceStream(**self.__params).cmd()
        result = shlex.split(result)
        self.assertEqual(result, shlex.split('{} alsasrc ! queue ! audioconvert ! lamemp3enc bitrate=192 ! tee name=t t. ! queue ! shout2send ip=radio2.hmsu.org port=9999 password="yourpassword" mount=/bass -t genre="drum and bass" streamname="HMSU Online Radio" description="The Colours Of Drum and Bass" t. ! queue ! filesink location=HMSU_Online_Radio_The_Colours_Of_Drum_and_Bass.mp3'.format(self.__gst)))

    def test_icestream_password_bitrate_ip_port_genre_args(self):

        self.__params['password'] = 'yourpassword'
        self.__params['bitrate'] = 192
        self.__params['ip'] = 'radio2.hmsu.org'
        self.__params['port'] = 9999
        self.__params['genre'] = 'dnb'
        self.__params['desc'] = 'dnb desc'
        self.__params['streamname'] = 'dnb stream'

        result = icestream.IceStream(**self.__params).cmd()
        result = shlex.split(result)
        self.assertEqual(result, shlex.split('{} alsasrc ! queue ! audioconvert ! lamemp3enc bitrate=192 ! tee name=t t. ! queue ! shout2send ip=radio2.hmsu.org port=9999 password="yourpassword" mount=/bass -t genre="dnb" streamname="dnb stream" description="dnb desc" t. ! queue ! filesink location=dnb_stream_dnb_desc.mp3'.format(self.__gst)))

    def test_icestream_gst(self):
        result = icestream.IceStream(**self.__params)
        self.assertEqual('gst-launch-1.0', result.gst)

    def test_icestream_execute_with_error(self):
        result = icestream.IceStream(**self.__params)
        res = result.execute('head -n1 README1.md')
        self.assertFalse(res)

    def test_icestream_execute_not_found(self):
        result = icestream.IceStream(**self.__params)

        ices = icestream.IceStream(**self.__params)
        result = ices.execute('head1')
        self.assertFalse(result)
