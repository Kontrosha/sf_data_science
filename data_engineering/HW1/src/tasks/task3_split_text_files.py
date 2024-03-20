import os
from io import StringIO

import luigi
import pandas as pd

from .task2_extract_and_organize import ExtractAndOrganize


class SplitTextFiles(luigi.Task):
    dataset_name = luigi.Parameter()

    def requires(self):
        return ExtractAndOrganize(dataset_name=self.dataset_name)

    def output(self):
        return luigi.LocalTarget(f'execute_results/{self.dataset_name}/processed/processing_complete.txt')

    def run(self):
        extracted_dir = f'execute_results/{self.dataset_name}/extracted/'

        processed_dir = os.path.join(f'execute_results/{self.dataset_name}', 'processed')
        os.makedirs(processed_dir, exist_ok=True)

        for subdir, dirs, files in os.walk(extracted_dir):
            for file in files:
                if file.endswith('.txt'):
                    full_file_path = os.path.join(subdir, file)
                    self.process_file(full_file_path, processed_dir)

        with self.output().open('w') as marker_file:
            marker_file.write("Processing complete\n")

    def process_file(self, file_path, processed_dir):
        dfs = {}
        with open(file_path, 'r') as f:
            write_key = None
            fio = StringIO()
            for line in f.readlines():
                if line.startswith('['):
                    if write_key:
                        fio.seek(0)
                        header = None if write_key == 'Heading' else 'infer'
                        dfs[write_key] = pd.read_csv(fio, sep='\t', header=header)
                        fio = StringIO()  # Сбрасываем StringIO для следующей таблицы
                    write_key = line.strip('[]\n')
                    continue
                if write_key:
                    fio.write(line)
            if write_key:
                fio.seek(0)
                dfs[write_key] = pd.read_csv(fio, sep='\t')

        for key, df in dfs.items():
            output_file_path = os.path.join(processed_dir,
                                            f"{os.path.basename(os.path.splitext(file_path)[0])}_{key}.tsv").replace(
                ".txt", "")
            df.to_csv(output_file_path, sep='\t', index=False)
