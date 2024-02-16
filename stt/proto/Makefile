PROTOC = python -m grpc_tools.protoc

all:
	$(PROTOC) \
	  --python_out=../ \
	  --grpc_python_out=../ \
	  --proto_path=. \
	  ./google/*/*.proto \
	  ./google/*/*/*.proto
