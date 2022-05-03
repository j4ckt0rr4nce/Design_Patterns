from abc import ABC, abstractmethod
import json


class InputData(ABC):
    @abstractmethod
    def get_data_from_file(self, file_path: str) -> None:
        """Method to get data from file"""
        

class ConcreteInputData(InputData):
    def get_data_from_file(self, file_path: str) -> None:
        records = map(json.loads, open(file_path, encoding="utf8"))
        return records