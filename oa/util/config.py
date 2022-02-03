import logging
_logger = logging.getLogger(__name__)

import json
import os


class Config:
    """OPEN ASSISTANT CONFIGURATION"""

    def __init__(self, path=None, **opts):
        _logger.info("Loading Mind: {path}".format(path=path))

        # DIRECTORIES
        self.cache_dir = os.path.join(path, 'cache')
        self.conf_dir = os.path.join(path, 'conf')

        # CONFIGURATION FILES
        self.opt_file = os.path.join(self.conf_dir, "settings.json")
        self.cmd_file = os.path.join(self.conf_dir, "commands.json")

        # CACHE FILES
        self.history_file = os.path.join(self.cache_dir, "history")
        self.hash_file = os.path.join(self.cache_dir, "hash.json")

        self._make_dir(self.conf_dir)
        self._make_dir(self.cache_dir)

        self.options = self._read_options_file()
        self.options.update(opts)
        _logger.info("Options: {}".format(self.options))

        self.commands = self._read_commands_file()
        _logger.info("Command Count: {}".format(len(self.commands)))

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return repr({
            'cache_dir': self.cache_dir,
            'conf_dir': self.conf_dir,
            'options': self.options,
        })

    @staticmethod
    def _make_dir(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def _read_options_file(self):
        try:
            _logger.debug("Reading options from {}".format(self.opt_file))
            with open(self.opt_file, 'r') as f:
                _options = json.load(f)
                return _options
        except FileNotFoundError:
            # MAKE AN EMPTY OPTIONS NAMESPACE
            _logger.warn("Error reading options file: {path}".format(
                path=self.opt_file))
            return {}

    def _read_commands_file(self):
        try:
            _logger.debug("Reading commands from {}".format(self.cmd_file))
            with open(self.cmd_file, 'r') as f:
                _cmds = json.load(f)
                return _cmds
        except FileNotFoundError:
            # MAKE AN EMPTY COMMANDS NAMESPACE
            _logger.warn("Error reading commands file: {path}".format(
                path=self.cmd_file))
            return {}
