# AIQ.STT Python Example

This repository contains simple example CLI programs that recognizes the given
`resources/hello.wav` audio file. Example usages can be found in [Colab example](https://colab.research.google.com/drive/1xT8vJnEcROI7a_4xA8E8sZtsK2_4lh9u#scrollTo=6pTb9KvAgV5E).

## Before you begin

Our examples are based on python 3.8 runtime.

Before running the examples, make sure you've followed the steps.

```shell
$ pip install -U -r ./requirements.txt
```

If you want to use `resources/hello.wav`, you should run the following command:

```
$ git lfs pull
```

Get your AIQ API key from the
[AIQ Console](https://aiq.skelterlabs.com/console).

## Samples

NOTE. We support mono audio only now.

### Synchronously transcribe a local file

Perform synchronous transcription on a local audio file.
Synchronous request supports ~1 minute audio length.

```shell
$ ./recognize.py --api-key=<your API key>
```

### Streaming speech recognition

Perform streaming request on a local audio file.

```shell
$ ./streaming_recognize.py --api-key=<your API key>
```
