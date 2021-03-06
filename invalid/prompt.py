from typing import Union
from pick import pick
from dateutil.parser import parse as dateparse
from os import system


class _Prompt:
    def __init__(self, name, validate=None, default=None) -> None:
        self.imperative = "Enter"
        self.name = name
        self.validate = validate
        self.default = default

        self.__repr__ = lambda self: f"{self.__class__.__name__} prompt type"

    def __repr__(self) -> str:
        return "Prompt superclass"

    @property
    def title(self):
        return f"{self.imperative} {self.name}: "

    def parse(self, response):
        return response

    @staticmethod
    def clear():
        system("cls")
        system("clear")

    def prompt(self):
        self.clear()
        while True:
            if self.default:
                response = input(
                    f"{self.imperative} {self.name} (default: {self.default}): "
                )
            else:
                response = input(self.title)
            try:
                if not response:
                    if self.default:
                        response = self.default
                    else:
                        raise ValueError

                response = self.parse(response)

                if self.validate:
                    if self.validate(response):
                        break
                    else:
                        raise ValueError
                else:
                    break

            except Exception:
                _Prompt.clear()
                print(f"Invalid {self.name} '{response}'")

        _Prompt.clear()
        return response


class List(_Prompt):
    def __init__(
        self, name, options: Union[dict, list], indicator="->", default=None
    ) -> None:
        self.imperative = "Select"
        self.options = options
        self.indicator = indicator
        self.default = default

        super().__init__(name)

    def prompt(self):
        index = 0
        if isinstance(self.options, dict):
            if self.default:
                index = list(self.options.keys()).index(self.default)
            return self.options[
                pick(
                    list(self.options.keys()),
                    self.title,
                    self.indicator,
                    default_index=index,
                )[0]
            ]
        else:
            if self.default:
                index = self.options.index(self.default)
            return pick(self.options, self.title, self.indicator, default_index=index)[
                0
            ]


class Int(_Prompt):
    def __init__(self, name, validate=None, default=None) -> None:
        super().__init__(name, validate=validate, default=default)

    def parse(self, response):
        return int(response)


class Text(_Prompt):
    def __init__(self, name, validate=None, default=None) -> None:
        super().__init__(name, validate=validate, default=default)


class Date(_Prompt):
    def __init__(self, name, validate=None, default=None) -> None:
        super().__init__(name, validate=validate, default=default)

    def parse(self, response):
        date = dateparse(response)
        return date.strftime("%Y-%m-%d")


class Form:
    def __init__(self, prompts):
        self.prompts = prompts

    def execute(self):
        new = {}
        for key, prompt in self.prompts.items():
            new[key] = prompt.prompt()
        return new
