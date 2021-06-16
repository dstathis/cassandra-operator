#!/usr/bin/env python3

#  Copyright 2021 Canonical Ltd.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import logging
from juju import loop
from juju.model import Model


async def deploy():
    model = Model()
    print("Connecting")
    await model.connect()
    print("Connecting Complete")

    try:
        print("Deploying")
        app = await model.deploy('local:./cassandra-k8s.charm', resources={
            "cassandra-image": "dstathis/cassandra-operator-image:latest"
        }, series="focal")
        print("Deploying Complete")
        await model.block_until(lambda: app.status == "active", timeout=300)
        await app.add_unit(count=2)
        await model.block_until(lambda: app.status == "active", timeout=300)
    finally:
        await model.disconnect()


def main():
    logging.basicConfig(level=logging.INFO)
    loop.run(deploy())


if __name__ == "__main__":
    main()
