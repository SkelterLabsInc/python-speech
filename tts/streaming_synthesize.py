#!/usr/bin/env python3
"""
Experimental streaming example. (alpha)

Dependencies:
    python 3.8

Usage:
    $ python streaming_synthesize.py \\
        --api_key <AIQ api key> --output_path <test.wav>
"""

from absl import app
from absl import flags

import grpc_utils
from google.cloud.texttospeech.v1 import cloud_tts_pb2
from google.cloud.texttospeech.v1 import cloud_tts_pb2_grpc

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
    stub = cloud_tts_pb2_grpc.TextToSpeechStub(channel)

    synthesis_input = cloud_tts_pb2.SynthesisInput(text=FLAGS.text)
    voice = cloud_tts_pb2.VoiceSelectionParams(
        language_code='ko-KR', name='KO_KR_WOMAN_2')
    audio_config = cloud_tts_pb2.AudioConfig(audio_encoding='LINEAR16')
    request = cloud_tts_pb2.SynthesizeSpeechRequest(
        input=synthesis_input, voice=voice, audio_config=audio_config)
    responses = stub.StreamingSynthesizeSpeech(request)
    with open(FLAGS.output_path, mode='wb') as output_file:
        for response in responses:
            output_file.write(response.audio_content)


if __name__ == '__main__':
    flags.mark_flags_as_required(['output_path'])
    app.run(main)
