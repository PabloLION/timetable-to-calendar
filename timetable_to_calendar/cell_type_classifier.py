__todo__ = """this file should include some AI NLP to classify if the cell 
value is an "event_id", "time_slot" or "date". Also in the future "location", 
"description", "event_name", "event_status", "comment", etc.. (commented code)

Now it can only classify "event_id", "time_slot" and "date" by simple regular
expression. And cannot classify weekdays, week count, etc. (excluded first two
rows when used).
"""

import enum
import re

WEEKDAY = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
IGNORED = "h"


class CellType(enum.Enum):
    EVENT_ID = enum.auto()
    TIME_SLOT = enum.auto()
    DATE = enum.auto()
    EMPTY = enum.auto()
    OTHER = enum.auto()
    # not used yet
    # WEEKDAY = enum.auto()
    # LOCATION = enum.auto()
    # DESCRIPTION = enum.auto()
    # EVENT_NAME = enum.auto()
    # EVENT_TYPE = enum.auto()
    # EVENT_STATUS = enum.auto()
    # COMMENT = enum.auto()


class CellTypeClassifier:
    """
    Class for classifying cell values based on predefined patterns.
    Initialize with a set of values to classify, then call the object with a
    value to classify it. Or equivalently, call the classify method.
    """

    def __init__(self, value_set: set[str | None]):
        """
        Initializes a ValueClassifier object.

        Args:
            value_set (set[str | None]): A set of values to classify.
        """
        self.value_set = value_set
        self.classified_value_dict = self._gen_classification_dict()

    def _gen_classification_dict(self) -> dict:
        """
        Generates a dictionary mapping values to their corresponding cell types.

        Returns:
            dict: A dictionary mapping values to CellType.
        """
        d: dict = {"": CellType.EMPTY, None: CellType.EMPTY}
        for value in self.value_set:
            if value in d:
                continue
            if not value:  # "" and None
                d[value] = CellType.EMPTY
            elif re.match(r"^\d+-\d+$", value):  # like 07-08, 8-9, 11-12, etc.
                d[value] = CellType.TIME_SLOT
            elif re.match(r"^\d+/\d+$", value):  # like 1/1, 1/2, 1/3, etc.
                d[value] = CellType.DATE
            elif re.match(r"^\d+-\w+\.?$", value):  # like 1-gen, 28-nov, etc.
                d[value] = CellType.DATE
            elif re.match(r"^\w+-\d+$", value):  # like gen-1, nov-28, etc.
                d[value] = CellType.DATE
            elif value.startswith("Setmana "):
                d[value] = CellType.OTHER
            elif value in WEEKDAY or value in IGNORED:
                d[value] = CellType.OTHER
            else:
                d[value] = CellType.EVENT_ID
        return d

    def __call__(self, word: str | None) -> CellType:
        """
        Classifies a word into a CellType.

        Args:
            word (str | None): The word to classify.

        Returns:
            CellType: The classified cell type.
        """
        return self.classified_value_dict[word]

    def classify(self, word: str | None) -> CellType:
        """
        Classifies a word into a CellType.

        Args:
            word (str | None): The word to classify.

        Returns:
            CellType: The classified cell type.
        """
        return self(word)
