#!/usr/bin/env python3
import sys
from typing import Dict
from typing import List

if len(sys.argv) == 1:
    sys.argv.append("final_log")


import json


class CanMsg:
    def __init__(self, canid, data):
        self.canid = canid
        self.data = data

    def __repr__(self):
        return f"CAN<{self.canid}, {self.data}>"


def parse_log(log_file):
    messages = list()
    with open(log_file) as f:
        for can_msg in f.readlines():
            can_id, can_data = can_msg.strip().split(" ")[-1].split("#")
            cm = CanMsg(can_id, can_data)
            messages.append(cm)
    #
    unique_datas = dict()
    #
    for canid in {msg.canid for msg in messages}:
        id_datas = {msg.data for msg in messages if msg.canid == canid}
        unique_datas[canid] = id_datas
    #
    return unique_datas


data = parse_log(sys.argv[1])


def gen_dbc_entry(can_id):
    dbc_entry = {
        "id": int(f"{can_id}", 16),
        "is_extended_frame": False,
        "name": f"Ox{can_id}",
        "signals": list(),
    }

    def gen_sig(start_bit, bit_length=8):
        return {
            "bit_length": bit_length,
            "factor": "1",
            "is_big_endian": True,
            "is_float": False,
            "is_signed": False,
            "name": f"Ox{can_id}_{start_bit}",
            "offset": "0",
            "start_bit": start_bit,
        }

    for start_bit in range(0, 64, 8):
        sig = gen_sig(start_bit=start_bit)
        dbc_entry["signals"].append(sig)

    return dbc_entry


dbc = {"messages": list()}  # type: Dict[str, List]

unique_message_dbc_threshold = 15

for can_id, can_messages in data.items():
    if len(can_messages) > unique_message_dbc_threshold:
        continue
    dbc["messages"].append(gen_dbc_entry(can_id))


dbc_json = "tesla_autogen.json"
dbc_file = "tesla_autogen.dbc"
print("Machen dbc-json")
with open(dbc_json, "w") as fp:
    json.dump(obj=dbc, fp=fp, indent=4, sort_keys=True)


import canmatrix.convert

canmatrix.convert.convert(
    infile=dbc_json,
    out_file_name=dbc_file,
    # ...
)
