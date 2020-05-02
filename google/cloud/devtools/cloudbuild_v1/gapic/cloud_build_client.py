# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Accesses the google.devtools.cloudbuild.v1 CloudBuild API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.operation
import google.api_core.operations_v1
import google.api_core.page_iterator
import grpc

from google.cloud.devtools.cloudbuild_v1.gapic import cloud_build_client_config
from google.cloud.devtools.cloudbuild_v1.gapic import enums
from google.cloud.devtools.cloudbuild_v1.gapic.transports import (
    cloud_build_grpc_transport,
)
from google.cloud.devtools.cloudbuild_v1.proto import cloudbuild_pb2
from google.cloud.devtools.cloudbuild_v1.proto import cloudbuild_pb2_grpc
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-build").version


class CloudBuildClient(object):
    """``WorkerPool`` status"""

    SERVICE_ADDRESS = "cloudbuild.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.devtools.cloudbuild.v1.CloudBuild"

    @classmethod
    def from_service_account_file(cls, filename, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            CloudBuildClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
        client_options=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.CloudBuildGrpcTransport,
                    Callable[[~.Credentials, type], ~.CloudBuildGrpcTransport]): A transport
                instance, responsible for actually making the API calls.
                The default transport uses the gRPC protocol.
                This argument may also be a callable which returns a
                transport instance. Callables will be sent the credentials
                as the first argument and the default transport class as
                the second argument.
            channel (grpc.Channel): DEPRECATED. A ``Channel`` instance
                through which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception.
            client_config (dict): DEPRECATED. A dictionary of call options for
                each method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            client_options (Union[dict, google.api_core.client_options.ClientOptions]):
                Client options used to set user options on the client. API Endpoint
                should be set through client_options.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = cloud_build_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        api_endpoint = self.SERVICE_ADDRESS
        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(
                    client_options
                )
            if client_options.api_endpoint:
                api_endpoint = client_options.api_endpoint

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=cloud_build_grpc_transport.CloudBuildGrpcTransport,
                    address=api_endpoint,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = cloud_build_grpc_transport.CloudBuildGrpcTransport(
                address=api_endpoint, channel=channel, credentials=credentials
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config["interfaces"][self._INTERFACE_NAME]
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def list_builds(
        self,
        project_id,
        page_size=None,
        filter_=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists previously requested builds.

        Previously requested builds may still be in-progress, or may have finished
        successfully or unsuccessfully.

        Example:
            >>> from google.cloud.devtools import cloudbuild_v1
            >>>
            >>> client = cloudbuild_v1.CloudBuildClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_builds(project_id):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_builds(project_id).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            project_id (str): Required. ID of the project.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            filter_ (str): The raw filter text to constrain the results.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.devtools.cloudbuild_v1.types.Build` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_builds" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_builds"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_builds,
                default_retry=self._method_configs["ListBuilds"].retry,
                default_timeout=self._method_configs["ListBuilds"].timeout,
                client_info=self._client_info,
            )

        request = cloudbuild_pb2.ListBuildsRequest(
            project_id=project_id, page_size=page_size, filter=filter_
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("project_id", project_id)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_builds"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="builds",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def delete_build_trigger(
        self,
        project_id,
        trigger_id,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        ``WorkerPool`` is running.

        Example:
            >>> from google.cloud.devtools import cloudbuild_v1
            >>>
            >>> client = cloudbuild_v1.CloudBuildClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # TODO: Initialize `trigger_id`:
            >>> trigger_id = ''
            >>>
            >>> client.delete_build_trigger(project_id, trigger_id)

        Args:
            project_id (str): Required. ID of the project that owns the trigger.
            trigger_id (str): Request to create a new ``WorkerPool``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_build_trigger" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_build_trigger"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_build_trigger,
                default_retry=self._method_configs["DeleteBuildTrigger"].retry,
                default_timeout=self._method_configs["DeleteBuildTrigger"].timeout,
                client_info=self._client_info,
            )

        request = cloudbuild_pb2.DeleteBuildTriggerRequest(
            project_id=project_id, trigger_id=trigger_id
        )
        self._inner_api_calls["delete_build_trigger"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_build(
        self,
        project_id,
        build,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Output only. Stores timing information for phases of the build.
        Valid keys are:

        -  BUILD: time to execute all build steps
        -  PUSH: time to push all specified images.
        -  FETCHSOURCE: time to fetch source.

        If the build does not specify source or images, these keys will not be
        included.

        Example:
            >>> from google.cloud.devtools import cloudbuild_v1
            >>>
            >>> client = cloudbuild_v1.CloudBuildClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # TODO: Initialize `build`:
            >>> build = {}
            >>>
            >>> response = client.create_build(project_id, build)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            project_id (str): Required. ID of the project.
            build (Union[dict, ~google.cloud.devtools.cloudbuild_v1.types.Build]): Required. Build resource to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.devtools.cloudbuild_v1.types.Build`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.devtools.cloudbuild_v1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_build" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_build"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_build,
                default_retry=self._method_configs["CreateBuild"].retry,
                default_timeout=self._method_configs["CreateBuild"].timeout,
                client_info=self._client_info,
            )

        request = cloudbuild_pb2.CreateBuildRequest(project_id=project_id, build=build)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("project_id", project_id)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        operation = self._inner_api_calls["create_build"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            cloudbuild_pb2.Build,
            metadata_type=cloudbuild_pb2.BuildOperationMetadata,
        )

    def get_build(
        self,
        project_id,
        id_,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Status of the ``WorkerPool`` is unknown.

        Example:
            >>> from google.cloud.devtools import cloudbuild_v1
            >>>
            >>> client = cloudbuild_v1.CloudBuildClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # TODO: Initialize `id_`:
            >>> id_ = ''
            >>>
            >>> response = client.get_build(project_id, id_)

        Args:
            project_id (str): Required. ID of the project.
            id_ (str): Required. ID of the build.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.devtools.cloudbuild_v1.types.Build` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_build" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_build"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_build,
                default_retry=self._method_configs["GetBuild"].retry,
                default_timeout=self._method_configs["GetBuild"].timeout,
                client_info=self._client_info,
            )

        request = cloudbuild_pb2.GetBuildRequest(project_id=project_id, id=id_)
        return self._inner_api_calls["get_build"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def cancel_build(
        self,
        project_id,
        id_,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Cancels a build in progress.

        Example:
            >>> from google.cloud.devtools import cloudbuild_v1
            >>>
            >>> client = cloudbuild_v1.CloudBuildClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # TODO: Initialize `id_`:
            >>> id_ = ''
            >>>
            >>> response = client.cancel_build(project_id, id_)

        Args:
            project_id (str): Required. ID of the project.
            id_ (str): Required. ID of the build.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.devtools.cloudbuild_v1.types.Build` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "cancel_build" not in self._inner_api_calls:
            self._inner_api_calls[
                "cancel_build"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.cancel_build,
                default_retry=self._method_configs["CancelBuild"].retry,
                default_timeout=self._method_configs["CancelBuild"].timeout,
                client_info=self._client_info,
            )

        request = cloudbuild_pb2.CancelBuildRequest(project_id=project_id, id=id_)
        return self._inner_api_calls["cancel_build"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def retry_build(
        self,
        project_id,
        id_,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Denotes a field as required. This indicates that the field **must**
        be provided as part of the request, and failure to do so will cause an
        error (usually ``INVALID_ARGUMENT``).

        Example:
            >>> from google.cloud.devtools import cloudbuild_v1
            >>>
            >>> client = cloudbuild_v1.CloudBuildClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # TODO: Initialize `id_`:
            >>> id_ = ''
            >>>
            >>> response = client.retry_build(project_id, id_)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            project_id (str): Required. ID of the project.
            id_ (str): Required. Build ID of the original build.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.devtools.cloudbuild_v1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "retry_build" not in self._inner_api_calls:
            self._inner_api_calls[
                "retry_build"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.retry_build,
                default_retry=self._method_configs["RetryBuild"].retry,
                default_timeout=self._method_configs["RetryBuild"].timeout,
                client_info=self._client_info,
            )

        request = cloudbuild_pb2.RetryBuildRequest(project_id=project_id, id=id_)
        operation = self._inner_api_calls["retry_build"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            cloudbuild_pb2.Build,
            metadata_type=cloudbuild_pb2.BuildOperationMetadata,
        )

    def create_build_trigger(
        self,
        project_id,
        trigger,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        A Timestamp represents a point in time independent of any time zone
        or local calendar, encoded as a count of seconds and fractions of
        seconds at nanosecond resolution. The count is relative to an epoch at
        UTC midnight on January 1, 1970, in the proleptic Gregorian calendar
        which extends the Gregorian calendar backwards to year one.

        All minutes are 60 seconds long. Leap seconds are "smeared" so that no
        leap second table is needed for interpretation, using a `24-hour linear
        smear <https://developers.google.com/time/smear>`__.

        The range is from 0001-01-01T00:00:00Z to
        9999-12-31T23:59:59.999999999Z. By restricting to that range, we ensure
        that we can convert to and from `RFC
        3339 <https://www.ietf.org/rfc/rfc3339.txt>`__ date strings.

        # Examples

        Example 1: Compute Timestamp from POSIX ``time()``.

        ::

            Timestamp timestamp;
            timestamp.set_seconds(time(NULL));
            timestamp.set_nanos(0);

        Example 2: Compute Timestamp from POSIX ``gettimeofday()``.

        ::

            struct timeval tv;
            gettimeofday(&tv, NULL);

            Timestamp timestamp;
            timestamp.set_seconds(tv.tv_sec);
            timestamp.set_nanos(tv.tv_usec * 1000);

        Example 3: Compute Timestamp from Win32 ``GetSystemTimeAsFileTime()``.

        ::

            FILETIME ft;
            GetSystemTimeAsFileTime(&ft);
            UINT64 ticks = (((UINT64)ft.dwHighDateTime) << 32) | ft.dwLowDateTime;

            // A Windows tick is 100 nanoseconds. Windows epoch 1601-01-01T00:00:00Z
            // is 11644473600 seconds before Unix epoch 1970-01-01T00:00:00Z.
            Timestamp timestamp;
            timestamp.set_seconds((INT64) ((ticks / 10000000) - 11644473600LL));
            timestamp.set_nanos((INT32) ((ticks % 10000000) * 100));

        Example 4: Compute Timestamp from Java ``System.currentTimeMillis()``.

        ::

            long millis = System.currentTimeMillis();

            Timestamp timestamp = Timestamp.newBuilder().setSeconds(millis / 1000)
                .setNanos((int) ((millis % 1000) * 1000000)).build();

        Example 5: Compute Timestamp from current time in Python.

        ::

            timestamp = Timestamp()
            timestamp.GetCurrentTime()

        # JSON Mapping

        In JSON format, the Timestamp type is encoded as a string in the `RFC
        3339 <https://www.ietf.org/rfc/rfc3339.txt>`__ format. That is, the
        format is "{year}-{month}-{day}T{hour}:{min}:{sec}[.{frac_sec}]Z" where
        {year} is always expressed using four digits while {month}, {day},
        {hour}, {min}, and {sec} are zero-padded to two digits each. The
        fractional seconds, which can go up to 9 digits (i.e. up to 1 nanosecond
        resolution), are optional. The "Z" suffix indicates the timezone
        ("UTC"); the timezone is required. A proto3 JSON serializer should
        always use UTC (as indicated by "Z") when printing the Timestamp type
        and a proto3 JSON parser should be able to accept both UTC and other
        timezones (as indicated by an offset).

        For example, "2017-01-15T01:30:15.01Z" encodes 15.01 seconds past 01:30
        UTC on January 15, 2017.

        In JavaScript, one can convert a Date object to this format using the
        standard
        `toISOString() <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/toISOString>`__
        method. In Python, a standard ``datetime.datetime`` object can be
        converted to this format using
        ```strftime`` <https://docs.python.org/2/library/time.html#time.strftime>`__
        with the time format spec '%Y-%m-%dT%H:%M:%S.%fZ'. Likewise, in Java,
        one can use the Joda Time's
        ```ISODateTimeFormat.dateTime()`` <http://www.joda.org/joda-time/apidocs/org/joda/time/format/ISODateTimeFormat.html#dateTime%2D%2D>`__
        to obtain a formatter capable of generating timestamps in this format.

        Example:
            >>> from google.cloud.devtools import cloudbuild_v1
            >>>
            >>> client = cloudbuild_v1.CloudBuildClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # TODO: Initialize `trigger`:
            >>> trigger = {}
            >>>
            >>> response = client.create_build_trigger(project_id, trigger)

        Args:
            project_id (str): Required. ID of the project for which to configure automatic builds.
            trigger (Union[dict, ~google.cloud.devtools.cloudbuild_v1.types.BuildTrigger]): Build was enqueued for longer than the value of ``queue_ttl``.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.devtools.cloudbuild_v1.types.BuildTrigger`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.devtools.cloudbuild_v1.types.BuildTrigger` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_build_trigger" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_build_trigger"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_build_trigger,
                default_retry=self._method_configs["CreateBuildTrigger"].retry,
                default_timeout=self._method_configs["CreateBuildTrigger"].timeout,
                client_info=self._client_info,
            )

        request = cloudbuild_pb2.CreateBuildTriggerRequest(
            project_id=project_id, trigger=trigger
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("project_id", project_id)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["create_build_trigger"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_build_trigger(
        self,
        project_id,
        trigger_id,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        ``WorkerPool`` is being created.

        Example:
            >>> from google.cloud.devtools import cloudbuild_v1
            >>>
            >>> client = cloudbuild_v1.CloudBuildClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # TODO: Initialize `trigger_id`:
            >>> trigger_id = ''
            >>>
            >>> response = client.get_build_trigger(project_id, trigger_id)

        Args:
            project_id (str): Required. ID of the project that owns the trigger.
            trigger_id (str): Request to list existing ``BuildTriggers``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.devtools.cloudbuild_v1.types.BuildTrigger` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_build_trigger" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_build_trigger"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_build_trigger,
                default_retry=self._method_configs["GetBuildTrigger"].retry,
                default_timeout=self._method_configs["GetBuildTrigger"].timeout,
                client_info=self._client_info,
            )

        request = cloudbuild_pb2.GetBuildTriggerRequest(
            project_id=project_id, trigger_id=trigger_id
        )
        return self._inner_api_calls["get_build_trigger"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_build_triggers(
        self,
        project_id,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        For extensions, this is the name of the type being extended. It is
        resolved in the same manner as type_name.

        Example:
            >>> from google.cloud.devtools import cloudbuild_v1
            >>>
            >>> client = cloudbuild_v1.CloudBuildClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_build_triggers(project_id):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_build_triggers(project_id).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            project_id (str): Required. ID of the project for which to list BuildTriggers.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.devtools.cloudbuild_v1.types.BuildTrigger` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_build_triggers" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_build_triggers"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_build_triggers,
                default_retry=self._method_configs["ListBuildTriggers"].retry,
                default_timeout=self._method_configs["ListBuildTriggers"].timeout,
                client_info=self._client_info,
            )

        request = cloudbuild_pb2.ListBuildTriggersRequest(
            project_id=project_id, page_size=page_size
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("project_id", project_id)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_build_triggers"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="triggers",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def update_build_trigger(
        self,
        project_id,
        trigger_id,
        trigger,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        ``WorkerPool`` is being deleted: cancelling builds and draining
        workers.

        Example:
            >>> from google.cloud.devtools import cloudbuild_v1
            >>>
            >>> client = cloudbuild_v1.CloudBuildClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # TODO: Initialize `trigger_id`:
            >>> trigger_id = ''
            >>>
            >>> # TODO: Initialize `trigger`:
            >>> trigger = {}
            >>>
            >>> response = client.update_build_trigger(project_id, trigger_id, trigger)

        Args:
            project_id (str): Required. ID of the project that owns the trigger.
            trigger_id (str): A Location identifies a piece of source code in a .proto file which
                corresponds to a particular definition. This information is intended to
                be useful to IDEs, code indexers, documentation generators, and similar
                tools.

                For example, say we have a file like: message Foo { optional string foo
                = 1; } Let's look at just the field definition: optional string foo = 1;
                ^ ^^ ^^ ^ ^^^ a bc de f ghi We have the following locations: span path
                represents [a,i) [ 4, 0, 2, 0 ] The whole field definition. [a,b) [ 4,
                0, 2, 0, 4 ] The label (optional). [c,d) [ 4, 0, 2, 0, 5 ] The type
                (string). [e,f) [ 4, 0, 2, 0, 1 ] The name (foo). [g,h) [ 4, 0, 2, 0, 3
                ] The number (1).

                Notes:

                -  A location may refer to a repeated field itself (i.e. not to any
                   particular index within it). This is used whenever a set of elements
                   are logically enclosed in a single code segment. For example, an
                   entire extend block (possibly containing multiple extension
                   definitions) will have an outer location whose path refers to the
                   "extensions" repeated field without an index.
                -  Multiple locations may have the same path. This happens when a single
                   logical declaration is spread out across multiple places. The most
                   obvious example is the "extend" block again -- there may be multiple
                   extend blocks in the same scope, each of which will have the same
                   path.
                -  A location's span is not always a subset of its parent's span. For
                   example, the "extendee" of an extension declaration appears at the
                   beginning of the "extend" block and is shared by all extensions
                   within the block.
                -  Just because a location's span is a subset of some other location's
                   span does not mean that it is a descendant. For example, a "group"
                   defines both a type and a field in a single declaration. Thus, the
                   locations corresponding to the type and field and their components
                   will overlap.
                -  Code which tries to interpret locations should probably be designed
                   to ignore those that it doesn't understand, as more types of
                   locations could be recorded in the future.
            trigger (Union[dict, ~google.cloud.devtools.cloudbuild_v1.types.BuildTrigger]): Response containing existing ``BuildTriggers``.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.devtools.cloudbuild_v1.types.BuildTrigger`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.devtools.cloudbuild_v1.types.BuildTrigger` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_build_trigger" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_build_trigger"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_build_trigger,
                default_retry=self._method_configs["UpdateBuildTrigger"].retry,
                default_timeout=self._method_configs["UpdateBuildTrigger"].timeout,
                client_info=self._client_info,
            )

        request = cloudbuild_pb2.UpdateBuildTriggerRequest(
            project_id=project_id, trigger_id=trigger_id, trigger=trigger
        )
        return self._inner_api_calls["update_build_trigger"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def run_build_trigger(
        self,
        project_id,
        trigger_id,
        source,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        The resource has one pattern, but the API owner expects to add more
        later. (This is the inverse of ORIGINALLY_SINGLE_PATTERN, and prevents
        that from being necessary once there are multiple patterns.)

        Example:
            >>> from google.cloud.devtools import cloudbuild_v1
            >>>
            >>> client = cloudbuild_v1.CloudBuildClient()
            >>>
            >>> # TODO: Initialize `project_id`:
            >>> project_id = ''
            >>>
            >>> # TODO: Initialize `trigger_id`:
            >>> trigger_id = ''
            >>>
            >>> # TODO: Initialize `source`:
            >>> source = {}
            >>>
            >>> response = client.run_build_trigger(project_id, trigger_id, source)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            project_id (str): Required. ID of the project.
            trigger_id (str): Required. ID of the trigger.
            source (Union[dict, ~google.cloud.devtools.cloudbuild_v1.types.RepoSource]): Required. Source to build against this trigger.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.devtools.cloudbuild_v1.types.RepoSource`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.devtools.cloudbuild_v1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "run_build_trigger" not in self._inner_api_calls:
            self._inner_api_calls[
                "run_build_trigger"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.run_build_trigger,
                default_retry=self._method_configs["RunBuildTrigger"].retry,
                default_timeout=self._method_configs["RunBuildTrigger"].timeout,
                client_info=self._client_info,
            )

        request = cloudbuild_pb2.RunBuildTriggerRequest(
            project_id=project_id, trigger_id=trigger_id, source=source
        )
        operation = self._inner_api_calls["run_build_trigger"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            cloudbuild_pb2.Build,
            metadata_type=cloudbuild_pb2.BuildOperationMetadata,
        )

    def create_worker_pool(
        self,
        parent=None,
        worker_pool=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        ``WorkerPool`` is deleted.

        Example:
            >>> from google.cloud.devtools import cloudbuild_v1
            >>>
            >>> client = cloudbuild_v1.CloudBuildClient()
            >>>
            >>> response = client.create_worker_pool()

        Args:
            parent (str): ID of the parent project.
            worker_pool (Union[dict, ~google.cloud.devtools.cloudbuild_v1.types.WorkerPool]): ``WorkerPools`` for the project.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.devtools.cloudbuild_v1.types.WorkerPool`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.devtools.cloudbuild_v1.types.WorkerPool` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_worker_pool" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_worker_pool"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_worker_pool,
                default_retry=self._method_configs["CreateWorkerPool"].retry,
                default_timeout=self._method_configs["CreateWorkerPool"].timeout,
                client_info=self._client_info,
            )

        request = cloudbuild_pb2.CreateWorkerPoolRequest(
            parent=parent, worker_pool=worker_pool
        )
        return self._inner_api_calls["create_worker_pool"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_worker_pool(
        self,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        If set, gives the index of a oneof in the containing type's
        oneof_decl list. This field is a member of that oneof.

        Example:
            >>> from google.cloud.devtools import cloudbuild_v1
            >>>
            >>> client = cloudbuild_v1.CloudBuildClient()
            >>>
            >>> response = client.get_worker_pool()

        Args:
            name (str): The field will contain name of the resource requested, for example:
                "projects/project-1/workerPools/workerpool-name"
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.devtools.cloudbuild_v1.types.WorkerPool` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_worker_pool" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_worker_pool"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_worker_pool,
                default_retry=self._method_configs["GetWorkerPool"].retry,
                default_timeout=self._method_configs["GetWorkerPool"].timeout,
                client_info=self._client_info,
            )

        request = cloudbuild_pb2.GetWorkerPoolRequest(name=name)
        return self._inner_api_calls["get_worker_pool"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_worker_pool(
        self,
        name=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        User-defined name of the ``WorkerPool``.

        Example:
            >>> from google.cloud.devtools import cloudbuild_v1
            >>>
            >>> client = cloudbuild_v1.CloudBuildClient()
            >>>
            >>> client.delete_worker_pool()

        Args:
            name (str): The field will contain name of the resource requested, for example:
                "projects/project-1/workerPools/workerpool-name"
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_worker_pool" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_worker_pool"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_worker_pool,
                default_retry=self._method_configs["DeleteWorkerPool"].retry,
                default_timeout=self._method_configs["DeleteWorkerPool"].timeout,
                client_info=self._client_info,
            )

        request = cloudbuild_pb2.DeleteWorkerPoolRequest(name=name)
        self._inner_api_calls["delete_worker_pool"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_worker_pool(
        self,
        name=None,
        worker_pool=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Required. The name of the container image that will run this
        particular build step.

        If the image is available in the host's Docker daemon's cache, it will
        be run directly. If not, the host will attempt to pull the image first,
        using the builder service account's credentials if necessary.

        The Docker daemon's cache will already have the latest versions of all
        of the officially supported build steps
        (https://github.com/GoogleCloudPlatform/cloud-builders). The Docker
        daemon will also have cached many of the layers for some popular images,
        like "ubuntu", "debian", but they will be refreshed at the time you
        attempt to use them.

        If you built an image in a previous build step, it will be stored in the
        host's Docker daemon's cache and is available to use as the name for a
        later build step.

        Example:
            >>> from google.cloud.devtools import cloudbuild_v1
            >>>
            >>> client = cloudbuild_v1.CloudBuildClient()
            >>>
            >>> response = client.update_worker_pool()

        Args:
            name (str): The field will contain name of the resource requested, for example:
                "projects/project-1/workerPools/workerpool-name"
            worker_pool (Union[dict, ~google.cloud.devtools.cloudbuild_v1.types.WorkerPool]): Returns information about a ``WorkerPool``.

                This API is experimental.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.devtools.cloudbuild_v1.types.WorkerPool`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.devtools.cloudbuild_v1.types.WorkerPool` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_worker_pool" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_worker_pool"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_worker_pool,
                default_retry=self._method_configs["UpdateWorkerPool"].retry,
                default_timeout=self._method_configs["UpdateWorkerPool"].timeout,
                client_info=self._client_info,
            )

        request = cloudbuild_pb2.UpdateWorkerPoolRequest(
            name=name, worker_pool=worker_pool
        )
        return self._inner_api_calls["update_worker_pool"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_worker_pools(
        self,
        parent=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        A list of arguments that will be presented to the step when it is
        started.

        If the image used to run the step's container has an entrypoint, the
        ``args`` are used as arguments to that entrypoint. If the image does not
        define an entrypoint, the first element in args is used as the
        entrypoint, and the remainder will be used as arguments.

        Example:
            >>> from google.cloud.devtools import cloudbuild_v1
            >>>
            >>> client = cloudbuild_v1.CloudBuildClient()
            >>>
            >>> response = client.list_worker_pools()

        Args:
            parent (str): ID of the parent project.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.devtools.cloudbuild_v1.types.ListWorkerPoolsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_worker_pools" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_worker_pools"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_worker_pools,
                default_retry=self._method_configs["ListWorkerPools"].retry,
                default_timeout=self._method_configs["ListWorkerPools"].timeout,
                client_info=self._client_info,
            )

        request = cloudbuild_pb2.ListWorkerPoolsRequest(parent=parent)
        return self._inner_api_calls["list_worker_pools"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
