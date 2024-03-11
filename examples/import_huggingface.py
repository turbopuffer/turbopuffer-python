#!/usr/bin/python3

import sys
import time
import traceback
from typing import Iterable, Iterator

from datasets import load_dataset

import turbopuffer as tpuf


class DocumentMapper:
    doc_source: Iterator
    index: int

    def __init__(self, doc_source: Iterable):
        self.doc_source = iter(doc_source)
        self.index = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        value = next(self.doc_source)
        if value:
            vector = value.pop("emb")
            return tpuf.VectorRow(
                id=self.index,
                vector=vector,
                attributes=value,
            )
        return value


def main(dataset_name):
    docs = load_dataset(dataset_name, split="train", streaming=True)

    mapper = DocumentMapper(docs)
    ns = tpuf.Namespace(dataset_name.replace("/", "-"))
    start_time = time.monotonic()
    try:
        ns.upsert(mapper)
    except Exception:
        traceback.print_exc()
    finally:
        print("Upserted", mapper.index + 1, "documents")
        print("Took:", (time.monotonic() - start_time), "seconds")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            f"Usage: {sys.argv[0]} <dataset_name>\n"
            "    Default TURBOPUFFER_API_KEY will be used from environment."
        )
        sys.exit(1)

    main(sys.argv[1])
