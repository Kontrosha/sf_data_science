import sys

sys.path.append('tasks')

from luigi import build
from tasks.task0_find_download_link import FindDownloadLink
from tasks.task1_download_dataset import DownloadDataset
from tasks.task2_extract_and_organize import ExtractAndOrganize
from tasks.task3_split_text_files import SplitTextFiles
from tasks.task4_create_reduced_tables import CreateReducedTables
from tasks.task5_cleanup import Cleanup

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ds_name = sys.argv[1]
    else:
        print("Usage: python run_pipeline.py [DATASET_NAME]")
        sys.exit(1)
    print("Start pipeline with ds_name:", ds_name)
    # if you want, you can run each task
    build([
        # FindDownloadLink(dataset_name=ds_name),
        # DownloadDataset(dataset_name=ds_name),
        # ExtractAndOrganize(dataset_name=ds_name),
        # SplitTextFiles(dataset_name=ds_name),
        # CreateReducedTables(dataset_name=ds_name),
        Cleanup(dataset_name=ds_name)
    ], local_scheduler=False)
