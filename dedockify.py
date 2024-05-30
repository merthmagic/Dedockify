#!/usr/bin/python3

from sys import argv
import docker
import docker.errors

class ImageNotFound(Exception):
    pass


class MainObj:
    def __init__(self):
        super(MainObj, self).__init__()
        self.commands = []
        self.cli = docker.client.from_env()
        self._get_image(argv[-1])
        self.hist = self.img.history()
        self._parse_history()
        self.commands.reverse()
        self._print_commands()

    def _print_commands(self):
        for i in self.commands:
            print(i)

    def _get_image(self, img_hash):
        try:
            img = self.cli.images.get(img_hash)
            self.img = img
        except docker.errors.ImageNotFound:
            raise ImageNotFound("Image {} not found".format(img_hash))
        

    def _insert_step(self, step):
        if "#(nop)" in step:
            to_add = step.split("#(nop) ")[1]
        else:
            to_add = ("RUN {}".format(step))
        to_add = to_add.replace("&&", "\\\n    &&")
        self.commands.append(to_add.strip(' '))

    def _parse_history(self, rec=False):
        first_tag = False
        actual_tag = False
        for i in self.hist:
            if i['Tags']:
                actual_tag = i['Tags'][0]
                if first_tag and not rec:
                    break
                first_tag = True
            self._insert_step(i['CreatedBy'])
        if not rec:
            self.commands.append("FROM {}".format(actual_tag))


__main__ = MainObj()