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
# Generated code. DO NOT EDIT!
#
# Snippet for CreateBuildTrigger
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-build


# [START cloudbuild_v1_generated_CloudBuild_CreateBuildTrigger_async]
from google.cloud.devtools import cloudbuild_v1


async def sample_create_build_trigger():
    # Create a client
    client = cloudbuild_v1.CloudBuildAsyncClient()

    # Initialize request argument(s)
    trigger = cloudbuild_v1.BuildTrigger()
    trigger.autodetect = True

    request = cloudbuild_v1.CreateBuildTriggerRequest(
        project_id="project_id_value",
        trigger=trigger,
    )

    # Make the request
    response = await client.create_build_trigger(request=request)

    # Handle the response
    print(response)

# [END cloudbuild_v1_generated_CloudBuild_CreateBuildTrigger_async]
