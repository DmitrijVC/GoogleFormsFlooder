import requests
import os
import json
import threading
import logging
import random


class _Math:
    @staticmethod
    def chance(percent: int):
        if random.randrange(0, 100) < percent:
            return True
        return False


class Settings:
    def __init__(
            self,
            skip_not_required: bool = True,
            headers: dict = {},
            cookies: dict = {},
            payload: dict = {},
            tokens: list = []
    ):
        self.skip_not_required = skip_not_required
        self.headers = headers
        self.cookies = cookies
        self.payload = payload
        self.tokens = tokens

    def __dir__(self):
        return [
            str(self.skip_not_required)
        ]

    def __str__(self):
        return f"{self.to_dict()}"

    def to_dict(self):
        return self.__dict__

    # @staticmethod
    # def to_settings(data: dict):
    #     return Settings()


class Flooder:
    def __init__(self, form_id: str, settings: Settings = None):
        self.form_id = form_id
        self.settings = settings

        if settings is not None:
            self.headers = settings.headers
            self.cookies = settings.cookies
            self.payload = settings.payload
            self.tokens = settings.tokens
        else:
            self.headers = {}
            self.cookies = {}
            self.payload = {}
            self.tokens = {}

        self.form_url_view = f"https://docs.google.com/forms/d/e/{form_id}/viewform"
        self.form_url_response = f"https://docs.google.com/forms/d/e/{form_id}/formResponse"

        self.json: dict = {}
        self.view: dict = {}
        self.har: dict = {}
        self.payload = {}
        self.counter = 0

    def _get_data(self):
        result = requests.get(self.form_url_view)
        print(result.headers)

    def from_har(self, file_name: str, use_headers: bool = False, use_cookies: bool = False):
        warn_msg = "Har not initialized!"
        if os.path.exists(file_name):
            try:
                with open(file_name, "r") as f:
                    content = json.loads(f.read())
                    if content["log"]["entries"] is not []:
                        entry: dict
                        for entry in content["log"]["entries"]:
                            if self.form_id in entry["request"]["url"]:
                                self.har = entry
                                if use_headers:
                                    self.headers = entry["request"]["headers"]
                                if use_cookies:
                                    self.cookies = entry["request"]["cookies"]
                                f.close()
                                return self
                        logging.warning(f"{warn_msg} Valid entry has not been found.")
                        f.close()
                        return self
                    logging.warning(f"{warn_msg} No entries has been found.")
                    f.close()
                    return self
            except Exception as e:
                logging.warning(f"{warn_msg} Can't open the har file, {e}")
                return self
        logging.warning(f"{warn_msg} Har file does not exists")
        return self

    def from_json(self, file_name: str):  # , use_headers: bool = False, use_cookies: bool = False):
        warn_msg = "Json not initialized!"
        if os.path.exists(file_name):
            try:
                with open(file_name, "r") as f:
                    content = json.loads(f.read())
                    for entry in content["entries"]:
                        self.json[f"entry.{entry['id']}"] = entry['values']
                f.close()
                return self
            except Exception as e:
                logging.warning(f"{warn_msg} Can't open the json file, {e}")
                return self
        logging.warning(f"{warn_msg} Json file does not exists.")
        return self

    def _prepare(self):
        if self.har.__len__() is not 0:
            for param in self.har["request"]["postData"]["params"]:
                self.payload[param["name"]] = param["value"]

    def _run(self):
        looper = self.tokens.__len__()
        if looper > 0:
            looper -= 1
        while True:
            self.counter += 1
            if self.json.__len__() is not 0:
                for entry_id, entry_values in self.json.items():
                    self.payload[entry_id] = random.choice(entry_values)
            try:
                self.payload["token"] = self.tokens[looper]  # change it !!!!
            except:
                pass
            result = requests.post(self.form_url_response, data=self.payload)
            logging.info(f"[{self.counter}] Result: {result.status_code}")

            if self.tokens.__len__() is not 0:
                looper -= 1
                if looper <= 0:
                    break

    def run(self, use_threading: bool = False):
        self._prepare()
        if use_threading:
            thread = threading.Thread(target=self._run)
            thread.start()
            return thread
        self._run()
