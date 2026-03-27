# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 14:26:27 2026

@author: Logan.Jamison
"""

import time
import requests
import pandas as pd
import io

def safe_api(url, params, retries=3, delay=1):
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, timeout=20)
            r.raise_for_status()

            data = r.json()   # this is where empty responses fail
            if data:          # non-empty JSON
                return data

            print("Empty JSON, retrying...")
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")

        time.sleep(delay)

    return None




def safe_read_csv(url, retries=3, delay=1, timeout=20):
    last_error = None

    for attempt in range(1, retries + 1):
        try:
            r = requests.get(url, timeout=timeout)
            r.raise_for_status()

            # Try reading CSV from bytes
            return pd.read_csv(io.BytesIO(r.content))

        except Exception as e:
            print(f"[Attempt {attempt}] Failed to download CSV: {e}")
            last_error = e
            time.sleep(delay)

    print(f"safe_read_csv: failed after {retries} attempts. Last error: {last_error}")
    return None
