#!/usr/bin/env python3
r"""
Dependencies:
    python 3.8

Before executing this script, you should compile protobuf files:
    $ cd proto
    $ make

Usage:
    $ python ssml_synthesize.py \
        --api_key <AIQ api key> \
        --input_path <test.ssml> \
        --output_path <test.wav>
"""

from absl import app
from absl import flags

from google.cloud.texttospeech.v1 import cloud_tts_pb2
from google.cloud.texttospeech.v1 import cloud_tts_pb2_grpc
import grpc_utils

flags.DEFINE_string('api_url', 'aiq.skelterlabs.com:443', 'AIQ portal address.')
flags.DEFINE_string('api_key', None, 'AIQ project api key.')
flags.DEFINE_boolean('insecure', None, 'Use plaintext and insecure connection.')
flags.DEFINE_string('input_path', None, 'Input SSML file path.')
flags.DEFINE_string('output_path', None, 'Output wav path.')
FLAGS = flags.FLAGS


def main(args):
    del args  # Unused

    channel = grpc_utils.create_channel(
        FLAGS.api_url, api_key=FLAGS.api_key, insecure=FLAGS.insecure)
    stub = cloud_tts_pb2_grpc.TextToSpeechStub(channel)

    with open(FLAGS.input_path, 'r', encoding='utf-8') as input_file:
        input_content = input_file.read()

    synthesis_input = cloud_tts_pb2.SynthesisInput(ssml=input_content)
    voice = cloud_tts_pb2.VoiceSelectionParams(
        language_code='ko-KR', name='KO_KR_WOMAN_2')
    audio_config = cloud_tts_pb2.AudioConfig(audio_encoding='LINEAR16')
    request = cloud_tts_pb2.SynthesizeSpeechRequest(
        input=synthesis_input, voice=voice, audio_config=audio_config)
    response = stub.SynthesizeSpeech(request)
    with open(FLAGS.output_path, mode='wb') as output_file:
        output_file.write(response.audio_content)


if __name__ == '__main__':
    flags.mark_flags_as_required(['input_path', 'output_path'])
    app.run(main)
