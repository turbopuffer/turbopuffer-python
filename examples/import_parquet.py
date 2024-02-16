#!/usr/bin/python3

import glob
import os
import sys
import time
import turbopuffer as tpuf
from pyarrow.parquet import ParquetFile
import traceback
import threading
from queue import Queue, Full

NUM_THREADS = 8

# Update these values to resume upserting
START_OFFSET = 0
MAX_OFFSET = None # 1_000_000

# Adjust lower if request body ends up too large
tpuf.upsert_batch_size = 10_000

# Print in a way that doesn't mash lines from different threads together
def thread_print(message):
    print(f'{message}\n', end='')


def read_docs_to_queue(queue, parquet_files, exiting):
    try:
        file_offset = 0
        for file_path in parquet_files:
            while queue.full() and not exiting.is_set():
                time.sleep(1)
            if exiting.is_set():
                return
            parquet_file = ParquetFile(file_path, memory_map=True)
            file_size = parquet_file.metadata.num_rows
            if MAX_OFFSET is not None and file_offset > MAX_OFFSET:
                thread_print(f'Skipping remaining files, file_offset from {file_offset} to {file_offset + file_size - 1}')
                break
            elif file_offset + file_size <= START_OFFSET:
                thread_print(f'Skipped {file_path}, file_offset from {file_offset} to {file_offset + file_size - 1}')
                file_offset += file_size
            else:
                # Add any attribute columns to include after 'emb'
                for i in parquet_file.iter_batches(batch_size=tpuf.upsert_batch_size, columns=['emb']):
                    df = i.to_pandas().rename(columns={'emb': 'vector'})
                    if 'id' not in df.keys():
                        df['id'] = range(file_offset, file_offset+len(df))
                    if file_offset + len(df) <= START_OFFSET:
                        thread_print(f'Skipped batch file_offset from {file_offset} to {file_offset + len(df) - 1}')
                        file_offset += len(df)
                        continue
                    elif MAX_OFFSET is not None and file_offset > MAX_OFFSET:
                        thread_print(f'Skipping remaining files, file_offset from {file_offset} to {file_offset + len(df) - 1}')
                        break

                    while not exiting.is_set():
                        try:
                            queue.put(df, timeout=1)
                            break
                        except Full:
                            pass
                    thread_print(f'Loaded {file_path}, file_offset from {file_offset} to {file_offset + len(df) - 1}')
                    file_offset += len(df)
    except Exception:
        thread_print('Failed to read batch:')
        traceback.print_exc()
    for _ in range(0, NUM_THREADS):
        queue.put(None)  # Signal the end of the documents


def upsert_docs_from_queue(input_queue, dataset_name, exiting):
    ns = tpuf.Namespace(dataset_name)

    batch = input_queue.get()
    while batch is not None and not exiting.is_set():
        try:
            before = time.monotonic()
            ns.upsert(batch)
            time_diff = time.monotonic() - before
            thread_print(f"Completed {batch['id'][0]}..{batch['id'][batch.shape[0]-1]} time: {time_diff} / {len(batch)} = {len(batch)/time_diff}")
        except Exception:
            thread_print(f"Failed to upsert batch: {batch['id'][0]}..{batch['id'][batch.shape[0]-1]}")
            traceback.print_exc()
        batch = input_queue.get()


def main(dataset_name, input_path):
    input_glob = os.path.join(input_path, "*.parquet")
    parquet_files = glob.glob(input_glob)

    if len(parquet_files) == 0:
        thread_print(f"No .parquet files found in: {input_glob}")
        sys.exit(1)

    sorted_files = sorted(sorted(parquet_files), key=len)

    ns = tpuf.Namespace(dataset_name)
    if ns.exists():
        thread_print(f'The namespace "{ns.name}" already exists!')
        existing_dims = ns.dimensions()
        thread_print(f'Vectors: {ns.approx_count()}, dimensions: {existing_dims}')
        response = input('Delete namespace? [y/N]: ')
        if response == 'y':
            ns.delete_all()
        else:
            response2 = input(f'Resume upsert from {START_OFFSET}? [y/N]: ')
            if response2 != 'y':
                thread_print('Cancelled')
                sys.exit(1)

    exiting = threading.Event()
    doc_queue = Queue(NUM_THREADS)
    read_thread = threading.Thread(target=read_docs_to_queue, args=(doc_queue, sorted_files, exiting))
    upsert_threads = []

    start_time = time.monotonic()

    try:
        read_thread.start()

        for _ in range(NUM_THREADS):
            upsert_thread = threading.Thread(target=upsert_docs_from_queue, args=(doc_queue, dataset_name, exiting))
            upsert_threads.append(upsert_thread)
            upsert_thread.start()

        read_thread.join()

        for upsert_thread in upsert_threads:
            upsert_thread.join()
    except KeyboardInterrupt:
        exiting.set()
        sys.exit(1)
    finally:
        thread_print('DONE!')
        thread_print(f'Took: {time.monotonic() - start_time:.3f} seconds')


if __name__ == "__main__":
    if len(sys.argv) != 3:
        thread_print(f"Usage: {sys.argv[0]} <dataset_name> <input_folder>\n"
                      "    Default TURBOPUFFER_API_KEY will be used from environment.")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
