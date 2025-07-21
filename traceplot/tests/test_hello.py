from src.traceplot.helpers import greet
from src.traceplot import hello
import pytest


def test_greeting() -> None:
	assert greet.greetme() == "greeted"

def test_hello() -> None:
	assert hello() == "Hello from traceplot!"
