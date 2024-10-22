#!/usr/bin/env python3

import json

def get_load_average():
    with open("/proc/loadavg", "r") as f:
        load_avg_5min = f.read().split()[1]
    
    output = {
        "text": f"LA: {load_avg_5min}",
        "class": "load-avg",
    }
    
    print(json.dumps(output))

if __name__ == "__main__":
    get_load_average()

