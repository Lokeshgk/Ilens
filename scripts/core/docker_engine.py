import os
import json
import docker
# from scripts.utils.config import VOLUMES
from scripts.utils.logsetup import logger


class DockerEngine(object):
    def __init__(self):
        try:
            self.client = docker.DockerClient(base_url="tcp://127.0.0.1:4243")
            # TO DO CHANGE THIS
            self.client.login(username='chandrakanthg',
                              password='gck@kl9897')
        except Exception as e:
            print("Failed to connect to docker daemon")
            logger.error("Failed to connect to docker daemon : {}".format(str(e)))

    def pull_image(self, data):
        try:
            logger.debug("Pulling image : {}".format(data['image']))
            self.client.images.pull(repository=data['image'])
            print(10 * "===>")
            print("Successfully pulled image from the registry")
        except self.client.errors.APIError as de:
            logger.error("Error occurred while pulling the image : {}".format(str(de)), exc_info=True)
        except Exception as e:
            logger.error("Error occurred while pulling the image : {}".format(str(e)), exc_info=True)

    def run_image(self, data):
        try:
            print("Started pulling the image")
            logger.debug("Started pulling container : {}".format(data['image']))
            self.client.images.pull(repository='chandrakanthg/data_processor:0.2')
            logger.debug("Image pull completed")
            print("Image pull completed successfully")
            print(10 * "===>")
            print("Started running container")
            container_run = self.client.containers.run(data["image"], restart_policy={"Name": "always"},
                                                       environment={ "PIPELINE_ID": data["request_json"]["pipeline_id"],
                                                                     "config": json.dumps(data["request_json"]["config"]),
                                                                     'JOB_ID': data["request_json"]['job_id'] },
                                                       name=data["request_json"]["pipeline_id"],
                                                       detach=True
                                                       )
            print(container_run)
            print("Container started successfully")
        except Exception as e:
            logger.error("Error occurred while running the container : {}".format(str(e)), exc_info=True)
        except self.client.errors.APIError as de:
            logger.error("Error occurred while running the container: {}".format(str(de)), exc_info=True)

