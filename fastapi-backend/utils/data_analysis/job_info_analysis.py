import os

from register.tortoise import TORTOISE_ORM


def get_basic_info():
    import pandas as pd
    current_dir = os.path.dirname(os.path.realpath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    dataset_path = os.path.join(project_root, 'static', 'job_info_dataset.xlsx')
    df = pd.read_excel(dataset_path)
    print(df)


if __name__ == '__main__':
    print(TORTOISE_ORM)
