from typing import Dict, List
from hashcat.filemanager import FileManager
from hashcat.hashcat_executor_base import HashcatExecutorBase
from hashcat.hashcat_interface import HashcatInterface


class HashcatBenchmarkCalculationException(Exception):
    pass


class HashcatBenchmark(HashcatExecutorBase):
    def __init__(self, file_manager: FileManager, hashcat: HashcatInterface):
        self.file_manager = file_manager
        self.hashcat = hashcat

    def _reset_benchmark(self, benchmark_all=False):
        self.hashcat.reset()
        self.hashcat.quiet = True
        self.hashcat.benchmark = True
        self.hashcat.no_threading = True
        self.hashcat.benchmark_all = benchmark_all

    def benchmark(self, hash_modes: List[int]) -> Dict:
        hashrates = {}

        for hash_mode in hash_modes:
            self._reset_benchmark(benchmark_all=False)
            self.hashcat.hash_mode = hash_mode

            if not self.check_hexec():
                raise HashcatBenchmarkCalculationException(
                    f"Failed to benchmark the hash {hash_mode}"
                )

            hashrates[str(hash_mode)] = {
                "overall": self.hashcat.status_get_hashes_msec_all()
            }

        return hashrates

