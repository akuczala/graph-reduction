from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Callable, Dict, Union, Type, Optional


class ValueType(ABC):
    pass


V = TypeVar('V', bound=ValueType)
T = TypeVar('T')


@dataclass
class ADT(ABC):
    value: ValueType

    @property
    @abstractmethod
    def match_kwargs(self) -> Dict[Type[V], str]:
        pass

    @property
    @abstractmethod
    def _default_expect_value_exceptions(self) -> Dict[str, Callable[[ValueType], Exception]]:
        pass

    def match_value(self, **kwargs: Callable[[ValueType], T]) -> T:
        matched_fn: Optional[Callable[[ValueType], T]] = next(
            (
                kwargs[kw_name] for value_type, kw_name in self.match_kwargs.items()
                if isinstance(self.value, value_type)
            ), None
        )
        if matched_fn is None:
            raise ValueError(f"{self.value} of type {type(self.value)} is not a valid {type(self)} value")
        else:
            return matched_fn(self.value)

    def expect_value(self,
                     **kwargs: Callable[[ValueType], Union[T, Exception]]) -> T:
        """
        Raises error if we match on something we don't specify a lambda for. Error messages can be customized
        by passing lambdas that return Exceptions
        """
        result = self.match_value(**dict(self._default_expect_value_exceptions, **kwargs))
        if isinstance(result, Exception):
            raise result
        else:
            return result
