#!/usr/bin/env python3
"""
Dependencies:
    - python 3.8

The librosa requires libsndfile.
    macOS) brew install libsndfile
    ubuntu) apt install libsndfile1

Before executing this script, you should compile protobuf files:
    $ cd proto
    $ make

Usage:
    $ python recognize_timestamp.py --api_key <AIQ api key>

NOTE:
    - Input audio duration is less than or equal to 60 seconds.
"""
import datetime

from absl import app
from absl import flags
import librosa
import numpy as np

from google.speech.v1 import cloud_speech_pb2
from google.speech.v1 import cloud_speech_pb2_grpc
import grpc_utils
import utils

flags.DEFINE_string('api_url', 'aiq.skelterlabs.com:443', 'AIQ portal address.')
flags.DEFINE_string('api_key', None, 'AIQ project api key.')
flags.DEFINE_boolean('insecure', None, 'Use plaintext and insecure connection.')
flags.DEFINE_string('audio_path', './resources/hello.wav', 'Input wav path.')
FLAGS = flags.FLAGS


def make_audio(audio_path):
    """Create recognition audio of 16kHz audio encoded as LINEAR16.

    Args:
        audio_path: Audio file path.

    Returns:
        RecognitionAudio object.
    """
    content, sample_rate = librosa.load(audio_path, sr=16000)
    del sample_rate
    if content.dtype in (np.float32, np.float64):
        content = (content * np.iinfo(np.int16).max).astype(np.int16)
    return cloud_speech_pb2.RecognitionAudio(content=content.tobytes())


def time_to_second(time_info):
    """Convert time_info to seconds."""
    if isinstance(time_info, datetime.timedelta):
        return time_info.total_seconds()
    return time_info.seconds + time_info.nanos / 1e9


def main(args):
    del args  # Unused

    channel = grpc_utils.create_channel(
        FLAGS.api_url, api_key=FLAGS.api_key, insecure=FLAGS.insecure)
    stub = cloud_speech_pb2_grpc.SpeechStub(channel)

    audio = make_audio(FLAGS.audio_path)

    # pylint: disable=no-member
    config = cloud_speech_pb2.RecognitionConfig(
        encoding=cloud_speech_pb2.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='ko-KR',
        # Below option is required for timestamp
        enable_word_time_offsets=True)
    # pylint: enable=no-member
    request = cloud_speech_pb2.RecognizeRequest(config=config, audio=audio)
    response = stub.Recognize(request)

    for result in response.results:
        # The alternatives are ordered from most likely to least.
        utils.print_recognition_result(result)


if __name__ == '__main__':
    app.run(main)
