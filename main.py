from icecream import ic
from app import Logger
from valuer import ValuerApp


def main() -> None:
    app = ValuerApp()
    app.run()


if __name__ == "__main__":
    ic.configureOutput(prefix=Logger.info,
                       outputFunction=Logger.write_log)
    Logger.clear_file_not_found()
    Logger.clear()
    main()
