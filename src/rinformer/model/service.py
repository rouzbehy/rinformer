from abc import ABC, abstractmethod
from typing import Type, TypeVar, Any


class Service(ABC):

    @abstractmethod
    def query(self)-> dict[str, Any]: pass

T = TypeVar("T", bound=Service)
services : dict[str, Service] = {}


def register_service(service_cls: Type[T]) -> Type[T]:
    services[service_cls.__name__] = service_cls
    return service_cls


