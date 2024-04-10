from typing import Dict, List

from hashcat.executor_base import HashcatExecutorBase


class HashcatBenchmarkCalculationException(Exception):
    pass


class HashcatBenchmark(HashcatExecutorBase):
    def _reset_benchmark(self, benchmark_all=False):
        self._hashcat.reset()
        self._hashcat.quiet = True
        self._hashcat.benchmark = True
        self._hashcat.no_threading = True
        self._hashcat.benchmark_all = benchmark_all

    def benchmark(self, hash_modes: List[int]) -> Dict:
        hashrates = {}

        for hash_mode in hash_modes:
            self._reset_benchmark(benchmark_all=False)
            self._hashcat.hash_mode = hash_mode

            if not self.check_hexec():
                raise HashcatBenchmarkCalculationException(
                    f"Failed to benchmark the hash {hash_mode}"
                )

            hashrates[str(hash_mode)] = {
                "overall": self._hashcat.status_get_hashes_msec_all()
            }

        return hashrates
