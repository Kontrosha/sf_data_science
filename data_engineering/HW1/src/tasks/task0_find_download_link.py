import json
import os

import luigi
import requests
from bs4 import BeautifulSoup


class FindDownloadLink(luigi.Task):
    dataset_name = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(f'execute_results/{self.dataset_name}_download_link.json')

    def run(self):
        url = f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={self.dataset_name}"
        response = requests.get(url, timeout=60)
        soup = BeautifulSoup(response.text, 'html.parser')

        os.makedirs("execute_results", exist_ok=True)

        # Здесь должен быть код на поиск ссылки, пока гвоздь
        download_link = \
            f"https://www.ncbi.nlm.nih.gov/geo/download/?acc={self.dataset_name}&format=file"

        result = {
            "download_link": download_link,
        }

        with self.output().open('w') as out_file:
            out_file.write(json.dumps(result))
