import json
import os

import luigi
import requests
from tqdm import tqdm

from .task0_find_download_link import FindDownloadLink


class DownloadDataset(luigi.Task):
    dataset_name = luigi.Parameter()
    filepath = ""

    def requires(self):
        return [FindDownloadLink(dataset_name=self.dataset_name)]

    def output(self):
        self.filepath = os.path.join("execute_results", self.dataset_name, f"{self.dataset_name}_RAW.tar")
        return luigi.LocalTarget(self.filepath)

    def run(self):
        print("path is ", self.input()[0])
        with self.input()[0].open('r') as infile:
            json_file = json.load(infile)
            url = json_file["download_link"]

        file_path = self.output().path

        if os.path.exists(file_path):
            print(f"Dataset {self.dataset_name} already downloaded.")
            return

        dataset_path = os.path.dirname(file_path)
        os.makedirs(dataset_path, exist_ok=True)

        response = requests.get(url, stream=True)
        with open(file_path, 'wb') as f, tqdm(
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
                total=int(response.headers.get('content-length', 0)),
                desc=self.dataset_name
        ) as bar:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))

        print(f"Dataset {self.dataset_name} has been downloaded.")
