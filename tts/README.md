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

```shell
$ ./synthesize.py --api-key=<your API key> --output_path <test.wav>
```

### Streaming synthesize text to speech. (alpha)

We offer streaming synthesis for reducing latency of our engine.

```shell
$ ./streaming_synthesize.py --api-key=<your API key> --output_path <test.wav>
```
