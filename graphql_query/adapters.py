import abc
from typing import Any


class AbstractAdapter(abc.ABC):

    @abc.abstractmethod
    def to_query(self) -> str:  # noqa
        raise NotImplementedError

    @abc.abstractmethod
    def from_query(self) -> Any:  # noqa
        raise NotImplementedError
