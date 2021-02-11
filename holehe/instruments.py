import trio
from tqdm import tqdm

class TrioProgress(trio.abc.Instrument):
    def __init__(self, total):
        self.tqdm = tqdm(total=total)

    def task_exited(self, task):
        if task.name.split(".")[-1] == "launch_module":
            self.tqdm.update(1)