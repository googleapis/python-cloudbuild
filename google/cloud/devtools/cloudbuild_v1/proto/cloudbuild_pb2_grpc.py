# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.cloud.devtools.cloudbuild_v1.proto import (
    cloudbuild_pb2 as google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2,
)
from google.longrunning import (
    operations_pb2 as google_dot_longrunning_dot_operations__pb2,
)
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class CloudBuildStub(object):
    """Creates and manages builds on Google Cloud Platform.

    The main concept used by this API is a `Build`, which describes the location
    of the source to build, how to build the source, and where to store the
    built artifacts, if any.

    A user can list previously-requested builds or get builds by their ID to
    determine the status of the build.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
          channel: A grpc.Channel.
        """
        self.CreateBuild = channel.unary_unary(
            "/google.devtools.cloudbuild.v1.CloudBuild/CreateBuild",
            request_serializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.CreateBuildRequest.SerializeToString,
            response_deserializer=google_dot_longrunning_dot_operations__pb2.Operation.FromString,
        )
        self.GetBuild = channel.unary_unary(
            "/google.devtools.cloudbuild.v1.CloudBuild/GetBuild",
            request_serializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.GetBuildRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.Build.FromString,
        )
        self.ListBuilds = channel.unary_unary(
            "/google.devtools.cloudbuild.v1.CloudBuild/ListBuilds",
            request_serializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.ListBuildsRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.ListBuildsResponse.FromString,
        )
        self.CancelBuild = channel.unary_unary(
            "/google.devtools.cloudbuild.v1.CloudBuild/CancelBuild",
            request_serializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.CancelBuildRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.Build.FromString,
        )
        self.RetryBuild = channel.unary_unary(
            "/google.devtools.cloudbuild.v1.CloudBuild/RetryBuild",
            request_serializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.RetryBuildRequest.SerializeToString,
            response_deserializer=google_dot_longrunning_dot_operations__pb2.Operation.FromString,
        )
        self.CreateBuildTrigger = channel.unary_unary(
            "/google.devtools.cloudbuild.v1.CloudBuild/CreateBuildTrigger",
            request_serializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.CreateBuildTriggerRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.BuildTrigger.FromString,
        )
        self.GetBuildTrigger = channel.unary_unary(
            "/google.devtools.cloudbuild.v1.CloudBuild/GetBuildTrigger",
            request_serializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.GetBuildTriggerRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.BuildTrigger.FromString,
        )
        self.ListBuildTriggers = channel.unary_unary(
            "/google.devtools.cloudbuild.v1.CloudBuild/ListBuildTriggers",
            request_serializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.ListBuildTriggersRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.ListBuildTriggersResponse.FromString,
        )
        self.DeleteBuildTrigger = channel.unary_unary(
            "/google.devtools.cloudbuild.v1.CloudBuild/DeleteBuildTrigger",
            request_serializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.DeleteBuildTriggerRequest.SerializeToString,
            response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
        self.UpdateBuildTrigger = channel.unary_unary(
            "/google.devtools.cloudbuild.v1.CloudBuild/UpdateBuildTrigger",
            request_serializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.UpdateBuildTriggerRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.BuildTrigger.FromString,
        )
        self.RunBuildTrigger = channel.unary_unary(
            "/google.devtools.cloudbuild.v1.CloudBuild/RunBuildTrigger",
            request_serializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.RunBuildTriggerRequest.SerializeToString,
            response_deserializer=google_dot_longrunning_dot_operations__pb2.Operation.FromString,
        )
        self.CreateWorkerPool = channel.unary_unary(
            "/google.devtools.cloudbuild.v1.CloudBuild/CreateWorkerPool",
            request_serializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.CreateWorkerPoolRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.WorkerPool.FromString,
        )
        self.GetWorkerPool = channel.unary_unary(
            "/google.devtools.cloudbuild.v1.CloudBuild/GetWorkerPool",
            request_serializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.GetWorkerPoolRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.WorkerPool.FromString,
        )
        self.DeleteWorkerPool = channel.unary_unary(
            "/google.devtools.cloudbuild.v1.CloudBuild/DeleteWorkerPool",
            request_serializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.DeleteWorkerPoolRequest.SerializeToString,
            response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
        self.UpdateWorkerPool = channel.unary_unary(
            "/google.devtools.cloudbuild.v1.CloudBuild/UpdateWorkerPool",
            request_serializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.UpdateWorkerPoolRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.WorkerPool.FromString,
        )
        self.ListWorkerPools = channel.unary_unary(
            "/google.devtools.cloudbuild.v1.CloudBuild/ListWorkerPools",
            request_serializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.ListWorkerPoolsRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.ListWorkerPoolsResponse.FromString,
        )


class CloudBuildServicer(object):
    """Creates and manages builds on Google Cloud Platform.

    The main concept used by this API is a `Build`, which describes the location
    of the source to build, how to build the source, and where to store the
    built artifacts, if any.

    A user can list previously-requested builds or get builds by their ID to
    determine the status of the build.
    """

    def CreateBuild(self, request, context):
        """Starts a build with the specified configuration.

        This method returns a long-running `Operation`, which includes the build
        ID. Pass the build ID to `GetBuild` to determine the build status (such as
        `SUCCESS` or `FAILURE`).
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetBuild(self, request, context):
        """Returns information about a previously requested build.

        The `Build` that is returned includes its status (such as `SUCCESS`,
        `FAILURE`, or `WORKING`), and timing information.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def ListBuilds(self, request, context):
        """Lists previously requested builds.

        Previously requested builds may still be in-progress, or may have finished
        successfully or unsuccessfully.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def CancelBuild(self, request, context):
        """Cancels a build in progress."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def RetryBuild(self, request, context):
        """Creates a new build based on the specified build.

        This method creates a new build using the original build request, which may
        or may not result in an identical build.

        For triggered builds:

        * Triggered builds resolve to a precise revision; therefore a retry of a
        triggered build will result in a build that uses the same revision.

        For non-triggered builds that specify `RepoSource`:

        * If the original build built from the tip of a branch, the retried build
        will build from the tip of that branch, which may not be the same revision
        as the original build.
        * If the original build specified a commit sha or revision ID, the retried
        build will use the identical source.

        For builds that specify `StorageSource`:

        * If the original build pulled source from Google Cloud Storage without
        specifying the generation of the object, the new build will use the current
        object, which may be different from the original build source.
        * If the original build pulled source from Cloud Storage and specified the
        generation of the object, the new build will attempt to use the same
        object, which may or may not be available depending on the bucket's
        lifecycle management settings.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def CreateBuildTrigger(self, request, context):
        """Creates a new `BuildTrigger`.

        This API is experimental.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetBuildTrigger(self, request, context):
        """Returns information about a `BuildTrigger`.

        This API is experimental.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def ListBuildTriggers(self, request, context):
        """Lists existing `BuildTrigger`s.

        This API is experimental.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def DeleteBuildTrigger(self, request, context):
        """Deletes a `BuildTrigger` by its project ID and trigger ID.

        This API is experimental.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def UpdateBuildTrigger(self, request, context):
        """Updates a `BuildTrigger` by its project ID and trigger ID.

        This API is experimental.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def RunBuildTrigger(self, request, context):
        """Runs a `BuildTrigger` at a particular source revision."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def CreateWorkerPool(self, request, context):
        """Creates a `WorkerPool` to run the builds, and returns the new worker pool.

        This API is experimental.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetWorkerPool(self, request, context):
        """Returns information about a `WorkerPool`.

        This API is experimental.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def DeleteWorkerPool(self, request, context):
        """Deletes a `WorkerPool` by its project ID and WorkerPool name.

        This API is experimental.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def UpdateWorkerPool(self, request, context):
        """Update a `WorkerPool`.

        This API is experimental.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def ListWorkerPools(self, request, context):
        """List project's `WorkerPool`s.

        This API is experimental.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_CloudBuildServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "CreateBuild": grpc.unary_unary_rpc_method_handler(
            servicer.CreateBuild,
            request_deserializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.CreateBuildRequest.FromString,
            response_serializer=google_dot_longrunning_dot_operations__pb2.Operation.SerializeToString,
        ),
        "GetBuild": grpc.unary_unary_rpc_method_handler(
            servicer.GetBuild,
            request_deserializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.GetBuildRequest.FromString,
            response_serializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.Build.SerializeToString,
        ),
        "ListBuilds": grpc.unary_unary_rpc_method_handler(
            servicer.ListBuilds,
            request_deserializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.ListBuildsRequest.FromString,
            response_serializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.ListBuildsResponse.SerializeToString,
        ),
        "CancelBuild": grpc.unary_unary_rpc_method_handler(
            servicer.CancelBuild,
            request_deserializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.CancelBuildRequest.FromString,
            response_serializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.Build.SerializeToString,
        ),
        "RetryBuild": grpc.unary_unary_rpc_method_handler(
            servicer.RetryBuild,
            request_deserializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.RetryBuildRequest.FromString,
            response_serializer=google_dot_longrunning_dot_operations__pb2.Operation.SerializeToString,
        ),
        "CreateBuildTrigger": grpc.unary_unary_rpc_method_handler(
            servicer.CreateBuildTrigger,
            request_deserializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.CreateBuildTriggerRequest.FromString,
            response_serializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.BuildTrigger.SerializeToString,
        ),
        "GetBuildTrigger": grpc.unary_unary_rpc_method_handler(
            servicer.GetBuildTrigger,
            request_deserializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.GetBuildTriggerRequest.FromString,
            response_serializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.BuildTrigger.SerializeToString,
        ),
        "ListBuildTriggers": grpc.unary_unary_rpc_method_handler(
            servicer.ListBuildTriggers,
            request_deserializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.ListBuildTriggersRequest.FromString,
            response_serializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.ListBuildTriggersResponse.SerializeToString,
        ),
        "DeleteBuildTrigger": grpc.unary_unary_rpc_method_handler(
            servicer.DeleteBuildTrigger,
            request_deserializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.DeleteBuildTriggerRequest.FromString,
            response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        ),
        "UpdateBuildTrigger": grpc.unary_unary_rpc_method_handler(
            servicer.UpdateBuildTrigger,
            request_deserializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.UpdateBuildTriggerRequest.FromString,
            response_serializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.BuildTrigger.SerializeToString,
        ),
        "RunBuildTrigger": grpc.unary_unary_rpc_method_handler(
            servicer.RunBuildTrigger,
            request_deserializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.RunBuildTriggerRequest.FromString,
            response_serializer=google_dot_longrunning_dot_operations__pb2.Operation.SerializeToString,
        ),
        "CreateWorkerPool": grpc.unary_unary_rpc_method_handler(
            servicer.CreateWorkerPool,
            request_deserializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.CreateWorkerPoolRequest.FromString,
            response_serializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.WorkerPool.SerializeToString,
        ),
        "GetWorkerPool": grpc.unary_unary_rpc_method_handler(
            servicer.GetWorkerPool,
            request_deserializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.GetWorkerPoolRequest.FromString,
            response_serializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.WorkerPool.SerializeToString,
        ),
        "DeleteWorkerPool": grpc.unary_unary_rpc_method_handler(
            servicer.DeleteWorkerPool,
            request_deserializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.DeleteWorkerPoolRequest.FromString,
            response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        ),
        "UpdateWorkerPool": grpc.unary_unary_rpc_method_handler(
            servicer.UpdateWorkerPool,
            request_deserializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.UpdateWorkerPoolRequest.FromString,
            response_serializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.WorkerPool.SerializeToString,
        ),
        "ListWorkerPools": grpc.unary_unary_rpc_method_handler(
            servicer.ListWorkerPools,
            request_deserializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.ListWorkerPoolsRequest.FromString,
            response_serializer=google_dot_cloud_dot_devtools_dot_cloudbuild__v1_dot_proto_dot_cloudbuild__pb2.ListWorkerPoolsResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "google.devtools.cloudbuild.v1.CloudBuild", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))
