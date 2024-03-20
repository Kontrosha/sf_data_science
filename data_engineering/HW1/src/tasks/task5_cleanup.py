import os

import luigi
from luigi import Task

from .task4_create_reduced_tables import CreateReducedTables


class Cleanup(Task):
    dataset_name = luigi.Parameter()

    def requires(self):
        return CreateReducedTables(dataset_name=self.dataset_name)

    def output(self):
        return luigi.LocalTarget(f'execute_results/{self.dataset_name}/cleanup_complete.txt')

    def run(self):
        extracted_dir = f'execute_results/{self.dataset_name}/extracted/'
        deleted_files_log = []

        for root, dirs, files in os.walk(extracted_dir, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                os.remove(file_path)
                deleted_files_log.append(file_path)

            for name in dirs:
                os.rmdir(os.path.join(root, name))

        with self.output().open('w') as marker_file:
            marker_file.write("Deleted files:\n" + "\n".join(deleted_files_log))