import gzip
import os
import shutil
import tarfile

import luigi

from .task1_download_dataset import DownloadDataset


class ExtractAndOrganize(luigi.Task):
    dataset_name = luigi.Parameter()

    def requires(self):
        return [DownloadDataset(dataset_name=self.dataset_name)]

    def output(self):
        return luigi.LocalTarget(
            os.path.join("execute_results", self.dataset_name, "extracted", "extraction_complete.txt"))

    def run(self):
        input_path = self.input()[0].path
        extract_dir = os.path.join(os.path.dirname(input_path), 'extracted')
        os.makedirs(extract_dir, exist_ok=True)

        with tarfile.open(input_path, "r:*") as tar:
            tar.extractall(path=extract_dir)

        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                if file.endswith('.gz'):
                    gzip_path = os.path.join(root, file)
                    file_dir = os.path.splitext(gzip_path)[0].replace(".txt", "")
                    os.makedirs(file_dir, exist_ok=True)
                    with gzip.open(gzip_path, 'rb') as f_in:
                        with open(file_dir + '/' + os.path.basename(
                                os.path.splitext(file.replace(".txt", ""))[0]) + '.txt', 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    os.remove(gzip_path)

        with self.output().open('w') as marker_file:
            marker_file.write("Extraction complete\n")
