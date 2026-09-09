
import json
import os

class Storer:
    def __init__(self, data, table):
        self.table = table

    def DataStore(self, filename = "Data.json"):
        self.File
        try:
            with open(filename, "r") as f:
                self.File = f
        except FileNotFoundError:
            self.File = open(filename, "x").close()

        try:
            

        








class Retreiver:
