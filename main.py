from icecream import ic
from app import Logger, ValuerApp
from app.handlers import MainFileHandler


def main() -> None:
    app = ValuerApp()
    app.run()


if __name__ == "__main__":
    ic.configureOutput(prefix=Logger.info,
                       outputFunction=Logger.write_log)
    main()
