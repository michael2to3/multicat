from pathlib import Path

from filemanager.searchengine import BaseSearchEngine


class FuzzySearchEngine(BaseSearchEngine):
    def __init__(self, min_similarity=0.6):
        self.min_similarity = min_similarity

    def _search_for_file(self, base_dir: Path, search_term: str) -> Path:
        search_term = search_term.lower()
        best_match = None
        highest_similarity = 0

        for file in self._walk(base_dir):

            relative_path_lower = str(file.relative_to(base_dir)).lower()
            similarity = self._calculate_similarity(relative_path_lower, search_term)
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = file

        if best_match and highest_similarity >= self.min_similarity:
            return best_match
        else:
            raise FileNotFoundError(
                f"File matching '{search_term}' not found in '{base_dir}' with a similarity of {highest_similarity}"
            )

    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]

    def _calculate_similarity(self, text, search_term):
        distance = self._levenshtein_distance(text, search_term)
        similarity = 1 - distance / max(len(text), len(search_term))
        return max(0, similarity)

    def _walk(self, base_dir):
        return base_dir.rglob("*")
