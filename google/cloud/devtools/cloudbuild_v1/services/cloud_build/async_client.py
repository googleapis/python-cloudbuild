# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
from collections import OrderedDict
import functools
import re
from typing import Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.devtools.cloudbuild_v1.services.cloud_build import pagers
from google.cloud.devtools.cloudbuild_v1.types import cloudbuild
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import CloudBuildTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import CloudBuildGrpcAsyncIOTransport
from .client import CloudBuildClient


class CloudBuildAsyncClient:
    """Creates and manages builds on Google Cloud Platform.

    The main concept used by this API is a ``Build``, which describes
    the location of the source to build, how to build the source, and
    where to store the built artifacts, if any.

    A user can list previously-requested builds or get builds by their
    ID to determine the status of the build.
    """

    _client: CloudBuildClient

    DEFAULT_ENDPOINT = CloudBuildClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = CloudBuildClient.DEFAULT_MTLS_ENDPOINT

    build_path = staticmethod(CloudBuildClient.build_path)
    parse_build_path = staticmethod(CloudBuildClient.parse_build_path)
    build_trigger_path = staticmethod(CloudBuildClient.build_trigger_path)
    parse_build_trigger_path = staticmethod(CloudBuildClient.parse_build_trigger_path)
    crypto_key_path = staticmethod(CloudBuildClient.crypto_key_path)
    parse_crypto_key_path = staticmethod(CloudBuildClient.parse_crypto_key_path)
    network_path = staticmethod(CloudBuildClient.network_path)
    parse_network_path = staticmethod(CloudBuildClient.parse_network_path)
    secret_version_path = staticmethod(CloudBuildClient.secret_version_path)
    parse_secret_version_path = staticmethod(CloudBuildClient.parse_secret_version_path)
    service_account_path = staticmethod(CloudBuildClient.service_account_path)
    parse_service_account_path = staticmethod(
        CloudBuildClient.parse_service_account_path
    )
    subscription_path = staticmethod(CloudBuildClient.subscription_path)
    parse_subscription_path = staticmethod(CloudBuildClient.parse_subscription_path)
    topic_path = staticmethod(CloudBuildClient.topic_path)
    parse_topic_path = staticmethod(CloudBuildClient.parse_topic_path)
    worker_pool_path = staticmethod(CloudBuildClient.worker_pool_path)
    parse_worker_pool_path = staticmethod(CloudBuildClient.parse_worker_pool_path)
    common_billing_account_path = staticmethod(
        CloudBuildClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        CloudBuildClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(CloudBuildClient.common_folder_path)
    parse_common_folder_path = staticmethod(CloudBuildClient.parse_common_folder_path)
    common_organization_path = staticmethod(CloudBuildClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        CloudBuildClient.parse_common_organization_path
    )
    common_project_path = staticmethod(CloudBuildClient.common_project_path)
    parse_common_project_path = staticmethod(CloudBuildClient.parse_common_project_path)
    common_location_path = staticmethod(CloudBuildClient.common_location_path)
    parse_common_location_path = staticmethod(
        CloudBuildClient.parse_common_location_path
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            CloudBuildAsyncClient: The constructed client.
        """
        return CloudBuildClient.from_service_account_info.__func__(CloudBuildAsyncClient, info, *args, **kwargs)  # type: ignore

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            CloudBuildAsyncClient: The constructed client.
        """
        return CloudBuildClient.from_service_account_file.__func__(CloudBuildAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> CloudBuildTransport:
        """Returns the transport used by the client instance.

        Returns:
            CloudBuildTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(CloudBuildClient).get_transport_class, type(CloudBuildClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, CloudBuildTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the cloud build client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.CloudBuildTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = CloudBuildClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_build(
        self,
        request: cloudbuild.CreateBuildRequest = None,
        *,
        project_id: str = None,
        build: cloudbuild.Build = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Starts a build with the specified configuration.

        This method returns a long-running ``Operation``, which includes
        the build ID. Pass the build ID to ``GetBuild`` to determine the
        build status (such as ``SUCCESS`` or ``FAILURE``).

        Args:
            request (:class:`google.cloud.devtools.cloudbuild_v1.types.CreateBuildRequest`):
                The request object. Request to create a new build.
            project_id (:class:`str`):
                Required. ID of the project.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            build (:class:`google.cloud.devtools.cloudbuild_v1.types.Build`):
                Required. Build resource to create.
                This corresponds to the ``build`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.devtools.cloudbuild_v1.types.Build` A
                build resource in the Cloud Build API.

                   At a high level, a Build describes where to find
                   source code, how to build it (for example, the
                   builder image to run on the source), and where to
                   store the built artifacts.

                   Fields can include the following variables, which
                   will be expanded when the build is created:

                   -  $PROJECT_ID: the project ID of the build.
                   -  $PROJECT_NUMBER: the project number of the build.
                   -  $BUILD_ID: the autogenerated ID of the build.
                   -  $REPO_NAME: the source repository name specified
                      by RepoSource.
                   -  $BRANCH_NAME: the branch name specified by
                      RepoSource.
                   -  $TAG_NAME: the tag name specified by RepoSource.
                   -  $REVISION_ID or $COMMIT_SHA: the commit SHA
                      specified by RepoSource or resolved from the
                      specified branch or tag.
                   -  $SHORT_SHA: first 7 characters of $REVISION_ID or
                      $COMMIT_SHA.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, build])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudbuild.CreateBuildRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if project_id is not None:
            request.project_id = project_id
        if build is not None:
            request.build = build

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_build,
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            cloudbuild.Build,
            metadata_type=cloudbuild.BuildOperationMetadata,
        )

        # Done; return the response.
        return response

    async def get_build(
        self,
        request: cloudbuild.GetBuildRequest = None,
        *,
        project_id: str = None,
        id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloudbuild.Build:
        r"""Returns information about a previously requested build.

        The ``Build`` that is returned includes its status (such as
        ``SUCCESS``, ``FAILURE``, or ``WORKING``), and timing
        information.

        Args:
            request (:class:`google.cloud.devtools.cloudbuild_v1.types.GetBuildRequest`):
                The request object. Request to get a build.
            project_id (:class:`str`):
                Required. ID of the project.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            id (:class:`str`):
                Required. ID of the build.
                This corresponds to the ``id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.devtools.cloudbuild_v1.types.Build:
                A build resource in the Cloud Build API.

                   At a high level, a Build describes where to find
                   source code, how to build it (for example, the
                   builder image to run on the source), and where to
                   store the built artifacts.

                   Fields can include the following variables, which
                   will be expanded when the build is created:

                   -  $PROJECT_ID: the project ID of the build.
                   -  $PROJECT_NUMBER: the project number of the build.
                   -  $BUILD_ID: the autogenerated ID of the build.
                   -  $REPO_NAME: the source repository name specified
                      by RepoSource.
                   -  $BRANCH_NAME: the branch name specified by
                      RepoSource.
                   -  $TAG_NAME: the tag name specified by RepoSource.
                   -  $REVISION_ID or $COMMIT_SHA: the commit SHA
                      specified by RepoSource or resolved from the
                      specified branch or tag.
                   -  $SHORT_SHA: first 7 characters of $REVISION_ID or
                      $COMMIT_SHA.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudbuild.GetBuildRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if project_id is not None:
            request.project_id = project_id
        if id is not None:
            request.id = id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_build,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_builds(
        self,
        request: cloudbuild.ListBuildsRequest = None,
        *,
        project_id: str = None,
        filter: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListBuildsAsyncPager:
        r"""Lists previously requested builds.
        Previously requested builds may still be in-progress, or
        may have finished successfully or unsuccessfully.

        Args:
            request (:class:`google.cloud.devtools.cloudbuild_v1.types.ListBuildsRequest`):
                The request object. Request to list builds.
            project_id (:class:`str`):
                Required. ID of the project.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (:class:`str`):
                The raw filter text to constrain the
                results.

                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.devtools.cloudbuild_v1.services.cloud_build.pagers.ListBuildsAsyncPager:
                Response including listed builds.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, filter])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudbuild.ListBuildsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if project_id is not None:
            request.project_id = project_id
        if filter is not None:
            request.filter = filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_builds,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListBuildsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def cancel_build(
        self,
        request: cloudbuild.CancelBuildRequest = None,
        *,
        project_id: str = None,
        id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloudbuild.Build:
        r"""Cancels a build in progress.

        Args:
            request (:class:`google.cloud.devtools.cloudbuild_v1.types.CancelBuildRequest`):
                The request object. Request to cancel an ongoing build.
            project_id (:class:`str`):
                Required. ID of the project.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            id (:class:`str`):
                Required. ID of the build.
                This corresponds to the ``id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.devtools.cloudbuild_v1.types.Build:
                A build resource in the Cloud Build API.

                   At a high level, a Build describes where to find
                   source code, how to build it (for example, the
                   builder image to run on the source), and where to
                   store the built artifacts.

                   Fields can include the following variables, which
                   will be expanded when the build is created:

                   -  $PROJECT_ID: the project ID of the build.
                   -  $PROJECT_NUMBER: the project number of the build.
                   -  $BUILD_ID: the autogenerated ID of the build.
                   -  $REPO_NAME: the source repository name specified
                      by RepoSource.
                   -  $BRANCH_NAME: the branch name specified by
                      RepoSource.
                   -  $TAG_NAME: the tag name specified by RepoSource.
                   -  $REVISION_ID or $COMMIT_SHA: the commit SHA
                      specified by RepoSource or resolved from the
                      specified branch or tag.
                   -  $SHORT_SHA: first 7 characters of $REVISION_ID or
                      $COMMIT_SHA.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudbuild.CancelBuildRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if project_id is not None:
            request.project_id = project_id
        if id is not None:
            request.id = id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.cancel_build,
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def retry_build(
        self,
        request: cloudbuild.RetryBuildRequest = None,
        *,
        project_id: str = None,
        id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new build based on the specified build.

        This method creates a new build using the original build
        request, which may or may not result in an identical build.

        For triggered builds:

        -  Triggered builds resolve to a precise revision; therefore a
           retry of a triggered build will result in a build that uses
           the same revision.

        For non-triggered builds that specify ``RepoSource``:

        -  If the original build built from the tip of a branch, the
           retried build will build from the tip of that branch, which
           may not be the same revision as the original build.
        -  If the original build specified a commit sha or revision ID,
           the retried build will use the identical source.

        For builds that specify ``StorageSource``:

        -  If the original build pulled source from Google Cloud Storage
           without specifying the generation of the object, the new
           build will use the current object, which may be different
           from the original build source.
        -  If the original build pulled source from Cloud Storage and
           specified the generation of the object, the new build will
           attempt to use the same object, which may or may not be
           available depending on the bucket's lifecycle management
           settings.

        Args:
            request (:class:`google.cloud.devtools.cloudbuild_v1.types.RetryBuildRequest`):
                The request object. Specifies a build to retry.
            project_id (:class:`str`):
                Required. ID of the project.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            id (:class:`str`):
                Required. Build ID of the original
                build.

                This corresponds to the ``id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.devtools.cloudbuild_v1.types.Build` A
                build resource in the Cloud Build API.

                   At a high level, a Build describes where to find
                   source code, how to build it (for example, the
                   builder image to run on the source), and where to
                   store the built artifacts.

                   Fields can include the following variables, which
                   will be expanded when the build is created:

                   -  $PROJECT_ID: the project ID of the build.
                   -  $PROJECT_NUMBER: the project number of the build.
                   -  $BUILD_ID: the autogenerated ID of the build.
                   -  $REPO_NAME: the source repository name specified
                      by RepoSource.
                   -  $BRANCH_NAME: the branch name specified by
                      RepoSource.
                   -  $TAG_NAME: the tag name specified by RepoSource.
                   -  $REVISION_ID or $COMMIT_SHA: the commit SHA
                      specified by RepoSource or resolved from the
                      specified branch or tag.
                   -  $SHORT_SHA: first 7 characters of $REVISION_ID or
                      $COMMIT_SHA.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudbuild.RetryBuildRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if project_id is not None:
            request.project_id = project_id
        if id is not None:
            request.id = id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.retry_build,
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            cloudbuild.Build,
            metadata_type=cloudbuild.BuildOperationMetadata,
        )

        # Done; return the response.
        return response

    async def approve_build(
        self,
        request: cloudbuild.ApproveBuildRequest = None,
        *,
        name: str = None,
        approval_result: cloudbuild.ApprovalResult = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Approves or rejects a pending build.
        If approved, the returned LRO will be analogous to the
        LRO returned from a CreateBuild call.

        If rejected, the returned LRO will be immediately done.

        Args:
            request (:class:`google.cloud.devtools.cloudbuild_v1.types.ApproveBuildRequest`):
                The request object. Request to approve or reject a
                pending build.
            name (:class:`str`):
                Required. Name of the target build. For example:
                "projects/{$project_id}/builds/{$build_id}"

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            approval_result (:class:`google.cloud.devtools.cloudbuild_v1.types.ApprovalResult`):
                Approval decision and metadata.
                This corresponds to the ``approval_result`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.devtools.cloudbuild_v1.types.Build` A
                build resource in the Cloud Build API.

                   At a high level, a Build describes where to find
                   source code, how to build it (for example, the
                   builder image to run on the source), and where to
                   store the built artifacts.

                   Fields can include the following variables, which
                   will be expanded when the build is created:

                   -  $PROJECT_ID: the project ID of the build.
                   -  $PROJECT_NUMBER: the project number of the build.
                   -  $BUILD_ID: the autogenerated ID of the build.
                   -  $REPO_NAME: the source repository name specified
                      by RepoSource.
                   -  $BRANCH_NAME: the branch name specified by
                      RepoSource.
                   -  $TAG_NAME: the tag name specified by RepoSource.
                   -  $REVISION_ID or $COMMIT_SHA: the commit SHA
                      specified by RepoSource or resolved from the
                      specified branch or tag.
                   -  $SHORT_SHA: first 7 characters of $REVISION_ID or
                      $COMMIT_SHA.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, approval_result])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudbuild.ApproveBuildRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if approval_result is not None:
            request.approval_result = approval_result

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.approve_build,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            cloudbuild.Build,
            metadata_type=cloudbuild.BuildOperationMetadata,
        )

        # Done; return the response.
        return response

    async def create_build_trigger(
        self,
        request: cloudbuild.CreateBuildTriggerRequest = None,
        *,
        project_id: str = None,
        trigger: cloudbuild.BuildTrigger = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloudbuild.BuildTrigger:
        r"""Creates a new ``BuildTrigger``.

        This API is experimental.

        Args:
            request (:class:`google.cloud.devtools.cloudbuild_v1.types.CreateBuildTriggerRequest`):
                The request object. Request to create a new
                `BuildTrigger`.
            project_id (:class:`str`):
                Required. ID of the project for which
                to configure automatic builds.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            trigger (:class:`google.cloud.devtools.cloudbuild_v1.types.BuildTrigger`):
                Required. ``BuildTrigger`` to create.
                This corresponds to the ``trigger`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.devtools.cloudbuild_v1.types.BuildTrigger:
                Configuration for an automated build
                in response to source repository
                changes.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, trigger])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudbuild.CreateBuildTriggerRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if project_id is not None:
            request.project_id = project_id
        if trigger is not None:
            request.trigger = trigger

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_build_trigger,
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def get_build_trigger(
        self,
        request: cloudbuild.GetBuildTriggerRequest = None,
        *,
        project_id: str = None,
        trigger_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloudbuild.BuildTrigger:
        r"""Returns information about a ``BuildTrigger``.

        This API is experimental.

        Args:
            request (:class:`google.cloud.devtools.cloudbuild_v1.types.GetBuildTriggerRequest`):
                The request object. Returns the `BuildTrigger` with the
                specified ID.
            project_id (:class:`str`):
                Required. ID of the project that owns
                the trigger.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            trigger_id (:class:`str`):
                Required. Identifier (``id`` or ``name``) of the
                ``BuildTrigger`` to get.

                This corresponds to the ``trigger_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.devtools.cloudbuild_v1.types.BuildTrigger:
                Configuration for an automated build
                in response to source repository
                changes.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, trigger_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudbuild.GetBuildTriggerRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if project_id is not None:
            request.project_id = project_id
        if trigger_id is not None:
            request.trigger_id = trigger_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_build_trigger,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_build_triggers(
        self,
        request: cloudbuild.ListBuildTriggersRequest = None,
        *,
        project_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListBuildTriggersAsyncPager:
        r"""Lists existing ``BuildTrigger``\ s.

        This API is experimental.

        Args:
            request (:class:`google.cloud.devtools.cloudbuild_v1.types.ListBuildTriggersRequest`):
                The request object. Request to list existing
                `BuildTriggers`.
            project_id (:class:`str`):
                Required. ID of the project for which
                to list BuildTriggers.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.devtools.cloudbuild_v1.services.cloud_build.pagers.ListBuildTriggersAsyncPager:
                Response containing existing BuildTriggers.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudbuild.ListBuildTriggersRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if project_id is not None:
            request.project_id = project_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_build_triggers,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListBuildTriggersAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_build_trigger(
        self,
        request: cloudbuild.DeleteBuildTriggerRequest = None,
        *,
        project_id: str = None,
        trigger_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a ``BuildTrigger`` by its project ID and trigger ID.

        This API is experimental.

        Args:
            request (:class:`google.cloud.devtools.cloudbuild_v1.types.DeleteBuildTriggerRequest`):
                The request object. Request to delete a `BuildTrigger`.
            project_id (:class:`str`):
                Required. ID of the project that owns
                the trigger.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            trigger_id (:class:`str`):
                Required. ID of the ``BuildTrigger`` to delete.
                This corresponds to the ``trigger_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, trigger_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudbuild.DeleteBuildTriggerRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if project_id is not None:
            request.project_id = project_id
        if trigger_id is not None:
            request.trigger_id = trigger_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_build_trigger,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        await rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    async def update_build_trigger(
        self,
        request: cloudbuild.UpdateBuildTriggerRequest = None,
        *,
        project_id: str = None,
        trigger_id: str = None,
        trigger: cloudbuild.BuildTrigger = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloudbuild.BuildTrigger:
        r"""Updates a ``BuildTrigger`` by its project ID and trigger ID.

        This API is experimental.

        Args:
            request (:class:`google.cloud.devtools.cloudbuild_v1.types.UpdateBuildTriggerRequest`):
                The request object. Request to update an existing
                `BuildTrigger`.
            project_id (:class:`str`):
                Required. ID of the project that owns
                the trigger.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            trigger_id (:class:`str`):
                Required. ID of the ``BuildTrigger`` to update.
                This corresponds to the ``trigger_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            trigger (:class:`google.cloud.devtools.cloudbuild_v1.types.BuildTrigger`):
                Required. ``BuildTrigger`` to update.
                This corresponds to the ``trigger`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.devtools.cloudbuild_v1.types.BuildTrigger:
                Configuration for an automated build
                in response to source repository
                changes.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, trigger_id, trigger])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudbuild.UpdateBuildTriggerRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if project_id is not None:
            request.project_id = project_id
        if trigger_id is not None:
            request.trigger_id = trigger_id
        if trigger is not None:
            request.trigger = trigger

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_build_trigger,
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def run_build_trigger(
        self,
        request: cloudbuild.RunBuildTriggerRequest = None,
        *,
        project_id: str = None,
        trigger_id: str = None,
        source: cloudbuild.RepoSource = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Runs a ``BuildTrigger`` at a particular source revision.

        Args:
            request (:class:`google.cloud.devtools.cloudbuild_v1.types.RunBuildTriggerRequest`):
                The request object. Specifies a build trigger to run and
                the source to use.
            project_id (:class:`str`):
                Required. ID of the project.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            trigger_id (:class:`str`):
                Required. ID of the trigger.
                This corresponds to the ``trigger_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            source (:class:`google.cloud.devtools.cloudbuild_v1.types.RepoSource`):
                Source to build against this trigger.
                This corresponds to the ``source`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.devtools.cloudbuild_v1.types.Build` A
                build resource in the Cloud Build API.

                   At a high level, a Build describes where to find
                   source code, how to build it (for example, the
                   builder image to run on the source), and where to
                   store the built artifacts.

                   Fields can include the following variables, which
                   will be expanded when the build is created:

                   -  $PROJECT_ID: the project ID of the build.
                   -  $PROJECT_NUMBER: the project number of the build.
                   -  $BUILD_ID: the autogenerated ID of the build.
                   -  $REPO_NAME: the source repository name specified
                      by RepoSource.
                   -  $BRANCH_NAME: the branch name specified by
                      RepoSource.
                   -  $TAG_NAME: the tag name specified by RepoSource.
                   -  $REVISION_ID or $COMMIT_SHA: the commit SHA
                      specified by RepoSource or resolved from the
                      specified branch or tag.
                   -  $SHORT_SHA: first 7 characters of $REVISION_ID or
                      $COMMIT_SHA.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, trigger_id, source])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudbuild.RunBuildTriggerRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if project_id is not None:
            request.project_id = project_id
        if trigger_id is not None:
            request.trigger_id = trigger_id
        if source is not None:
            request.source = source

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.run_build_trigger,
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            cloudbuild.Build,
            metadata_type=cloudbuild.BuildOperationMetadata,
        )

        # Done; return the response.
        return response

    async def receive_trigger_webhook(
        self,
        request: cloudbuild.ReceiveTriggerWebhookRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloudbuild.ReceiveTriggerWebhookResponse:
        r"""ReceiveTriggerWebhook [Experimental] is called when the API
        receives a webhook request targeted at a specific trigger.

        Args:
            request (:class:`google.cloud.devtools.cloudbuild_v1.types.ReceiveTriggerWebhookRequest`):
                The request object. ReceiveTriggerWebhookRequest
                [Experimental] is the request object accepted by the
                ReceiveTriggerWebhook method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.devtools.cloudbuild_v1.types.ReceiveTriggerWebhookResponse:
                ReceiveTriggerWebhookResponse [Experimental] is the response object for the
                   ReceiveTriggerWebhook method.

        """
        # Create or coerce a protobuf request object.
        request = cloudbuild.ReceiveTriggerWebhookRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.receive_trigger_webhook,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def create_worker_pool(
        self,
        request: cloudbuild.CreateWorkerPoolRequest = None,
        *,
        parent: str = None,
        worker_pool: cloudbuild.WorkerPool = None,
        worker_pool_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a ``WorkerPool``.

        Args:
            request (:class:`google.cloud.devtools.cloudbuild_v1.types.CreateWorkerPoolRequest`):
                The request object. Request to create a new
                `WorkerPool`.
            parent (:class:`str`):
                Required. The parent resource where this worker pool
                will be created. Format:
                ``projects/{project}/locations/{location}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            worker_pool (:class:`google.cloud.devtools.cloudbuild_v1.types.WorkerPool`):
                Required. ``WorkerPool`` resource to create.
                This corresponds to the ``worker_pool`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            worker_pool_id (:class:`str`):
                Required. Immutable. The ID to use for the
                ``WorkerPool``, which will become the final component of
                the resource name.

                This value should be 1-63 characters, and valid
                characters are /[a-z][0-9]-/.

                This corresponds to the ``worker_pool_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.devtools.cloudbuild_v1.types.WorkerPool`
                Configuration for a WorkerPool.

                   Cloud Build owns and maintains a pool of workers for
                   general use and have no access to a project's private
                   network. By default, builds submitted to Cloud Build
                   will use a worker from this pool.

                   If your build needs access to resources on a private
                   network, create and use a WorkerPool to run your
                   builds. Private WorkerPools give your builds access
                   to any single VPC network that you administer,
                   including any on-prem resources connected to that VPC
                   network. For an overview of private pools, see
                   [Private pools
                   overview](\ https://cloud.google.com/build/docs/private-pools/private-pools-overview).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, worker_pool, worker_pool_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudbuild.CreateWorkerPoolRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if worker_pool is not None:
            request.worker_pool = worker_pool
        if worker_pool_id is not None:
            request.worker_pool_id = worker_pool_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_worker_pool,
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            cloudbuild.WorkerPool,
            metadata_type=cloudbuild.CreateWorkerPoolOperationMetadata,
        )

        # Done; return the response.
        return response

    async def get_worker_pool(
        self,
        request: cloudbuild.GetWorkerPoolRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloudbuild.WorkerPool:
        r"""Returns details of a ``WorkerPool``.

        Args:
            request (:class:`google.cloud.devtools.cloudbuild_v1.types.GetWorkerPoolRequest`):
                The request object. Request to get a `WorkerPool` with
                the specified name.
            name (:class:`str`):
                Required. The name of the ``WorkerPool`` to retrieve.
                Format:
                ``projects/{project}/locations/{location}/workerPools/{workerPool}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.devtools.cloudbuild_v1.types.WorkerPool:
                Configuration for a WorkerPool.

                   Cloud Build owns and maintains a pool of workers for
                   general use and have no access to a project's private
                   network. By default, builds submitted to Cloud Build
                   will use a worker from this pool.

                   If your build needs access to resources on a private
                   network, create and use a WorkerPool to run your
                   builds. Private WorkerPools give your builds access
                   to any single VPC network that you administer,
                   including any on-prem resources connected to that VPC
                   network. For an overview of private pools, see
                   [Private pools
                   overview](\ https://cloud.google.com/build/docs/private-pools/private-pools-overview).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudbuild.GetWorkerPoolRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_worker_pool,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_worker_pool(
        self,
        request: cloudbuild.DeleteWorkerPoolRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a ``WorkerPool``.

        Args:
            request (:class:`google.cloud.devtools.cloudbuild_v1.types.DeleteWorkerPoolRequest`):
                The request object. Request to delete a `WorkerPool`.
            name (:class:`str`):
                Required. The name of the ``WorkerPool`` to delete.
                Format:
                ``projects/{project}/locations/{workerPool}/workerPools/{workerPool}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudbuild.DeleteWorkerPoolRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_worker_pool,
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=cloudbuild.DeleteWorkerPoolOperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_worker_pool(
        self,
        request: cloudbuild.UpdateWorkerPoolRequest = None,
        *,
        worker_pool: cloudbuild.WorkerPool = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates a ``WorkerPool``.

        Args:
            request (:class:`google.cloud.devtools.cloudbuild_v1.types.UpdateWorkerPoolRequest`):
                The request object. Request to update a `WorkerPool`.
            worker_pool (:class:`google.cloud.devtools.cloudbuild_v1.types.WorkerPool`):
                Required. The ``WorkerPool`` to update.

                The ``name`` field is used to identify the
                ``WorkerPool`` to update. Format:
                ``projects/{project}/locations/{location}/workerPools/{workerPool}``.

                This corresponds to the ``worker_pool`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                A mask specifying which fields in ``worker_pool`` to
                update.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.devtools.cloudbuild_v1.types.WorkerPool`
                Configuration for a WorkerPool.

                   Cloud Build owns and maintains a pool of workers for
                   general use and have no access to a project's private
                   network. By default, builds submitted to Cloud Build
                   will use a worker from this pool.

                   If your build needs access to resources on a private
                   network, create and use a WorkerPool to run your
                   builds. Private WorkerPools give your builds access
                   to any single VPC network that you administer,
                   including any on-prem resources connected to that VPC
                   network. For an overview of private pools, see
                   [Private pools
                   overview](\ https://cloud.google.com/build/docs/private-pools/private-pools-overview).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([worker_pool, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudbuild.UpdateWorkerPoolRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if worker_pool is not None:
            request.worker_pool = worker_pool
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_worker_pool,
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("worker_pool.name", request.worker_pool.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            cloudbuild.WorkerPool,
            metadata_type=cloudbuild.UpdateWorkerPoolOperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_worker_pools(
        self,
        request: cloudbuild.ListWorkerPoolsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListWorkerPoolsAsyncPager:
        r"""Lists ``WorkerPool``\ s.

        Args:
            request (:class:`google.cloud.devtools.cloudbuild_v1.types.ListWorkerPoolsRequest`):
                The request object. Request to list `WorkerPool`\s.
            parent (:class:`str`):
                Required. The parent of the collection of
                ``WorkerPools``. Format:
                ``projects/{project}/locations/{location}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.devtools.cloudbuild_v1.services.cloud_build.pagers.ListWorkerPoolsAsyncPager:
                Response containing existing WorkerPools.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudbuild.ListWorkerPoolsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_worker_pools,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListWorkerPoolsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-devtools-cloudbuild",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("CloudBuildAsyncClient",)
