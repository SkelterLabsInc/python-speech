PROTOC = python -m grpc_tools.protoc

all:
	$(PROTOC) --python_out=../ --grpc_python_out=../ -I. ./google/cloud/texttospeech/v1/cloud_tts.proto
