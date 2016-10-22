import logging
import migrate
import pkg_resources

# Module version (PEP-0396).
#__version__ = pkg_resources.get_distribution(__package__).version


API_VERSION = '0.1'


def main():
    setup = migrate.DacService()
    setup.create()
    pass


if __name__ == "__main__":
    main()
