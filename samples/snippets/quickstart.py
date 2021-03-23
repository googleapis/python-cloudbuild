# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# [START cloudbuild_python_quickstart]
from google.cloud.devtools import cloudbuild_v1
import google.auth


def quickstart():
    """Create and execute a simple Google Cloud Build configuration, 
    print the in-progress status and print the completed status."""


    # Authorize the client with Google defaults
    credentials, project_id = google.auth.default()
    client = cloudbuild_v1.services.cloud_build.CloudBuildClient()

    build = cloudbuild_v1.Build()

    # The following build steps will output "hello world"
    # For more information on build configuration, see 
    # https://cloud.google.com/build/docs/configuring-builds/create-basic-configuration
    build.steps = [{"name": "ubuntu", 
                    "entrypoint": "bash",
                    "args": ["-c", "echo hello world"]}]

    operation = client.create_build(project_id=project_id, build=build)
    # Print the in-progress operation
    print("IN PROGRESS:")
    print(operation.metadata)

    result = operation.result()
    # Print the completed status
    print("RESULT:", result.status)
# [END cloudbuild_python_quickstart]


if __name__ == "__main__":
    quickstart()
