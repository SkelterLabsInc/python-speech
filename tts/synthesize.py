#!/usr/bin/env python3
r"""
Dependencies:
    python 3.8

Before executing this script, you should compile protobuf files:
    $ cd proto
    $ make

Usage:
    $ python synthesize.py \
        --api_key <your API key> \
        --text '안녕하세요?' \
        --output_path <test.wav>

    If you want other audio format (e.g. ALAW, ADPCM, ...), specify
    `--audio_encoding` flag.

    $ python synthesize.py \
        --api_key <your API key> \
        --text '안녕하세요?' \
        --audio_encoding ADPCM \
        --output_path <test.vox>
"""

from absl import app
from absl import flags

from google.cloud.texttospeech.v1 import cloud_tts_pb2
from google.cloud.texttospeech.v1 import cloud_tts_pb2_grpc
import grpc_utils

# List of supported audio encodings.
# For more detail, see `AudioEncoding` in the following file:
#   ./proto/google/cloud/texttospeech/v1/cloud_tts.proto
AUDIO_ENCODINGS = list(
    cloud_tts_pb2.AudioEncoding.keys())  # ['LINEAR16', 'ALAW', ..., 'ADPCM']

flags.DEFINE_string('api_url', 'aiq.skelterlabs.com:443', 'AIQ portal address.')
flags.DEFINE_string('api_key', None, 'AIQ project api key.')
flags.DEFINE_boolean('insecure', None, 'Use plaintext and insecure connection.')
flags.DEFINE_string('text', '안녕하세요. 스켈터랩스입니다.', 'Input text to synthesize.')
flags.DEFINE_enum(
    'audio_encoding', 'LINEAR16', AUDIO_ENCODINGS,
    'Output audio format encoding. Defaults to LINEAR16 (wav file).')
flags.DEFINE_string('output_path', None, 'Output audio path.')
FLAGS = flags.FLAGS


def main(args):
    del args  # Unused

    channel = grpc_utils.create_channel(
        FLAGS.api_url, api_key=FLAGS.api_key, insecure=FLAGS.insecure)
    stub = cloud_tts_pb2_grpc.TextToSpeechStub(channel)

    synthesis_input = cloud_tts_pb2.SynthesisInput(text=FLAGS.text)
    voice = cloud_tts_pb2.VoiceSelectionParams(
        language_code='ko-KR', name='KO_KR_WOMAN_2')
    audio_config = cloud_tts_pb2.AudioConfig(
        audio_encoding=FLAGS.audio_encoding)
    request = cloud_tts_pb2.SynthesizeSpeechRequest(
        input=synthesis_input, voice=voice, audio_config=audio_config)
    response = stub.SynthesizeSpeech(request)
    with open(FLAGS.output_path, mode='wb') as output_file:
        output_file.write(response.audio_content)


if __name__ == '__main__':
    flags.mark_flags_as_required(['output_path'])
    app.run(main)
