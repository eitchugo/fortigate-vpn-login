# -*- coding: utf-8 -*-
"""
    fortigate_vpn_login.config
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Configuration
"""
import os
import configparser
from typing import Optional
from pathlib import Path
from fortigate_vpn_login import utils, logger


class Config(object):
    """
    Represents a configuration.

    Params:
        CONFIG (dict): configuration defaults. These will be loaded if no other value
            is defined for each key. For example, if the class is instanced without
            any arguments, `self.openconnect_pid_filename` will receive the value from
            this parameter.

            Also note that any configuration option **has** to be in this CONFIG parameter,
            otherwise we don't recognize it as a valid option and will discard it.
    """

    CONFIG = {
        'debug_mode': "False",
        'quiet_mode': "True",
        'config_filename': utils.get_default_config_filepath() / 'config.ini',
        'openconnect_pid_filename': '/var/run/openconnect.pid',
        'forti_url': ""
    }

    def __init__(self, name: Optional[str] = None, **kwargs: str) -> None:
        """
        Creates a new configuration based on defaults or keyword arguments
        passed to the class. If one or more keyword arguments are passed, these
        will be copied into the class self variables.

        Only configuration options found on the `CONFIG` class parameter can
        be loaded. Any other configuration will be considered invalid and discarded.

        Args:
            name (Optional|str): an indentifier for the configuration, in
                case there are multiples instances of it.
        """
        self.name = name or self.__class__.__name__.lower()
        logger.debug(f"Initializing configuration ({self.name})")
        self.config = configparser.ConfigParser()

        # set defaults
        logger.debug('Setting configuration defaults:')
        logger.debug(self.CONFIG)
        self.config['main'] = self.CONFIG

        # read from config file
        try:
            self.config_filename = kwargs['config_filename']
        except KeyError:
            self.config_filename = self.CONFIG['config_filename']

        self.load()

        # set from instancing
        for key, value in kwargs.items():
            if key in self.CONFIG:
                logger.debug(f"Setting option from instance: {key}={value}")
                self.config['main'][key] = value

    def configure(self) -> None:
        """
        Interactively sets the configuration
        """
        while True:
            try:
                forti_url = self.get('forti_url')
                response = str(input(f"Fortigate VPN Server URL [{forti_url}]: "))
                if not response:
                    response = forti_url
                break
            except ValueError:
                print("ERROR: Input should be string only!")

        self.set('forti_url', response)

    def write(self, mkdir: bool = True) -> bool:
        """
        Persists the configuration into a file.

        Args:
            mkdir (bool): If True, recursively creates the path in which the
                file will be stored. The path is based on the instance variable
                `config_filename`. Defaults to `True`.

        Returns:
            bool: True if the save was successful. False if not.
        """
        try:
            logger.debug(f"Creating directories for file {self.config_filename}")
            os.makedirs(Path(self.config_filename).parent, mode=0o700, exist_ok=True)

            logger.debug(f"Writing configuration to file {self.config_filename}")
            with open(self.config_filename, 'w') as fp:
                self.config.write(fp)
            os.chmod(self.config_filename, 0o0600)
        except Exception as e:
            print(f"ERROR: Could not write to config file: {str(self.config_filename)}.")
            logger.debug(e)
            return False

        return True

    def save(self) -> bool:
        """
        Alias to write()` method.
        """
        return self.write()

    def load(self) -> bool:
        """
        Loads configuration from file.

        Returns:
            bool: True if load was successful. False if not.
        """
        logger.debug(f"Loading configuration file {self.config_filename}")
        self.config.read(self.config_filename)

    def has_option(self, option: str) -> bool:
        """
        Checks if an option is already present in the configuration. Option must be one in `CONFIG` class parameter.

        Returns:
            bool: True if it exists. False if not.
        """
        if option in self.CONFIG:
            return self.config.has_option('main', option)
        else:
            return False

    def get(self, option: str) -> Optional[str]:
        """
        Gets an option from the configuration. Option must be one in `CONFIG` class parameter.

        Returns:
            str|Optional: the option value
        """
        try:
            if option in self.CONFIG:
                return self.config.get('main', option)
            else:
                return None
        except configparser.NoOptionError:
            return None

    def getboolean(self, option: str) -> Optional[bool]:
        """
        Gets an option from the configuration, as a boolean. Option must be one in `CONFIG` class parameter.

        Returns:
            bool|Optional: the option boolean value
        """
        try:
            if option in self.CONFIG:
                return self.config.getboolean('main', option)
            else:
                return None
        except (configparser.NoOptionError, ValueError):
            return None

    def set(self, option: str, value: str) -> None:
        """
        Sets an option on the configuration. Option must be one in `CONFIG` class parameter.

        Args:
            option (str): option name
            value (str): option value
        """
        try:
            if option in self.CONFIG:
                self.config.set('main', option, value)
            else:
                return None
        except (configparser.NoSectionError, TypeError):
            return None

    def __getstate__(self) -> dict:
        """
        Gets the exact state of this configuration.

        Returns:
            dict: A dictionary with all items from this configuration.
        """
        return self.config['main'].items()

    def __setstate__(self, items: dict) -> None:
        """
        Sets a state for this configuration.

        Args:
            items (dict): a dictionary that will be copied to this configuration.
        """
        for key, value in items:
            if key in self.CONFIG:
                self.config['main'][key] = value

    def __repr__(self) -> str:
        return "%s(%s)" % (self.__class__.__name__, dict.__repr__(self))

    def __str__(self) -> str:
        """
        Returns a string representation of this configuration.

        Returns:
            str: configuration state
        """
        res = ["{}(name={!r}):".format(self.__class__.__name__, self.name)]
        res = res + [f"  {it[0]} = {it[1]}" for it in self.config['main'].items()]
        return "\n".join(res)
