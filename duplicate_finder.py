from dataclasses import dataclass
from typing import List, Set, Dict
import re
from pathlib import Path
from itertools import combinations
from collections import defaultdict


@dataclass(frozen=True)
class Company:
    """A data structure to represent a company with its original name and cleaned name."""

    original_name: str
    cleaned_name: str


class DuplicateFinder:
    """A class with self-contained pipeline for outputting potential duplicate companies from a list of
    company names. This class handles the entire duplicate detection process, from reading input files,
    cleaning company names, detecting duplicates, to writing results to an output file.
    """

    # Class constants for regex patterns
    URL_PATTERN = r"www\.|\.(?:com|org|net)"
    PUNCTUATION_PATTERN = r"[^\w\s]"

    # Class constants for default paths
    DEFAULT_OUTPUT_PATH = Path("output/duplicates.txt")
    DEFAULT_REMOVAL_WORDS_PATH = Path("removal_words.txt")

    def __init__(
        self,
        output_path: Path = DEFAULT_OUTPUT_PATH,
        removal_words_path: Path = DEFAULT_REMOVAL_WORDS_PATH,
    ):
        """Initialize the DuplicateFinder class.

        Args:
            output_path: The path to the output file to write duplicate pairs. Defaults to `output/duplicates.txt`.
            removal_words_path: The path to the file containing explicit words/phrases to remove from company names during preprocessing. Defaults to `removal_words.txt`.
        """
        self.output_path = output_path
        self.removal_words: Set[str] = {
            line.strip() for line in removal_words_path.open()
        }

    def find_duplicates(self, input_path: Path) -> None:
        """Entry point for the duplicate finder pipeline.

        Orchestrates the complete process of reading input, finding duplicates, and writing results.

        Args:
            input_path: Path to the input file containing company names, one per line.
        """
        companies = self._read_companies_(input_path)
        duplicates = self._find_duplicates_(companies)
        self._write_output_(duplicates)

    def _read_companies_(self, input_path: Path) -> List[Company]:
        """Reads and preprocesses company names from the input file.

        Creates Company objects with both original and cleaned names for each non-empty line
        in the input file.

        Args:
            input_path: Path to the input file containing company names.

        Returns:
            A list of Company objects, each containing both original and cleaned company names.
        """
        with open(input_path, "r", encoding="utf-8") as f:
            return [
                Company(name, self._clean_name_(name))
                for line in f
                if (name := line.strip())
            ]

    def _find_duplicates_(self, companies: List[Company]) -> List[List[Company]]:
        """Finds duplicate companies using their cleaned names as keys.

        Groups companies by their cleaned names and returns groups with more than one company.

        Args:
            companies: A list of Company objects to check for duplicates.

        Returns:
            A list of lists, where each inner list contains Company objects that are
            considered duplicates of each other based on their cleaned names.
        """
        company_dict = defaultdict(list)
        for company in companies:
            company_dict[company.cleaned_name].append(company)

        return [group for group in company_dict.values() if len(group) > 1]

    def _write_output_(self, duplicate_groups: List[List[Company]]) -> None:
        """Writes the duplicate groups to the output file.

        For each group of duplicates, writes all possible pairs of original company names
        to the output file, one pair per line.

        Args:
            duplicate_groups: A list of lists, where each inner list contains Company
                objects that are duplicates of each other.
        """
        print(
            f"Writing {len(duplicate_groups)} duplicate groups to {self.output_path}."
        )

        with open(self.output_path, "w", encoding="utf-8") as f:
            duplicate_pairs = (
                f"{company1.original_name}, {company2.original_name}\n"
                for group in duplicate_groups
                for company1, company2 in combinations(group, 2)
            )
            f.writelines(duplicate_pairs)

    def _clean_name_(self, name: str) -> str:
        """Cleans a company name for standardized comparison.

        Performs the following transformations:
        1. Converts to lowercase
        2. Removes URL components using URL_PATTERN
        3. Removes punctuation using PUNCTUATION_PATTERN
        4. Removes common business terms from removal_words
        5. Normalizes whitespace

        Args:
            name: The original company name to clean.

        Returns:
            A cleaned and standardized version of the company name for comparison.
        """
        return " ".join(
            word
            for word in re.sub(
                self.PUNCTUATION_PATTERN,
                " ",
                re.sub(self.URL_PATTERN, "", name.lower()),
            ).split()
            if word not in self.removal_words
        )
