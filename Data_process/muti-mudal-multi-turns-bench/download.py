import os
os.environ["HF_ENDPOINT"] = "http://mirrors.tools.huawei.com/huggingface"
from datasets import load_dataset

DARASET_PATH = "path/to/your/dataset"

## download dataset
dataset = load_dataset(DARASET_PATH)
print(dataset)

## filter
def is_multiround(example):
    return len(example['turns']) >= 2
filtered_dataset = dataset.filter(is_multiround)

