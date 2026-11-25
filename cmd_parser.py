#!/bin/env python3
from os import path
import sys
import argparse

class CommandLineParser:
    def __init__(self, script_name):
        self.TemplateFilePath = None
        self.DataFilePath = None
        self.IsValid = False

        self.parse_cmd(script_name)
        self.IsValid = self.__validate_cmd()


    def parse_cmd(self, program_name):
        parser = argparse.ArgumentParser(
            prog=program_name,
            usage=f"{program_name} --template path/to/template/file"
            + " --data path/to/data/file")

        parser.add_argument(
            "-t", "--template",
            type=str,
            help="A template file for the e-mail body.")

        parser.add_argument(
            "-d", "--data",
            type = str,
            help = "A data file that contains e-mail addresses and respective"
            + "  data. Please do consider that the template has required fields"
            + "  and they have to be named the same way.")

        args = parser.parse_args()

        if len(sys.argv) <= 1:
            self.IsValid = False
            parser.print_help()
            sys.exit()

        self.TemplateFilePath = args.template
        self.DataFilePath     = args.data


    def __validate_cmd(self):
        if not self.__is_valid_path(self.TemplateFilePath):
            return False

        if not self.__is_valid_path(self.DataFilePath):
            return False

        self.TemplateFilePath = self.__path2abs_path(self.TemplateFilePath)
        self.DataFilePath = self.__path2abs_path(self.DataFilePath)
        return True


    def __is_valid_path(self, filepath):
        if filepath == None:
            return False

        if not path.exists(filepath):
            print(f"Error: {filepath} does not exist!")
            return False

        if not path.isfile(filepath):
            print(f"Error: {filepath} is not a file!")
            return False

        return True

    def __path2abs_path(self, filepath):
        return path.abspath(filepath)
