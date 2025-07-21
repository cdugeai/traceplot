from traceplot import hello
from traceplot.helpers import greet


def main():
    print("Hello from examples!")
    greet.greetme()
    print(hello())


if __name__ == "__main__":
    main()
