import json
import time

import logging

from util.util import acquire_file_lock, LOCK_FILE, STATUS_FILE, syscmd, release_file_lock


def fetch_and_update_status():
    """
    Fetch and Update method with naive locking.
    :return: None
    """
    try:
        acquire_file_lock(LOCK_FILE)

        with open(STATUS_FILE, "w") as f:
            syscmd(['git', 'fetch'])
            cur_time = int(time.time())
            status = {"last_sync_time": cur_time}
            f.write(json.dumps(status))
        time.sleep(5)

        release_file_lock(LOCK_FILE)
    except IOError:
        logging.warn("failed to acquire log")
        return

if __name__ == "__main__":
    logging.basicConfig(filename="/tmp/neat_prompt.log", level=logging.DEBUG)
    fetch_and_update_status()
