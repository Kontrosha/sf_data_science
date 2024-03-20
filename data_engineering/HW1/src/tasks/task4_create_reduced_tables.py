import os

import luigi
import pandas as pd

from .task3_split_text_files import SplitTextFiles


class CreateReducedTables(luigi.Task):
    dataset_name = luigi.Parameter()

    def requires(self):
        return SplitTextFiles(dataset_name=self.dataset_name)

    def output(self):
        return luigi.LocalTarget(f'execute_results/{self.dataset_name}/reduced/reduction_complete.txt')

    def run(self):
        processed_dir = f'execute_results/{self.dataset_name}/processed/'

        reduced_dir = os.path.join(f'execute_results/{self.dataset_name}', 'reduced')
        os.makedirs(reduced_dir, exist_ok=True)

        for file_name in os.listdir(processed_dir):
            if "probes" in file_name.lower():
                full_file_path = os.path.join(processed_dir, file_name)
                df = pd.read_csv(full_file_path, sep='\t')

                columns_to_remove = ['Definition', 'Ontology_Component', 'Ontology_Process',
                                     'Ontology_Function', 'Synonyms', 'Obsolete_Probe_Id', 'Probe_Sequence']
                df_reduced = df.drop(columns=[col for col in columns_to_remove if col in df.columns])

                reduced_file_path = os.path.join(reduced_dir, f"reduced_{file_name}")
                df_reduced.to_csv(reduced_file_path, sep='\t', index=False)

        with self.output().open('w') as marker_file:
            marker_file.write("Reduction complete\n")
