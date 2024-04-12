from icecream import ic
from app import Logger


def main() -> None:
    ...


if __name__ == "__main__":
    ic.configureOutput(prefix=Logger.info,
                       outputFunction=Logger.write_log)
    main()
