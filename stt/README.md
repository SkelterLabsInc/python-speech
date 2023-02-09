# AIQ.TALK STT Python Example

The AIQ.TALK STT API is mostly compatible with the Google Cloud Speech API,
so you can use
[Google Cloud Speech Python Client](https://github.com/googleapis/python-speech)
to use AIQ.TALK STT API.

This repository contains simple example CLI programs that recognizes the given
`resources/hello.wav` audio file. Example usages can be found in [Colab example](https://colab.research.google.com/drive/1xT8vJnEcROI7a_4xA8E8sZtsK2_4lh9u#scrollTo=6pTb9KvAgV5E).

## Before you begin

Our examples are based on python 3.7 runtime.

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
$ ./grpc_sync.py --api-key=<your API key>
```

### Streaming speech recognition

Perform streaming request on a local audio file.

```shell
$ ./grpc_stream.py --api-key=<your API key>
```
