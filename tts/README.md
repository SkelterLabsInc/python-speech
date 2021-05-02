# AIQ.TALK TTS Python Example

The AIQ.TALK TTS API is mostly compatible with the Google Cloud Text-to-Speech
API, so you can use
[Google Cloud Text-to-Speech Client](https://github.com/googleapis/python-texttospeech)
to use AIQ.TALK TTS API.


## Before you begin

Our examples are based on python 3.7 runtime.

Before running the examples, make sure you've followed the steps.

```shell
$ pip install -U -r ./requirements.txt
```

Get your AIQ API key from the
[AIQ Console](https://aiq.skelterlabs.com/console).

## Samples

### Synchronously synthesize text to speech.

```shell
$ ./grpc_sync.py --api-key=<your API key> --output_path <test.wav>
```

### Streaming synthesize text to speech. (alpha)

We offer streaming synthesis for reducing latency of our engine.

```shell
$ ./grpc_stream.py --api-key=<your API key> --output_path <test.wav>
```
