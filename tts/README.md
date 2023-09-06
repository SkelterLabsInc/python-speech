# AIQ.TTS Python Example

This repository contains simple example CLI programs that synthesizes the given input text into an audio file.

## Before you begin

Our examples are based on python 3.8 runtime.

Before running the examples, make sure you've followed the steps.

```shell
$ pip install -U -r ./requirements.txt
$ cd proto && make
```

Get your AIQ API key from the
[AIQ Console](https://aiq.skelterlabs.com/console).

## Samples

### Synchronously synthesize text to speech.

To synthesize wav file, run the following:

```shell
$ python synthesize.py \
    --api_key <your API key> \
    --text '안녕하세요?' \
    --output_path <test.wav>
```

If you want other audio format (e.g. ALAW, ADPCM, ...), specify
`--audio_encoding` flag. For the complete list of supported formats, see
`AudioEncoding` in the
[protobuf file](./proto/google/cloud/texttospeech/v1/cloud_tts.proto).

```shell
$ python synthesize.py \
    --api_key <your API key> \
    --text '안녕하세요?' \
    --audio_encoding ADPCM \
    --output_path <test.vox>
```

### Streaming synthesize text to speech. (alpha)

We offer streaming synthesis for reducing latency of our engine.

```shell
$ python streaming_synthesize.py \
    --api_key <your API key> \
    --text '안녕하세요?' \
    --output_path <test.wav>
```

### Synthesize speech with SSML

AIQ.TTS supports pitch, speed, and volume configuration with
[SSML](https://en.wikipedia.org/wiki/Speech_Synthesis_Markup_Language) input.

```shell
$ echo '<speak>SSML 예제</speak>' >/path/to/test.ssml
$ python ssml_synthesize.py \
    --api_key <AIQ api key> \
    --input_path /path/to/test.ssml \
    --output_path /path/to/test.wav
```
