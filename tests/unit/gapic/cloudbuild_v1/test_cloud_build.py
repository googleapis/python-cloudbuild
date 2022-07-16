# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock
except ImportError:
    import mock

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule


from google.api import httpbody_pb2  # type: ignore
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import future
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import operation
from google.api_core import operation_async  # type: ignore
from google.api_core import operations_v1
from google.api_core import path_template
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.devtools.cloudbuild_v1.services.cloud_build import (
    CloudBuildAsyncClient,
)
from google.cloud.devtools.cloudbuild_v1.services.cloud_build import CloudBuildClient
from google.cloud.devtools.cloudbuild_v1.services.cloud_build import pagers
from google.cloud.devtools.cloudbuild_v1.services.cloud_build import transports
from google.cloud.devtools.cloudbuild_v1.types import cloudbuild
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import any_pb2  # type: ignore
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import google.auth


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert CloudBuildClient._get_default_mtls_endpoint(None) is None
    assert (
        CloudBuildClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        CloudBuildClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        CloudBuildClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        CloudBuildClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert CloudBuildClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (CloudBuildClient, "grpc"),
        (CloudBuildAsyncClient, "grpc_asyncio"),
    ],
)
def test_cloud_build_client_from_service_account_info(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == ("cloudbuild.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.CloudBuildGrpcTransport, "grpc"),
        (transports.CloudBuildGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_cloud_build_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (CloudBuildClient, "grpc"),
        (CloudBuildAsyncClient, "grpc_asyncio"),
    ],
)
def test_cloud_build_client_from_service_account_file(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == ("cloudbuild.googleapis.com:443")


def test_cloud_build_client_get_transport_class():
    transport = CloudBuildClient.get_transport_class()
    available_transports = [
        transports.CloudBuildGrpcTransport,
    ]
    assert transport in available_transports

    transport = CloudBuildClient.get_transport_class("grpc")
    assert transport == transports.CloudBuildGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (CloudBuildClient, transports.CloudBuildGrpcTransport, "grpc"),
        (
            CloudBuildAsyncClient,
            transports.CloudBuildGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    CloudBuildClient, "DEFAULT_ENDPOINT", modify_default_endpoint(CloudBuildClient)
)
@mock.patch.object(
    CloudBuildAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CloudBuildAsyncClient),
)
def test_cloud_build_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(CloudBuildClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(CloudBuildClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class(transport=transport_name)

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class(transport=transport_name)

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )
    # Check the case api_endpoint is provided
    options = client_options.ClientOptions(
        api_audience="https://language.googleapis.com"
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com",
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (CloudBuildClient, transports.CloudBuildGrpcTransport, "grpc", "true"),
        (
            CloudBuildAsyncClient,
            transports.CloudBuildGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (CloudBuildClient, transports.CloudBuildGrpcTransport, "grpc", "false"),
        (
            CloudBuildAsyncClient,
            transports.CloudBuildGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    CloudBuildClient, "DEFAULT_ENDPOINT", modify_default_endpoint(CloudBuildClient)
)
@mock.patch.object(
    CloudBuildAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CloudBuildAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_cloud_build_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client.DEFAULT_ENDPOINT
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client.DEFAULT_ENDPOINT
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                        api_audience=None,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize("client_class", [CloudBuildClient, CloudBuildAsyncClient])
@mock.patch.object(
    CloudBuildClient, "DEFAULT_ENDPOINT", modify_default_endpoint(CloudBuildClient)
)
@mock.patch.object(
    CloudBuildAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CloudBuildAsyncClient),
)
def test_cloud_build_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                return_value=mock_client_cert_source,
            ):
                (
                    api_endpoint,
                    cert_source,
                ) = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (CloudBuildClient, transports.CloudBuildGrpcTransport, "grpc"),
        (
            CloudBuildAsyncClient,
            transports.CloudBuildGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_cloud_build_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (CloudBuildClient, transports.CloudBuildGrpcTransport, "grpc", grpc_helpers),
        (
            CloudBuildAsyncClient,
            transports.CloudBuildGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_cloud_build_client_client_options_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


def test_cloud_build_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.devtools.cloudbuild_v1.services.cloud_build.transports.CloudBuildGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = CloudBuildClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (CloudBuildClient, transports.CloudBuildGrpcTransport, "grpc", grpc_helpers),
        (
            CloudBuildAsyncClient,
            transports.CloudBuildGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_cloud_build_client_create_channel_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # test that the credentials from file are saved and used as the credentials.
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        file_creds = ga_credentials.AnonymousCredentials()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "cloudbuild.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="cloudbuild.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.CreateBuildRequest,
        dict,
    ],
)
def test_create_build(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.CreateBuildRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_build_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_build), "__call__") as call:
        client.create_build()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.CreateBuildRequest()


@pytest.mark.asyncio
async def test_create_build_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.CreateBuildRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.CreateBuildRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_build_async_from_dict():
    await test_create_build_async(request_type=dict)


def test_create_build_field_headers():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.CreateBuildRequest()

    request.project_id = "project_id_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_build), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_build_field_headers_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.CreateBuildRequest()

    request.project_id = "project_id_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_build), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value",
    ) in kw["metadata"]


def test_create_build_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_build(
            project_id="project_id_value",
            build=cloudbuild.Build(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].build
        mock_val = cloudbuild.Build(name="name_value")
        assert arg == mock_val


def test_create_build_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_build(
            cloudbuild.CreateBuildRequest(),
            project_id="project_id_value",
            build=cloudbuild.Build(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_build_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_build(
            project_id="project_id_value",
            build=cloudbuild.Build(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].build
        mock_val = cloudbuild.Build(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_build_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_build(
            cloudbuild.CreateBuildRequest(),
            project_id="project_id_value",
            build=cloudbuild.Build(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.GetBuildRequest,
        dict,
    ],
)
def test_get_build(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.Build(
            name="name_value",
            id="id_value",
            project_id="project_id_value",
            status=cloudbuild.Build.Status.PENDING,
            status_detail="status_detail_value",
            images=["images_value"],
            logs_bucket="logs_bucket_value",
            build_trigger_id="build_trigger_id_value",
            log_url="log_url_value",
            tags=["tags_value"],
            service_account="service_account_value",
        )
        response = client.get_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.GetBuildRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.Build)
    assert response.name == "name_value"
    assert response.id == "id_value"
    assert response.project_id == "project_id_value"
    assert response.status == cloudbuild.Build.Status.PENDING
    assert response.status_detail == "status_detail_value"
    assert response.images == ["images_value"]
    assert response.logs_bucket == "logs_bucket_value"
    assert response.build_trigger_id == "build_trigger_id_value"
    assert response.log_url == "log_url_value"
    assert response.tags == ["tags_value"]
    assert response.service_account == "service_account_value"


def test_get_build_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_build), "__call__") as call:
        client.get_build()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.GetBuildRequest()


@pytest.mark.asyncio
async def test_get_build_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.GetBuildRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.Build(
                name="name_value",
                id="id_value",
                project_id="project_id_value",
                status=cloudbuild.Build.Status.PENDING,
                status_detail="status_detail_value",
                images=["images_value"],
                logs_bucket="logs_bucket_value",
                build_trigger_id="build_trigger_id_value",
                log_url="log_url_value",
                tags=["tags_value"],
                service_account="service_account_value",
            )
        )
        response = await client.get_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.GetBuildRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.Build)
    assert response.name == "name_value"
    assert response.id == "id_value"
    assert response.project_id == "project_id_value"
    assert response.status == cloudbuild.Build.Status.PENDING
    assert response.status_detail == "status_detail_value"
    assert response.images == ["images_value"]
    assert response.logs_bucket == "logs_bucket_value"
    assert response.build_trigger_id == "build_trigger_id_value"
    assert response.log_url == "log_url_value"
    assert response.tags == ["tags_value"]
    assert response.service_account == "service_account_value"


@pytest.mark.asyncio
async def test_get_build_async_from_dict():
    await test_get_build_async(request_type=dict)


def test_get_build_field_headers():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.GetBuildRequest()

    request.project_id = "project_id_value"
    request.id = "id_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_build), "__call__") as call:
        call.return_value = cloudbuild.Build()
        client.get_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value&id=id_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_build_field_headers_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.GetBuildRequest()

    request.project_id = "project_id_value"
    request.id = "id_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_build), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(cloudbuild.Build())
        await client.get_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value&id=id_value",
    ) in kw["metadata"]


def test_get_build_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.Build()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_build(
            project_id="project_id_value",
            id="id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].id
        mock_val = "id_value"
        assert arg == mock_val


def test_get_build_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_build(
            cloudbuild.GetBuildRequest(),
            project_id="project_id_value",
            id="id_value",
        )


@pytest.mark.asyncio
async def test_get_build_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.Build()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(cloudbuild.Build())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_build(
            project_id="project_id_value",
            id="id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].id
        mock_val = "id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_build_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_build(
            cloudbuild.GetBuildRequest(),
            project_id="project_id_value",
            id="id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.ListBuildsRequest,
        dict,
    ],
)
def test_list_builds(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_builds), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListBuildsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_builds(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ListBuildsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBuildsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_builds_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_builds), "__call__") as call:
        client.list_builds()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ListBuildsRequest()


@pytest.mark.asyncio
async def test_list_builds_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.ListBuildsRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_builds), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ListBuildsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_builds(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ListBuildsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBuildsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_builds_async_from_dict():
    await test_list_builds_async(request_type=dict)


def test_list_builds_field_headers():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.ListBuildsRequest()

    request.project_id = "project_id_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_builds), "__call__") as call:
        call.return_value = cloudbuild.ListBuildsResponse()
        client.list_builds(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_builds_field_headers_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.ListBuildsRequest()

    request.project_id = "project_id_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_builds), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ListBuildsResponse()
        )
        await client.list_builds(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value",
    ) in kw["metadata"]


def test_list_builds_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_builds), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListBuildsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_builds(
            project_id="project_id_value",
            filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].filter
        mock_val = "filter_value"
        assert arg == mock_val


def test_list_builds_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_builds(
            cloudbuild.ListBuildsRequest(),
            project_id="project_id_value",
            filter="filter_value",
        )


@pytest.mark.asyncio
async def test_list_builds_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_builds), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListBuildsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ListBuildsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_builds(
            project_id="project_id_value",
            filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].filter
        mock_val = "filter_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_builds_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_builds(
            cloudbuild.ListBuildsRequest(),
            project_id="project_id_value",
            filter="filter_value",
        )


def test_list_builds_pager(transport_name: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_builds), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildsResponse(
                builds=[
                    cloudbuild.Build(),
                    cloudbuild.Build(),
                    cloudbuild.Build(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[],
                next_page_token="def",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[
                    cloudbuild.Build(),
                ],
                next_page_token="ghi",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[
                    cloudbuild.Build(),
                    cloudbuild.Build(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("project_id", ""),)),
        )
        pager = client.list_builds(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, cloudbuild.Build) for i in results)


def test_list_builds_pages(transport_name: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_builds), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildsResponse(
                builds=[
                    cloudbuild.Build(),
                    cloudbuild.Build(),
                    cloudbuild.Build(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[],
                next_page_token="def",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[
                    cloudbuild.Build(),
                ],
                next_page_token="ghi",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[
                    cloudbuild.Build(),
                    cloudbuild.Build(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_builds(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_builds_async_pager():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_builds), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildsResponse(
                builds=[
                    cloudbuild.Build(),
                    cloudbuild.Build(),
                    cloudbuild.Build(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[],
                next_page_token="def",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[
                    cloudbuild.Build(),
                ],
                next_page_token="ghi",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[
                    cloudbuild.Build(),
                    cloudbuild.Build(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_builds(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, cloudbuild.Build) for i in responses)


@pytest.mark.asyncio
async def test_list_builds_async_pages():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_builds), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildsResponse(
                builds=[
                    cloudbuild.Build(),
                    cloudbuild.Build(),
                    cloudbuild.Build(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[],
                next_page_token="def",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[
                    cloudbuild.Build(),
                ],
                next_page_token="ghi",
            ),
            cloudbuild.ListBuildsResponse(
                builds=[
                    cloudbuild.Build(),
                    cloudbuild.Build(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_builds(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.CancelBuildRequest,
        dict,
    ],
)
def test_cancel_build(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.Build(
            name="name_value",
            id="id_value",
            project_id="project_id_value",
            status=cloudbuild.Build.Status.PENDING,
            status_detail="status_detail_value",
            images=["images_value"],
            logs_bucket="logs_bucket_value",
            build_trigger_id="build_trigger_id_value",
            log_url="log_url_value",
            tags=["tags_value"],
            service_account="service_account_value",
        )
        response = client.cancel_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.CancelBuildRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.Build)
    assert response.name == "name_value"
    assert response.id == "id_value"
    assert response.project_id == "project_id_value"
    assert response.status == cloudbuild.Build.Status.PENDING
    assert response.status_detail == "status_detail_value"
    assert response.images == ["images_value"]
    assert response.logs_bucket == "logs_bucket_value"
    assert response.build_trigger_id == "build_trigger_id_value"
    assert response.log_url == "log_url_value"
    assert response.tags == ["tags_value"]
    assert response.service_account == "service_account_value"


def test_cancel_build_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_build), "__call__") as call:
        client.cancel_build()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.CancelBuildRequest()


@pytest.mark.asyncio
async def test_cancel_build_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.CancelBuildRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.Build(
                name="name_value",
                id="id_value",
                project_id="project_id_value",
                status=cloudbuild.Build.Status.PENDING,
                status_detail="status_detail_value",
                images=["images_value"],
                logs_bucket="logs_bucket_value",
                build_trigger_id="build_trigger_id_value",
                log_url="log_url_value",
                tags=["tags_value"],
                service_account="service_account_value",
            )
        )
        response = await client.cancel_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.CancelBuildRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.Build)
    assert response.name == "name_value"
    assert response.id == "id_value"
    assert response.project_id == "project_id_value"
    assert response.status == cloudbuild.Build.Status.PENDING
    assert response.status_detail == "status_detail_value"
    assert response.images == ["images_value"]
    assert response.logs_bucket == "logs_bucket_value"
    assert response.build_trigger_id == "build_trigger_id_value"
    assert response.log_url == "log_url_value"
    assert response.tags == ["tags_value"]
    assert response.service_account == "service_account_value"


@pytest.mark.asyncio
async def test_cancel_build_async_from_dict():
    await test_cancel_build_async(request_type=dict)


def test_cancel_build_field_headers():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.CancelBuildRequest()

    request.project_id = "project_id_value"
    request.id = "id_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_build), "__call__") as call:
        call.return_value = cloudbuild.Build()
        client.cancel_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value&id=id_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_cancel_build_field_headers_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.CancelBuildRequest()

    request.project_id = "project_id_value"
    request.id = "id_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_build), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(cloudbuild.Build())
        await client.cancel_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value&id=id_value",
    ) in kw["metadata"]


def test_cancel_build_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.Build()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.cancel_build(
            project_id="project_id_value",
            id="id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].id
        mock_val = "id_value"
        assert arg == mock_val


def test_cancel_build_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.cancel_build(
            cloudbuild.CancelBuildRequest(),
            project_id="project_id_value",
            id="id_value",
        )


@pytest.mark.asyncio
async def test_cancel_build_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.Build()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(cloudbuild.Build())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.cancel_build(
            project_id="project_id_value",
            id="id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].id
        mock_val = "id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_cancel_build_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.cancel_build(
            cloudbuild.CancelBuildRequest(),
            project_id="project_id_value",
            id="id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.RetryBuildRequest,
        dict,
    ],
)
def test_retry_build(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.retry_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.retry_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.RetryBuildRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_retry_build_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.retry_build), "__call__") as call:
        client.retry_build()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.RetryBuildRequest()


@pytest.mark.asyncio
async def test_retry_build_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.RetryBuildRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.retry_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.retry_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.RetryBuildRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_retry_build_async_from_dict():
    await test_retry_build_async(request_type=dict)


def test_retry_build_field_headers():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.RetryBuildRequest()

    request.project_id = "project_id_value"
    request.id = "id_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.retry_build), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.retry_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value&id=id_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_retry_build_field_headers_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.RetryBuildRequest()

    request.project_id = "project_id_value"
    request.id = "id_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.retry_build), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.retry_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value&id=id_value",
    ) in kw["metadata"]


def test_retry_build_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.retry_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.retry_build(
            project_id="project_id_value",
            id="id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].id
        mock_val = "id_value"
        assert arg == mock_val


def test_retry_build_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.retry_build(
            cloudbuild.RetryBuildRequest(),
            project_id="project_id_value",
            id="id_value",
        )


@pytest.mark.asyncio
async def test_retry_build_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.retry_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.retry_build(
            project_id="project_id_value",
            id="id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].id
        mock_val = "id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_retry_build_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.retry_build(
            cloudbuild.RetryBuildRequest(),
            project_id="project_id_value",
            id="id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.ApproveBuildRequest,
        dict,
    ],
)
def test_approve_build(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.approve_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.approve_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ApproveBuildRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_approve_build_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.approve_build), "__call__") as call:
        client.approve_build()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ApproveBuildRequest()


@pytest.mark.asyncio
async def test_approve_build_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.ApproveBuildRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.approve_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.approve_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ApproveBuildRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_approve_build_async_from_dict():
    await test_approve_build_async(request_type=dict)


def test_approve_build_field_headers():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.ApproveBuildRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.approve_build), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.approve_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_approve_build_field_headers_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.ApproveBuildRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.approve_build), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.approve_build(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_approve_build_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.approve_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.approve_build(
            name="name_value",
            approval_result=cloudbuild.ApprovalResult(
                approver_account="approver_account_value"
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].approval_result
        mock_val = cloudbuild.ApprovalResult(approver_account="approver_account_value")
        assert arg == mock_val


def test_approve_build_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.approve_build(
            cloudbuild.ApproveBuildRequest(),
            name="name_value",
            approval_result=cloudbuild.ApprovalResult(
                approver_account="approver_account_value"
            ),
        )


@pytest.mark.asyncio
async def test_approve_build_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.approve_build), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.approve_build(
            name="name_value",
            approval_result=cloudbuild.ApprovalResult(
                approver_account="approver_account_value"
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].approval_result
        mock_val = cloudbuild.ApprovalResult(approver_account="approver_account_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_approve_build_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.approve_build(
            cloudbuild.ApproveBuildRequest(),
            name="name_value",
            approval_result=cloudbuild.ApprovalResult(
                approver_account="approver_account_value"
            ),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.CreateBuildTriggerRequest,
        dict,
    ],
)
def test_create_build_trigger(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger(
            resource_name="resource_name_value",
            id="id_value",
            description="description_value",
            name="name_value",
            tags=["tags_value"],
            disabled=True,
            ignored_files=["ignored_files_value"],
            included_files=["included_files_value"],
            filter="filter_value",
            service_account="service_account_value",
            autodetect=True,
        )
        response = client.create_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.CreateBuildTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.BuildTrigger)
    assert response.resource_name == "resource_name_value"
    assert response.id == "id_value"
    assert response.description == "description_value"
    assert response.name == "name_value"
    assert response.tags == ["tags_value"]
    assert response.disabled is True
    assert response.ignored_files == ["ignored_files_value"]
    assert response.included_files == ["included_files_value"]
    assert response.filter == "filter_value"
    assert response.service_account == "service_account_value"


def test_create_build_trigger_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_build_trigger), "__call__"
    ) as call:
        client.create_build_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.CreateBuildTriggerRequest()


@pytest.mark.asyncio
async def test_create_build_trigger_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.CreateBuildTriggerRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger(
                resource_name="resource_name_value",
                id="id_value",
                description="description_value",
                name="name_value",
                tags=["tags_value"],
                disabled=True,
                ignored_files=["ignored_files_value"],
                included_files=["included_files_value"],
                filter="filter_value",
                service_account="service_account_value",
            )
        )
        response = await client.create_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.CreateBuildTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.BuildTrigger)
    assert response.resource_name == "resource_name_value"
    assert response.id == "id_value"
    assert response.description == "description_value"
    assert response.name == "name_value"
    assert response.tags == ["tags_value"]
    assert response.disabled is True
    assert response.ignored_files == ["ignored_files_value"]
    assert response.included_files == ["included_files_value"]
    assert response.filter == "filter_value"
    assert response.service_account == "service_account_value"


@pytest.mark.asyncio
async def test_create_build_trigger_async_from_dict():
    await test_create_build_trigger_async(request_type=dict)


def test_create_build_trigger_field_headers():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.CreateBuildTriggerRequest()

    request.project_id = "project_id_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_build_trigger), "__call__"
    ) as call:
        call.return_value = cloudbuild.BuildTrigger()
        client.create_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_build_trigger_field_headers_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.CreateBuildTriggerRequest()

    request.project_id = "project_id_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_build_trigger), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger()
        )
        await client.create_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value",
    ) in kw["metadata"]


def test_create_build_trigger_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_build_trigger(
            project_id="project_id_value",
            trigger=cloudbuild.BuildTrigger(resource_name="resource_name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].trigger
        mock_val = cloudbuild.BuildTrigger(resource_name="resource_name_value")
        assert arg == mock_val


def test_create_build_trigger_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_build_trigger(
            cloudbuild.CreateBuildTriggerRequest(),
            project_id="project_id_value",
            trigger=cloudbuild.BuildTrigger(resource_name="resource_name_value"),
        )


@pytest.mark.asyncio
async def test_create_build_trigger_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_build_trigger(
            project_id="project_id_value",
            trigger=cloudbuild.BuildTrigger(resource_name="resource_name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].trigger
        mock_val = cloudbuild.BuildTrigger(resource_name="resource_name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_build_trigger_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_build_trigger(
            cloudbuild.CreateBuildTriggerRequest(),
            project_id="project_id_value",
            trigger=cloudbuild.BuildTrigger(resource_name="resource_name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.GetBuildTriggerRequest,
        dict,
    ],
)
def test_get_build_trigger(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger(
            resource_name="resource_name_value",
            id="id_value",
            description="description_value",
            name="name_value",
            tags=["tags_value"],
            disabled=True,
            ignored_files=["ignored_files_value"],
            included_files=["included_files_value"],
            filter="filter_value",
            service_account="service_account_value",
            autodetect=True,
        )
        response = client.get_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.GetBuildTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.BuildTrigger)
    assert response.resource_name == "resource_name_value"
    assert response.id == "id_value"
    assert response.description == "description_value"
    assert response.name == "name_value"
    assert response.tags == ["tags_value"]
    assert response.disabled is True
    assert response.ignored_files == ["ignored_files_value"]
    assert response.included_files == ["included_files_value"]
    assert response.filter == "filter_value"
    assert response.service_account == "service_account_value"


def test_get_build_trigger_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_build_trigger), "__call__"
    ) as call:
        client.get_build_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.GetBuildTriggerRequest()


@pytest.mark.asyncio
async def test_get_build_trigger_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.GetBuildTriggerRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger(
                resource_name="resource_name_value",
                id="id_value",
                description="description_value",
                name="name_value",
                tags=["tags_value"],
                disabled=True,
                ignored_files=["ignored_files_value"],
                included_files=["included_files_value"],
                filter="filter_value",
                service_account="service_account_value",
            )
        )
        response = await client.get_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.GetBuildTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.BuildTrigger)
    assert response.resource_name == "resource_name_value"
    assert response.id == "id_value"
    assert response.description == "description_value"
    assert response.name == "name_value"
    assert response.tags == ["tags_value"]
    assert response.disabled is True
    assert response.ignored_files == ["ignored_files_value"]
    assert response.included_files == ["included_files_value"]
    assert response.filter == "filter_value"
    assert response.service_account == "service_account_value"


@pytest.mark.asyncio
async def test_get_build_trigger_async_from_dict():
    await test_get_build_trigger_async(request_type=dict)


def test_get_build_trigger_field_headers():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.GetBuildTriggerRequest()

    request.project_id = "project_id_value"
    request.trigger_id = "trigger_id_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_build_trigger), "__call__"
    ) as call:
        call.return_value = cloudbuild.BuildTrigger()
        client.get_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value&trigger_id=trigger_id_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_build_trigger_field_headers_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.GetBuildTriggerRequest()

    request.project_id = "project_id_value"
    request.trigger_id = "trigger_id_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_build_trigger), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger()
        )
        await client.get_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value&trigger_id=trigger_id_value",
    ) in kw["metadata"]


def test_get_build_trigger_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_build_trigger(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].trigger_id
        mock_val = "trigger_id_value"
        assert arg == mock_val


def test_get_build_trigger_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_build_trigger(
            cloudbuild.GetBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )


@pytest.mark.asyncio
async def test_get_build_trigger_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_build_trigger(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].trigger_id
        mock_val = "trigger_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_build_trigger_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_build_trigger(
            cloudbuild.GetBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.ListBuildTriggersRequest,
        dict,
    ],
)
def test_list_build_triggers(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListBuildTriggersResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_build_triggers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ListBuildTriggersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBuildTriggersPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_build_triggers_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers), "__call__"
    ) as call:
        client.list_build_triggers()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ListBuildTriggersRequest()


@pytest.mark.asyncio
async def test_list_build_triggers_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.ListBuildTriggersRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ListBuildTriggersResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_build_triggers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ListBuildTriggersRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBuildTriggersAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_build_triggers_async_from_dict():
    await test_list_build_triggers_async(request_type=dict)


def test_list_build_triggers_field_headers():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.ListBuildTriggersRequest()

    request.project_id = "project_id_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers), "__call__"
    ) as call:
        call.return_value = cloudbuild.ListBuildTriggersResponse()
        client.list_build_triggers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_build_triggers_field_headers_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.ListBuildTriggersRequest()

    request.project_id = "project_id_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ListBuildTriggersResponse()
        )
        await client.list_build_triggers(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value",
    ) in kw["metadata"]


def test_list_build_triggers_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListBuildTriggersResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_build_triggers(
            project_id="project_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val


def test_list_build_triggers_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_build_triggers(
            cloudbuild.ListBuildTriggersRequest(),
            project_id="project_id_value",
        )


@pytest.mark.asyncio
async def test_list_build_triggers_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListBuildTriggersResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ListBuildTriggersResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_build_triggers(
            project_id="project_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_build_triggers_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_build_triggers(
            cloudbuild.ListBuildTriggersRequest(),
            project_id="project_id_value",
        )


def test_list_build_triggers_pager(transport_name: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[],
                next_page_token="def",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                ],
                next_page_token="ghi",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("project_id", ""),)),
        )
        pager = client.list_build_triggers(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, cloudbuild.BuildTrigger) for i in results)


def test_list_build_triggers_pages(transport_name: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[],
                next_page_token="def",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                ],
                next_page_token="ghi",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_build_triggers(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_build_triggers_async_pager():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[],
                next_page_token="def",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                ],
                next_page_token="ghi",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_build_triggers(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, cloudbuild.BuildTrigger) for i in responses)


@pytest.mark.asyncio
async def test_list_build_triggers_async_pages():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_build_triggers),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[],
                next_page_token="def",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                ],
                next_page_token="ghi",
            ),
            cloudbuild.ListBuildTriggersResponse(
                triggers=[
                    cloudbuild.BuildTrigger(),
                    cloudbuild.BuildTrigger(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_build_triggers(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.DeleteBuildTriggerRequest,
        dict,
    ],
)
def test_delete_build_trigger(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.DeleteBuildTriggerRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_build_trigger_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_build_trigger), "__call__"
    ) as call:
        client.delete_build_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.DeleteBuildTriggerRequest()


@pytest.mark.asyncio
async def test_delete_build_trigger_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.DeleteBuildTriggerRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.DeleteBuildTriggerRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_build_trigger_async_from_dict():
    await test_delete_build_trigger_async(request_type=dict)


def test_delete_build_trigger_field_headers():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.DeleteBuildTriggerRequest()

    request.project_id = "project_id_value"
    request.trigger_id = "trigger_id_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_build_trigger), "__call__"
    ) as call:
        call.return_value = None
        client.delete_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value&trigger_id=trigger_id_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_build_trigger_field_headers_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.DeleteBuildTriggerRequest()

    request.project_id = "project_id_value"
    request.trigger_id = "trigger_id_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_build_trigger), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value&trigger_id=trigger_id_value",
    ) in kw["metadata"]


def test_delete_build_trigger_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_build_trigger(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].trigger_id
        mock_val = "trigger_id_value"
        assert arg == mock_val


def test_delete_build_trigger_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_build_trigger(
            cloudbuild.DeleteBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )


@pytest.mark.asyncio
async def test_delete_build_trigger_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_build_trigger(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].trigger_id
        mock_val = "trigger_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_build_trigger_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_build_trigger(
            cloudbuild.DeleteBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.UpdateBuildTriggerRequest,
        dict,
    ],
)
def test_update_build_trigger(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger(
            resource_name="resource_name_value",
            id="id_value",
            description="description_value",
            name="name_value",
            tags=["tags_value"],
            disabled=True,
            ignored_files=["ignored_files_value"],
            included_files=["included_files_value"],
            filter="filter_value",
            service_account="service_account_value",
            autodetect=True,
        )
        response = client.update_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.UpdateBuildTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.BuildTrigger)
    assert response.resource_name == "resource_name_value"
    assert response.id == "id_value"
    assert response.description == "description_value"
    assert response.name == "name_value"
    assert response.tags == ["tags_value"]
    assert response.disabled is True
    assert response.ignored_files == ["ignored_files_value"]
    assert response.included_files == ["included_files_value"]
    assert response.filter == "filter_value"
    assert response.service_account == "service_account_value"


def test_update_build_trigger_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_build_trigger), "__call__"
    ) as call:
        client.update_build_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.UpdateBuildTriggerRequest()


@pytest.mark.asyncio
async def test_update_build_trigger_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.UpdateBuildTriggerRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger(
                resource_name="resource_name_value",
                id="id_value",
                description="description_value",
                name="name_value",
                tags=["tags_value"],
                disabled=True,
                ignored_files=["ignored_files_value"],
                included_files=["included_files_value"],
                filter="filter_value",
                service_account="service_account_value",
            )
        )
        response = await client.update_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.UpdateBuildTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.BuildTrigger)
    assert response.resource_name == "resource_name_value"
    assert response.id == "id_value"
    assert response.description == "description_value"
    assert response.name == "name_value"
    assert response.tags == ["tags_value"]
    assert response.disabled is True
    assert response.ignored_files == ["ignored_files_value"]
    assert response.included_files == ["included_files_value"]
    assert response.filter == "filter_value"
    assert response.service_account == "service_account_value"


@pytest.mark.asyncio
async def test_update_build_trigger_async_from_dict():
    await test_update_build_trigger_async(request_type=dict)


def test_update_build_trigger_field_headers():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.UpdateBuildTriggerRequest()

    request.project_id = "project_id_value"
    request.trigger_id = "trigger_id_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_build_trigger), "__call__"
    ) as call:
        call.return_value = cloudbuild.BuildTrigger()
        client.update_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value&trigger_id=trigger_id_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_build_trigger_field_headers_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.UpdateBuildTriggerRequest()

    request.project_id = "project_id_value"
    request.trigger_id = "trigger_id_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_build_trigger), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger()
        )
        await client.update_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value&trigger_id=trigger_id_value",
    ) in kw["metadata"]


def test_update_build_trigger_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_build_trigger(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            trigger=cloudbuild.BuildTrigger(resource_name="resource_name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].trigger_id
        mock_val = "trigger_id_value"
        assert arg == mock_val
        arg = args[0].trigger
        mock_val = cloudbuild.BuildTrigger(resource_name="resource_name_value")
        assert arg == mock_val


def test_update_build_trigger_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_build_trigger(
            cloudbuild.UpdateBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            trigger=cloudbuild.BuildTrigger(resource_name="resource_name_value"),
        )


@pytest.mark.asyncio
async def test_update_build_trigger_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.BuildTrigger()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.BuildTrigger()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_build_trigger(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            trigger=cloudbuild.BuildTrigger(resource_name="resource_name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].trigger_id
        mock_val = "trigger_id_value"
        assert arg == mock_val
        arg = args[0].trigger
        mock_val = cloudbuild.BuildTrigger(resource_name="resource_name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_build_trigger_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_build_trigger(
            cloudbuild.UpdateBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            trigger=cloudbuild.BuildTrigger(resource_name="resource_name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.RunBuildTriggerRequest,
        dict,
    ],
)
def test_run_build_trigger(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.run_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.RunBuildTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_run_build_trigger_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_build_trigger), "__call__"
    ) as call:
        client.run_build_trigger()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.RunBuildTriggerRequest()


@pytest.mark.asyncio
async def test_run_build_trigger_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.RunBuildTriggerRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.run_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.RunBuildTriggerRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_run_build_trigger_async_from_dict():
    await test_run_build_trigger_async(request_type=dict)


def test_run_build_trigger_field_headers():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.RunBuildTriggerRequest()

    request.project_id = "project_id_value"
    request.trigger_id = "trigger_id_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_build_trigger), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.run_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value&trigger_id=trigger_id_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_run_build_trigger_field_headers_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.RunBuildTriggerRequest()

    request.project_id = "project_id_value"
    request.trigger_id = "trigger_id_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_build_trigger), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.run_build_trigger(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value&trigger_id=trigger_id_value",
    ) in kw["metadata"]


def test_run_build_trigger_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.run_build_trigger(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            source=cloudbuild.RepoSource(project_id="project_id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].trigger_id
        mock_val = "trigger_id_value"
        assert arg == mock_val
        arg = args[0].source
        mock_val = cloudbuild.RepoSource(project_id="project_id_value")
        assert arg == mock_val


def test_run_build_trigger_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.run_build_trigger(
            cloudbuild.RunBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            source=cloudbuild.RepoSource(project_id="project_id_value"),
        )


@pytest.mark.asyncio
async def test_run_build_trigger_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.run_build_trigger), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.run_build_trigger(
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            source=cloudbuild.RepoSource(project_id="project_id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].project_id
        mock_val = "project_id_value"
        assert arg == mock_val
        arg = args[0].trigger_id
        mock_val = "trigger_id_value"
        assert arg == mock_val
        arg = args[0].source
        mock_val = cloudbuild.RepoSource(project_id="project_id_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_run_build_trigger_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.run_build_trigger(
            cloudbuild.RunBuildTriggerRequest(),
            project_id="project_id_value",
            trigger_id="trigger_id_value",
            source=cloudbuild.RepoSource(project_id="project_id_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.ReceiveTriggerWebhookRequest,
        dict,
    ],
)
def test_receive_trigger_webhook(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.receive_trigger_webhook), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ReceiveTriggerWebhookResponse()
        response = client.receive_trigger_webhook(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ReceiveTriggerWebhookRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.ReceiveTriggerWebhookResponse)


def test_receive_trigger_webhook_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.receive_trigger_webhook), "__call__"
    ) as call:
        client.receive_trigger_webhook()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ReceiveTriggerWebhookRequest()


@pytest.mark.asyncio
async def test_receive_trigger_webhook_async(
    transport: str = "grpc_asyncio",
    request_type=cloudbuild.ReceiveTriggerWebhookRequest,
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.receive_trigger_webhook), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ReceiveTriggerWebhookResponse()
        )
        response = await client.receive_trigger_webhook(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ReceiveTriggerWebhookRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.ReceiveTriggerWebhookResponse)


@pytest.mark.asyncio
async def test_receive_trigger_webhook_async_from_dict():
    await test_receive_trigger_webhook_async(request_type=dict)


def test_receive_trigger_webhook_field_headers():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.ReceiveTriggerWebhookRequest()

    request.project_id = "project_id_value"
    request.trigger = "trigger_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.receive_trigger_webhook), "__call__"
    ) as call:
        call.return_value = cloudbuild.ReceiveTriggerWebhookResponse()
        client.receive_trigger_webhook(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value&trigger=trigger_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_receive_trigger_webhook_field_headers_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.ReceiveTriggerWebhookRequest()

    request.project_id = "project_id_value"
    request.trigger = "trigger_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.receive_trigger_webhook), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ReceiveTriggerWebhookResponse()
        )
        await client.receive_trigger_webhook(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "project_id=project_id_value&trigger=trigger_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.CreateWorkerPoolRequest,
        dict,
    ],
)
def test_create_worker_pool(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.CreateWorkerPoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_worker_pool_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_worker_pool), "__call__"
    ) as call:
        client.create_worker_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.CreateWorkerPoolRequest()


@pytest.mark.asyncio
async def test_create_worker_pool_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.CreateWorkerPoolRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.CreateWorkerPoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_worker_pool_async_from_dict():
    await test_create_worker_pool_async(request_type=dict)


def test_create_worker_pool_field_headers():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.CreateWorkerPoolRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_worker_pool), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_worker_pool_field_headers_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.CreateWorkerPoolRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_worker_pool), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_worker_pool_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_worker_pool(
            parent="parent_value",
            worker_pool=cloudbuild.WorkerPool(name="name_value"),
            worker_pool_id="worker_pool_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].worker_pool
        mock_val = cloudbuild.WorkerPool(name="name_value")
        assert arg == mock_val
        arg = args[0].worker_pool_id
        mock_val = "worker_pool_id_value"
        assert arg == mock_val


def test_create_worker_pool_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_worker_pool(
            cloudbuild.CreateWorkerPoolRequest(),
            parent="parent_value",
            worker_pool=cloudbuild.WorkerPool(name="name_value"),
            worker_pool_id="worker_pool_id_value",
        )


@pytest.mark.asyncio
async def test_create_worker_pool_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_worker_pool(
            parent="parent_value",
            worker_pool=cloudbuild.WorkerPool(name="name_value"),
            worker_pool_id="worker_pool_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].worker_pool
        mock_val = cloudbuild.WorkerPool(name="name_value")
        assert arg == mock_val
        arg = args[0].worker_pool_id
        mock_val = "worker_pool_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_worker_pool_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_worker_pool(
            cloudbuild.CreateWorkerPoolRequest(),
            parent="parent_value",
            worker_pool=cloudbuild.WorkerPool(name="name_value"),
            worker_pool_id="worker_pool_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.GetWorkerPoolRequest,
        dict,
    ],
)
def test_get_worker_pool(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_worker_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.WorkerPool(
            name="name_value",
            display_name="display_name_value",
            uid="uid_value",
            state=cloudbuild.WorkerPool.State.CREATING,
            etag="etag_value",
            private_pool_v1_config=cloudbuild.PrivatePoolV1Config(
                worker_config=cloudbuild.PrivatePoolV1Config.WorkerConfig(
                    machine_type="machine_type_value"
                )
            ),
        )
        response = client.get_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.GetWorkerPoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.WorkerPool)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.uid == "uid_value"
    assert response.state == cloudbuild.WorkerPool.State.CREATING
    assert response.etag == "etag_value"


def test_get_worker_pool_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_worker_pool), "__call__") as call:
        client.get_worker_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.GetWorkerPoolRequest()


@pytest.mark.asyncio
async def test_get_worker_pool_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.GetWorkerPoolRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_worker_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.WorkerPool(
                name="name_value",
                display_name="display_name_value",
                uid="uid_value",
                state=cloudbuild.WorkerPool.State.CREATING,
                etag="etag_value",
            )
        )
        response = await client.get_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.GetWorkerPoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloudbuild.WorkerPool)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.uid == "uid_value"
    assert response.state == cloudbuild.WorkerPool.State.CREATING
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_get_worker_pool_async_from_dict():
    await test_get_worker_pool_async(request_type=dict)


def test_get_worker_pool_field_headers():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.GetWorkerPoolRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_worker_pool), "__call__") as call:
        call.return_value = cloudbuild.WorkerPool()
        client.get_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_worker_pool_field_headers_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.GetWorkerPoolRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_worker_pool), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.WorkerPool()
        )
        await client.get_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_worker_pool_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_worker_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.WorkerPool()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_worker_pool(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_worker_pool_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_worker_pool(
            cloudbuild.GetWorkerPoolRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_worker_pool_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_worker_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.WorkerPool()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.WorkerPool()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_worker_pool(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_worker_pool_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_worker_pool(
            cloudbuild.GetWorkerPoolRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.DeleteWorkerPoolRequest,
        dict,
    ],
)
def test_delete_worker_pool(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.DeleteWorkerPoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_worker_pool_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_worker_pool), "__call__"
    ) as call:
        client.delete_worker_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.DeleteWorkerPoolRequest()


@pytest.mark.asyncio
async def test_delete_worker_pool_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.DeleteWorkerPoolRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.DeleteWorkerPoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_worker_pool_async_from_dict():
    await test_delete_worker_pool_async(request_type=dict)


def test_delete_worker_pool_field_headers():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.DeleteWorkerPoolRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_worker_pool), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_worker_pool_field_headers_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.DeleteWorkerPoolRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_worker_pool), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_worker_pool_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_worker_pool(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_worker_pool_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_worker_pool(
            cloudbuild.DeleteWorkerPoolRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_worker_pool_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_worker_pool(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_worker_pool_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_worker_pool(
            cloudbuild.DeleteWorkerPoolRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.UpdateWorkerPoolRequest,
        dict,
    ],
)
def test_update_worker_pool(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.UpdateWorkerPoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_worker_pool_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_worker_pool), "__call__"
    ) as call:
        client.update_worker_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.UpdateWorkerPoolRequest()


@pytest.mark.asyncio
async def test_update_worker_pool_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.UpdateWorkerPoolRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.UpdateWorkerPoolRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_worker_pool_async_from_dict():
    await test_update_worker_pool_async(request_type=dict)


def test_update_worker_pool_field_headers():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.UpdateWorkerPoolRequest()

    request.worker_pool.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_worker_pool), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "worker_pool.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_worker_pool_field_headers_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.UpdateWorkerPoolRequest()

    request.worker_pool.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_worker_pool), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_worker_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "worker_pool.name=name_value",
    ) in kw["metadata"]


def test_update_worker_pool_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_worker_pool(
            worker_pool=cloudbuild.WorkerPool(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].worker_pool
        mock_val = cloudbuild.WorkerPool(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_worker_pool_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_worker_pool(
            cloudbuild.UpdateWorkerPoolRequest(),
            worker_pool=cloudbuild.WorkerPool(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_worker_pool_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_worker_pool), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_worker_pool(
            worker_pool=cloudbuild.WorkerPool(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].worker_pool
        mock_val = cloudbuild.WorkerPool(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_worker_pool_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_worker_pool(
            cloudbuild.UpdateWorkerPoolRequest(),
            worker_pool=cloudbuild.WorkerPool(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudbuild.ListWorkerPoolsRequest,
        dict,
    ],
)
def test_list_worker_pools(request_type, transport: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_worker_pools), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListWorkerPoolsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_worker_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ListWorkerPoolsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListWorkerPoolsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_worker_pools_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_worker_pools), "__call__"
    ) as call:
        client.list_worker_pools()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ListWorkerPoolsRequest()


@pytest.mark.asyncio
async def test_list_worker_pools_async(
    transport: str = "grpc_asyncio", request_type=cloudbuild.ListWorkerPoolsRequest
):
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_worker_pools), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ListWorkerPoolsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_worker_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudbuild.ListWorkerPoolsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListWorkerPoolsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_worker_pools_async_from_dict():
    await test_list_worker_pools_async(request_type=dict)


def test_list_worker_pools_field_headers():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.ListWorkerPoolsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_worker_pools), "__call__"
    ) as call:
        call.return_value = cloudbuild.ListWorkerPoolsResponse()
        client.list_worker_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_worker_pools_field_headers_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudbuild.ListWorkerPoolsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_worker_pools), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ListWorkerPoolsResponse()
        )
        await client.list_worker_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_worker_pools_flattened():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_worker_pools), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListWorkerPoolsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_worker_pools(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_worker_pools_flattened_error():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_worker_pools(
            cloudbuild.ListWorkerPoolsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_worker_pools_flattened_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_worker_pools), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudbuild.ListWorkerPoolsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudbuild.ListWorkerPoolsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_worker_pools(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_worker_pools_flattened_error_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_worker_pools(
            cloudbuild.ListWorkerPoolsRequest(),
            parent="parent_value",
        )


def test_list_worker_pools_pager(transport_name: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_worker_pools), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[
                    cloudbuild.WorkerPool(),
                    cloudbuild.WorkerPool(),
                    cloudbuild.WorkerPool(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[],
                next_page_token="def",
            ),
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[
                    cloudbuild.WorkerPool(),
                ],
                next_page_token="ghi",
            ),
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[
                    cloudbuild.WorkerPool(),
                    cloudbuild.WorkerPool(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_worker_pools(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, cloudbuild.WorkerPool) for i in results)


def test_list_worker_pools_pages(transport_name: str = "grpc"):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_worker_pools), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[
                    cloudbuild.WorkerPool(),
                    cloudbuild.WorkerPool(),
                    cloudbuild.WorkerPool(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[],
                next_page_token="def",
            ),
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[
                    cloudbuild.WorkerPool(),
                ],
                next_page_token="ghi",
            ),
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[
                    cloudbuild.WorkerPool(),
                    cloudbuild.WorkerPool(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_worker_pools(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_worker_pools_async_pager():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_worker_pools),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[
                    cloudbuild.WorkerPool(),
                    cloudbuild.WorkerPool(),
                    cloudbuild.WorkerPool(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[],
                next_page_token="def",
            ),
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[
                    cloudbuild.WorkerPool(),
                ],
                next_page_token="ghi",
            ),
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[
                    cloudbuild.WorkerPool(),
                    cloudbuild.WorkerPool(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_worker_pools(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, cloudbuild.WorkerPool) for i in responses)


@pytest.mark.asyncio
async def test_list_worker_pools_async_pages():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_worker_pools),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[
                    cloudbuild.WorkerPool(),
                    cloudbuild.WorkerPool(),
                    cloudbuild.WorkerPool(),
                ],
                next_page_token="abc",
            ),
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[],
                next_page_token="def",
            ),
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[
                    cloudbuild.WorkerPool(),
                ],
                next_page_token="ghi",
            ),
            cloudbuild.ListWorkerPoolsResponse(
                worker_pools=[
                    cloudbuild.WorkerPool(),
                    cloudbuild.WorkerPool(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_worker_pools(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.CloudBuildGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.CloudBuildGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudBuildClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.CloudBuildGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = CloudBuildClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = CloudBuildClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.CloudBuildGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudBuildClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CloudBuildGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = CloudBuildClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CloudBuildGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.CloudBuildGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CloudBuildGrpcTransport,
        transports.CloudBuildGrpcAsyncIOTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
    ],
)
def test_transport_kind(transport_name):
    transport = CloudBuildClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.CloudBuildGrpcTransport,
    )


def test_cloud_build_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.CloudBuildTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_cloud_build_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.devtools.cloudbuild_v1.services.cloud_build.transports.CloudBuildTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.CloudBuildTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_build",
        "get_build",
        "list_builds",
        "cancel_build",
        "retry_build",
        "approve_build",
        "create_build_trigger",
        "get_build_trigger",
        "list_build_triggers",
        "delete_build_trigger",
        "update_build_trigger",
        "run_build_trigger",
        "receive_trigger_webhook",
        "create_worker_pool",
        "get_worker_pool",
        "delete_worker_pool",
        "update_worker_pool",
        "list_worker_pools",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client

    # Catch all for all remaining methods and properties
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_cloud_build_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.devtools.cloudbuild_v1.services.cloud_build.transports.CloudBuildTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.CloudBuildTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_cloud_build_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.devtools.cloudbuild_v1.services.cloud_build.transports.CloudBuildTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.CloudBuildTransport()
        adc.assert_called_once()


def test_cloud_build_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        CloudBuildClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CloudBuildGrpcTransport,
        transports.CloudBuildGrpcAsyncIOTransport,
    ],
)
def test_cloud_build_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CloudBuildGrpcTransport,
        transports.CloudBuildGrpcAsyncIOTransport,
    ],
)
def test_cloud_build_transport_auth_gdch_credentials(transport_class):
    host = "https://language.com"
    api_audience_tests = [None, "https://language2.com"]
    api_audience_expect = [host, "https://language2.com"]
    for t, e in zip(api_audience_tests, api_audience_expect):
        with mock.patch.object(google.auth, "default", autospec=True) as adc:
            gdch_mock = mock.MagicMock()
            type(gdch_mock).with_gdch_audience = mock.PropertyMock(
                return_value=gdch_mock
            )
            adc.return_value = (gdch_mock, None)
            transport_class(host=host, api_audience=t)
            gdch_mock.with_gdch_audience.assert_called_once_with(e)


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.CloudBuildGrpcTransport, grpc_helpers),
        (transports.CloudBuildGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_cloud_build_transport_create_channel(transport_class, grpc_helpers):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])

        create_channel.assert_called_with(
            "cloudbuild.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="cloudbuild.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.CloudBuildGrpcTransport, transports.CloudBuildGrpcAsyncIOTransport],
)
def test_cloud_build_grpc_transport_client_cert_source_for_mtls(transport_class):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds,
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback,
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert, private_key=expected_key
            )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_cloud_build_host_no_port(transport_name):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudbuild.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("cloudbuild.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_cloud_build_host_with_port(transport_name):
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudbuild.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("cloudbuild.googleapis.com:8000")


def test_cloud_build_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.CloudBuildGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_cloud_build_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.CloudBuildGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [transports.CloudBuildGrpcTransport, transports.CloudBuildGrpcAsyncIOTransport],
)
def test_cloud_build_transport_channel_mtls_with_client_cert_source(transport_class):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [transports.CloudBuildGrpcTransport, transports.CloudBuildGrpcAsyncIOTransport],
)
def test_cloud_build_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_cloud_build_grpc_lro_client():
    client = CloudBuildClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_cloud_build_grpc_lro_async_client():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsAsyncClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_build_path():
    project = "squid"
    build = "clam"
    expected = "projects/{project}/builds/{build}".format(
        project=project,
        build=build,
    )
    actual = CloudBuildClient.build_path(project, build)
    assert expected == actual


def test_parse_build_path():
    expected = {
        "project": "whelk",
        "build": "octopus",
    }
    path = CloudBuildClient.build_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_build_path(path)
    assert expected == actual


def test_build_trigger_path():
    project = "oyster"
    trigger = "nudibranch"
    expected = "projects/{project}/triggers/{trigger}".format(
        project=project,
        trigger=trigger,
    )
    actual = CloudBuildClient.build_trigger_path(project, trigger)
    assert expected == actual


def test_parse_build_trigger_path():
    expected = {
        "project": "cuttlefish",
        "trigger": "mussel",
    }
    path = CloudBuildClient.build_trigger_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_build_trigger_path(path)
    assert expected == actual


def test_crypto_key_path():
    project = "winkle"
    location = "nautilus"
    keyring = "scallop"
    key = "abalone"
    expected = "projects/{project}/locations/{location}/keyRings/{keyring}/cryptoKeys/{key}".format(
        project=project,
        location=location,
        keyring=keyring,
        key=key,
    )
    actual = CloudBuildClient.crypto_key_path(project, location, keyring, key)
    assert expected == actual


def test_parse_crypto_key_path():
    expected = {
        "project": "squid",
        "location": "clam",
        "keyring": "whelk",
        "key": "octopus",
    }
    path = CloudBuildClient.crypto_key_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_crypto_key_path(path)
    assert expected == actual


def test_network_path():
    project = "oyster"
    network = "nudibranch"
    expected = "projects/{project}/global/networks/{network}".format(
        project=project,
        network=network,
    )
    actual = CloudBuildClient.network_path(project, network)
    assert expected == actual


def test_parse_network_path():
    expected = {
        "project": "cuttlefish",
        "network": "mussel",
    }
    path = CloudBuildClient.network_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_network_path(path)
    assert expected == actual


def test_secret_version_path():
    project = "winkle"
    secret = "nautilus"
    version = "scallop"
    expected = "projects/{project}/secrets/{secret}/versions/{version}".format(
        project=project,
        secret=secret,
        version=version,
    )
    actual = CloudBuildClient.secret_version_path(project, secret, version)
    assert expected == actual


def test_parse_secret_version_path():
    expected = {
        "project": "abalone",
        "secret": "squid",
        "version": "clam",
    }
    path = CloudBuildClient.secret_version_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_secret_version_path(path)
    assert expected == actual


def test_service_account_path():
    project = "whelk"
    service_account = "octopus"
    expected = "projects/{project}/serviceAccounts/{service_account}".format(
        project=project,
        service_account=service_account,
    )
    actual = CloudBuildClient.service_account_path(project, service_account)
    assert expected == actual


def test_parse_service_account_path():
    expected = {
        "project": "oyster",
        "service_account": "nudibranch",
    }
    path = CloudBuildClient.service_account_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_service_account_path(path)
    assert expected == actual


def test_subscription_path():
    project = "cuttlefish"
    subscription = "mussel"
    expected = "projects/{project}/subscriptions/{subscription}".format(
        project=project,
        subscription=subscription,
    )
    actual = CloudBuildClient.subscription_path(project, subscription)
    assert expected == actual


def test_parse_subscription_path():
    expected = {
        "project": "winkle",
        "subscription": "nautilus",
    }
    path = CloudBuildClient.subscription_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_subscription_path(path)
    assert expected == actual


def test_topic_path():
    project = "scallop"
    topic = "abalone"
    expected = "projects/{project}/topics/{topic}".format(
        project=project,
        topic=topic,
    )
    actual = CloudBuildClient.topic_path(project, topic)
    assert expected == actual


def test_parse_topic_path():
    expected = {
        "project": "squid",
        "topic": "clam",
    }
    path = CloudBuildClient.topic_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_topic_path(path)
    assert expected == actual


def test_worker_pool_path():
    project = "whelk"
    location = "octopus"
    worker_pool = "oyster"
    expected = (
        "projects/{project}/locations/{location}/workerPools/{worker_pool}".format(
            project=project,
            location=location,
            worker_pool=worker_pool,
        )
    )
    actual = CloudBuildClient.worker_pool_path(project, location, worker_pool)
    assert expected == actual


def test_parse_worker_pool_path():
    expected = {
        "project": "nudibranch",
        "location": "cuttlefish",
        "worker_pool": "mussel",
    }
    path = CloudBuildClient.worker_pool_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_worker_pool_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "winkle"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = CloudBuildClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nautilus",
    }
    path = CloudBuildClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "scallop"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = CloudBuildClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "abalone",
    }
    path = CloudBuildClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "squid"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = CloudBuildClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "clam",
    }
    path = CloudBuildClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "whelk"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = CloudBuildClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "octopus",
    }
    path = CloudBuildClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "oyster"
    location = "nudibranch"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = CloudBuildClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
    }
    path = CloudBuildClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudBuildClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.CloudBuildTransport, "_prep_wrapped_messages"
    ) as prep:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.CloudBuildTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = CloudBuildClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = CloudBuildAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close():
    transports = {
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        with mock.patch.object(
            type(getattr(client.transport, close_name)), "close"
        ) as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()


def test_client_ctx():
    transports = [
        "grpc",
    ]
    for transport in transports:
        client = CloudBuildClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()


@pytest.mark.parametrize(
    "client_class,transport_class",
    [
        (CloudBuildClient, transports.CloudBuildGrpcTransport),
        (CloudBuildAsyncClient, transports.CloudBuildGrpcAsyncIOTransport),
    ],
)
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
