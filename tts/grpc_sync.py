#!/usr/bin/env python3
"""
Dependencies:
    python 3.8

Usage:
    $ ./grpc_sync.py --api_key <AIQ api key> --output_path <test.wav>
"""

from absl import app
from absl import flags
from google.cloud import texttospeech
from google.cloud.texttospeech_v1.services.text_to_speech import transports

import grpc_utils

flags.DEFINE_string('api_url', 'aiq.skelterlabs.com:443', 'AIQ portal address.')
flags.DEFINE_string('api_key', None, 'AIQ project api key.')
flags.DEFINE_boolean('insecure', None, 'Use plaintext and insecure connection.')
flags.DEFINE_string('text', '안녕하세요. 스켈터랩스입니다.', 'Input text to synthesize.')
flags.DEFINE_string('output_path', None, 'Output wav path.')
FLAGS = flags.FLAGS


def main(args):
    del args  # Unused

    channel = grpc_utils.create_channel(
        FLAGS.api_url, api_key=FLAGS.api_key, insecure=FLAGS.insecure)
    transport = transports.TextToSpeechGrpcTransport(channel=channel)
    client = texttospeech.TextToSpeechClient(transport=transport)

    synthesis_input = texttospeech.SynthesisInput(text=FLAGS.text)
    voice = texttospeech.VoiceSelectionParams(
        language_code='ko-KR', name='KO_KR_WOMAN_2')
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config)
    with open(FLAGS.output_path, mode='wb') as output_file:
        output_file.write(response.audio_content)


if __name__ == '__main__':
    flags.mark_flags_as_required(['output_path'])
    app.run(main)
