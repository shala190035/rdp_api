import logging
import struct
import threading
import time
import random

from rdp.crud import Crud

logger = logging.getLogger("rdp.sensor")


class Reader:
    def __init__(self, crud: Crud, device: str = "/dev/rdp_cdev"):
        self._crud = crud
        self._device = device
        self._thread: threading.Thread = None

    def start(self) -> None:
        self._crud.add_device("dev1","test 1")
        self._crud.add_device("dev2","test 2")
        self._crud.add_device("dev3","test 3")

        self._thread = threading.Thread(target=self._run)
        self._thread.start()

    def stop(self):
        thread = self._thread
        self._thread = None
        thread.join()

    def _run(self) -> None:
        count = 0
        while self._thread is not None:
            logger.info("A")
            with open("/dev/rdp_cdev", "rb") as f:
                test = f.read(16)
                for i in range(16):
                    if i % 2:
                        print("  ", end="")
                value_time = 0
                for i in range(8):
                    value_time |= test[i] << 8 * i
                type_num = 0
                for i in range(4):
                    type_num |= test[i + 8] << 8 * i
                value = 0.0
                value = struct.unpack("f", test[-4::])
                logger.debug(
                    "Read one time: %d type :%d and value %f",
                    value_time,
                    type_num,
                    value[0],
                )
                try:
                    all_devices = self._crud.get_all_devices()
                    self._crud.add_value(value_time, type_num, value[0], random.choice(all_devices).id)
                except self._crud.IntegrityError:
                    logger.info("All Values read")
                    break
            time.sleep(0.1)
            count += 1
            if count % 100 == 0:
                logger.info("read 100 values")
                count = 0