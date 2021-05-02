"""Utility grpc functions."""

import os

import grpc


class AuthGateway(grpc.AuthMetadataPlugin):
    """Authenticate to AIQ APIs using the provided API key."""

    def __init__(self, api_key):
        self._api_key = api_key

    def __call__(self, context, callback):
        """Implement authentication by passing metadata to a callback.

        This method will be invoked asynchronously in a separate thread.

        Args:
            context: An AuthMetadataContext providing information on the RPC
                that the plugin is being called to authenticate.
            callback: An AuthMetadataPluginCallback to be invoked either
                synchronously or asynchronously.
        """
        del context  # Unused
        callback((('x-api-key', self._api_key),), None)


# This code referred.
# https://github.com/grpc/grpc/blob/master/examples/python/interceptors/headers/greeter_client.py
class GenericClientInterceptor(grpc.UnaryUnaryClientInterceptor,
                               grpc.UnaryStreamClientInterceptor,
                               grpc.StreamUnaryClientInterceptor,
                               grpc.StreamStreamClientInterceptor):

    def __init__(self, interceptor_function):
        # pylint: disable=super-init-not-called
        self._fn = interceptor_function

    def intercept_unary_unary(self, continuation, client_call_details, request):
        new_details, new_request_iterator, postprocess = self._fn(
            client_call_details, iter((request,)), False, False)
        response = continuation(new_details, next(new_request_iterator))
        return postprocess(response) if postprocess else response

    def intercept_unary_stream(self, continuation, client_call_details,
                               request):
        new_details, new_request_iterator, postprocess = self._fn(
            client_call_details, iter((request,)), False, True)
        response_it = continuation(new_details, next(new_request_iterator))
        return postprocess(response_it) if postprocess else response_it

    def intercept_stream_unary(self, continuation, client_call_details,
                               request_iterator):
        new_details, new_request_iterator, postprocess = self._fn(
            client_call_details, request_iterator, True, False)
        response = continuation(new_details, new_request_iterator)
        return postprocess(response) if postprocess else response

    def intercept_stream_stream(self, continuation, client_call_details,
                                request_iterator):
        new_details, new_request_iterator, postprocess = self._fn(
            client_call_details, request_iterator, True, True)
        response_it = continuation(new_details, new_request_iterator)
        return postprocess(response_it) if postprocess else response_it


def additional_headers_interceptor(headers):
    """Return interceptor which adds given headers to each calls.

    Args:
        headers: The list of header name, header value pair.
    """

    def _intercept_call(client_call_details, request_iterator,
                        request_streaming, response_streaming):
        del request_streaming  # Unused
        del response_streaming  # Unused
        metadata = []
        if client_call_details.metadata is not None:
            metadata = list(client_call_details.metadata)
        metadata += headers
        client_call_details = client_call_details._replace(metadata=metadata)
        return client_call_details, request_iterator, None

    return GenericClientInterceptor(_intercept_call)


def create_credentials(api_key):
    """Create a ChannelCredentials that authenticates to AIQ via an API key.

    Args:
        api_key: AIQ API key.

    Returns:
        A ChannelCredentials object.
    """
    with open(
            os.path.join(
                os.path.dirname(grpc.__file__),
                '_cython/_credentials/roots.pem'), 'rb') as root_pem_file:
        root_pem = root_pem_file.read()
    channel_credentials = grpc.ssl_channel_credentials(root_pem)

    if not api_key:
        return channel_credentials

    call_credentials = grpc.metadata_call_credentials(AuthGateway(api_key))
    return grpc.composite_channel_credentials(channel_credentials,
                                              call_credentials)


def create_channel(api_url, api_key=None, insecure=None):
    """Create gRPC channel.

    Args:
        api_url: AIQ API url.
        api_key: AIQ API key.
        insecure: Skip server certificate and domain verification.
            If it is None and api_key is specified, insecure is False.
            If it is None and api_key is unspecified, insecure is True.

    Returns:
        grpc.Channel
    """
    if insecure is None:
        insecure = not bool(api_key)

    if not insecure:
        credentials = create_credentials(api_key)
        return grpc.secure_channel(api_url, credentials)

    channel = grpc.insecure_channel(api_url)
    if not api_key:
        return channel

    interceptor = additional_headers_interceptor([('x-api-key', api_key)])
    return grpc.intercept_channel(channel, interceptor)
