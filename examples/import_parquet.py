#!/usr/bin/python3

import glob
import os
import sys
import time
import pandas as pd
import turbopuffer as tpuf
import traceback
import threading
from queue import Queue

NUM_THREADS = 4


def read_docs_to_queue(queue, parquet_files):
    try:
        file_offset = 0
        for parquet_file in parquet_files:
            df = pd.read_parquet(parquet_file).rename(columns={'emb': 'vector'})
            if 'id' not in df.keys():
                df['id'] = range(file_offset, file_offset+len(df))
            queue.put(df)
            file_offset += len(df)
    except Exception:
        print('Failed to read batch:')
        traceback.print_exc()
    for _ in range(0, NUM_THREADS):
        queue.put(None)  # Signal the end of the documents


def upsert_docs_from_queue(input_queue, dataset_name):
    ns = tpuf.Namespace(dataset_name)

    batch = input_queue.get()
    while batch is not None:
        try:
            ns.upsert(batch)
            print(f"Completed {batch['id'][0]}..{batch['id'][batch.shape[0]-1]}")
        except KeyboardInterrupt:
            break
        except Exception:
            print(f"Failed to upsert batch: {batch['id'][0]}..{batch['id'][batch.shape[0]-1]}")
            traceback.print_exc()
        batch = input_queue.get()


def main(dataset_name, input_path):
    input_glob = os.path.join(input_path, "*.parquet")
    parquet_files = glob.glob(input_glob)

    if len(parquet_files) == 0:
        print(f"No .parquet files found in: {input_glob}")
        sys.exit(1)

    doc_queue = Queue(NUM_THREADS)
    read_thread = threading.Thread(target=read_docs_to_queue, args=(doc_queue, parquet_files))
    upsert_threads = []

    start_time = time.monotonic()

    try:
        read_thread.start()

        for _ in range(NUM_THREADS):
            upsert_thread = threading.Thread(target=upsert_docs_from_queue, args=(doc_queue, dataset_name))
            upsert_threads.append(upsert_thread)
            upsert_thread.start()

        read_thread.join()

        for upsert_thread in upsert_threads:
            upsert_thread.join()

    finally:
        print('Upserted', doc_queue.qsize(), 'documents')
        print('Took:', (time.monotonic() - start_time), 'seconds')


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <dataset_name> <input_folder>\n"
              "    Default TURBOPUFFER_API_KEY will be used from environment.")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
