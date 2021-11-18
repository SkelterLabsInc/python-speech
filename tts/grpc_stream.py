#!/usr/bin/env python3
"""
Experimental streaming example. (alpha)

Dependencies:
    python 3.7

Usage:
    $ ./grpc_stream.py --api_key <AIQ api key> --output_path <test.wav>
"""

from absl import app
from absl import flags

import grpc_utils
# NOTE: It will be replaced to Skelter Lab's pip package.
from poodle.tts.server.jimin import compat_google_grpc_pb2
from poodle.tts.server.jimin import compat_google_grpc_pb2_grpc

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
    stub = compat_google_grpc_pb2_grpc.TextToSpeechStub(channel)

    synthesis_input = compat_google_grpc_pb2.SynthesisInput(text=FLAGS.text)
    voice = compat_google_grpc_pb2.VoiceSelectionParams(
        language_code='ko-KR', name='KO_KR_WOMAN_2')
    audio_config = compat_google_grpc_pb2.AudioConfig(audio_encoding='LINEAR16')
    request = compat_google_grpc_pb2.SynthesizeSpeechRequest(
        input=synthesis_input, voice=voice, audio_config=audio_config)
    responses = stub.StreamingSynthesizeSpeech(request)
    with open(FLAGS.output_path, mode='wb') as output_file:
        for response in responses:
            output_file.write(response.audio_content)


if __name__ == '__main__':
    flags.mark_flags_as_required(['output_path'])
    app.run(main)
