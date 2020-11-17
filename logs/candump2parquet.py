#!/usr/bin/env python3
"""Non-production script to convert a candump archive to parquet format for bulk processing with Dask.
"""
import struct

import fsspec
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from tqdm import tqdm

fs = fsspec.filesystem("file")

with fs.open(path="final_log") as f:
    candump_log_data = f.read()

"""
On Differential Equations 2:

"So you set it up in Maple, smack it with the $3000 hammer on your desk, and eat popcorn." - Dr Graves.

https://www.rose-hulman.edu/news/2017/campus-mourns-loss-of-professor-elton-graves.html
"""
hammer = dict()

# Init the CAN dict.
def init_dict(can_data):
    tmp = dict(
        {
            "timestamp": list(),
            "canbus": list(),
            "can_id": list(),
            "can_id_hex": list(),
            "can_data_hex": list(),
        }
    )
    # Determine how many bytes we should have.
    for byte in range(int(len(can_data) / 2)):
        tmp[f"B{byte:02d}"] = list()
        tmp[f"b{byte:02d}"] = list()
    return tmp


def process_log_line(can_line):
    ## Preprocess
    if isinstance(can_line, bytes):
        can_line = can_line.decode()
    ## Process the candump log line.
    time_raw, bus_raw, msg_raw = can_line.split(" ")
    can_id_hex_str, can_data = msg_raw.split("#")
    timestamp = float(time_raw.strip(")("))
    ## Init
    if not can_id_hex_str in hammer:
        hammer[can_id_hex_str] = init_dict(can_data)
    # Append the data to the appropriate dict key.
    hammer[can_id_hex_str]["timestamp"].append(timestamp)
    hammer[can_id_hex_str]["canbus"].append(bus_raw)
    hammer[can_id_hex_str]["can_id"].append(int(can_id_hex_str, base=16))
    hammer[can_id_hex_str]["can_id_hex"].append(can_id_hex_str)
    hammer[can_id_hex_str]["can_data_hex"].append(can_data)

    # Chunk the can_data string into a list of bytes.
    can_data_bytes = [
        int(can_data[idx : idx + 2], base=16) for idx in range(0, len(can_data), 2)
    ]
    # For each byte and byte position, decode the struct as little/big endian.
    # Upfront data manipulation as an example.
    for byte_idx, byte_data in enumerate(can_data_bytes):
        hammer[can_id_hex_str][f"B{byte_idx:02d}"].append(byte_data)
        byte_data_unsigned = struct.unpack("<b", struct.pack("<B", byte_data))[0]
        hammer[can_id_hex_str][f"b{byte_idx:02d}"].append(byte_data_unsigned)


# Process the can log.
for can_line in tqdm(candump_log_data.splitlines()):
    process_log_line(can_line)

# Write the parquet file.
for can_id_hex, can_id_data in tqdm(hammer.items()):
    df = pd.DataFrame(can_id_data)
    table = pa.Table.from_pandas(df)
    parquet_file = f"candump_0x{can_id_hex}.parquet"
    pq.write_table(table, parquet_file)
