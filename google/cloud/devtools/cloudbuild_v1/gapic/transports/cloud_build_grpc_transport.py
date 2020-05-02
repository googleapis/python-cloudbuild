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


import google.api_core.grpc_helpers
import google.api_core.operations_v1

from google.cloud.devtools.cloudbuild_v1.proto import cloudbuild_pb2_grpc


class CloudBuildGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.devtools.cloudbuild.v1 CloudBuild API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self, channel=None, credentials=None, address="cloudbuild.googleapis.com:443"
    ):
        """Instantiate the transport class.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            address (str): The address where the service is hosted.
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:
            raise ValueError(
                "The `channel` and `credentials` arguments are mutually " "exclusive."
            )

        # Create the channel.
        if channel is None:
            channel = self.create_channel(
                address=address,
                credentials=credentials,
                options={
                    "grpc.max_send_message_length": -1,
                    "grpc.max_receive_message_length": -1,
                }.items(),
            )

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {"cloud_build_stub": cloudbuild_pb2_grpc.CloudBuildStub(channel)}

        # Because this API includes a method that returns a
        # long-running operation (proto: google.longrunning.Operation),
        # instantiate an LRO client.
        self._operations_client = google.api_core.operations_v1.OperationsClient(
            channel
        )

    @classmethod
    def create_channel(
        cls, address="cloudbuild.googleapis.com:443", credentials=None, **kwargs
    ):
        """Create and return a gRPC channel object.

        Args:
            address (str): The host for the channel to use.
            credentials (~.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            kwargs (dict): Keyword arguments, which are passed to the
                channel creation.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return google.api_core.grpc_helpers.create_channel(
            address, credentials=credentials, scopes=cls._OAUTH_SCOPES, **kwargs
        )

    @property
    def channel(self):
        """The gRPC channel used by the transport.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return self._channel

    @property
    def list_builds(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.list_builds`.

        Lists previously requested builds.

        Previously requested builds may still be in-progress, or may have finished
        successfully or unsuccessfully.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].ListBuilds

    @property
    def delete_build_trigger(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.delete_build_trigger`.

        ``WorkerPool`` is running.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].DeleteBuildTrigger

    @property
    def create_build(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.create_build`.

        Output only. Stores timing information for phases of the build.
        Valid keys are:

        -  BUILD: time to execute all build steps
        -  PUSH: time to push all specified images.
        -  FETCHSOURCE: time to fetch source.

        If the build does not specify source or images, these keys will not be
        included.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].CreateBuild

    @property
    def get_build(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.get_build`.

        Status of the ``WorkerPool`` is unknown.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].GetBuild

    @property
    def cancel_build(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.cancel_build`.

        Cancels a build in progress.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].CancelBuild

    @property
    def retry_build(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.retry_build`.

        Denotes a field as required. This indicates that the field **must**
        be provided as part of the request, and failure to do so will cause an
        error (usually ``INVALID_ARGUMENT``).

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].RetryBuild

    @property
    def create_build_trigger(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.create_build_trigger`.

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

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].CreateBuildTrigger

    @property
    def get_build_trigger(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.get_build_trigger`.

        ``WorkerPool`` is being created.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].GetBuildTrigger

    @property
    def list_build_triggers(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.list_build_triggers`.

        For extensions, this is the name of the type being extended. It is
        resolved in the same manner as type_name.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].ListBuildTriggers

    @property
    def update_build_trigger(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.update_build_trigger`.

        ``WorkerPool`` is being deleted: cancelling builds and draining
        workers.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].UpdateBuildTrigger

    @property
    def run_build_trigger(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.run_build_trigger`.

        The resource has one pattern, but the API owner expects to add more
        later. (This is the inverse of ORIGINALLY_SINGLE_PATTERN, and prevents
        that from being necessary once there are multiple patterns.)

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].RunBuildTrigger

    @property
    def create_worker_pool(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.create_worker_pool`.

        ``WorkerPool`` is deleted.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].CreateWorkerPool

    @property
    def get_worker_pool(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.get_worker_pool`.

        If set, gives the index of a oneof in the containing type's
        oneof_decl list. This field is a member of that oneof.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].GetWorkerPool

    @property
    def delete_worker_pool(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.delete_worker_pool`.

        User-defined name of the ``WorkerPool``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].DeleteWorkerPool

    @property
    def update_worker_pool(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.update_worker_pool`.

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

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].UpdateWorkerPool

    @property
    def list_worker_pools(self):
        """Return the gRPC stub for :meth:`CloudBuildClient.list_worker_pools`.

        A list of arguments that will be presented to the step when it is
        started.

        If the image used to run the step's container has an entrypoint, the
        ``args`` are used as arguments to that entrypoint. If the image does not
        define an entrypoint, the first element in args is used as the
        entrypoint, and the remainder will be used as arguments.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_build_stub"].ListWorkerPools
