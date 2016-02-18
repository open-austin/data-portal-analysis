import ConfigParser

class ConfigHelper(object):
    """class ConfigHelper()
    Reads configuration vales from a file, or returns defaults
    """
    def __init__(self, configfile):
        """Initializes a config helper using a specified file,
           or fall back to defaults
        """
        self.views_url = ''
        self.migrations_url = ''
        self.request_url = ''
        self.log_file = ''
        if configfile:
            self._parse_config(configfile)
        self._load_defaults()

    def _load_defaults(self):
        """Offers fallbacks in case certain settings aren't found in config"""
        self.views_url = self.views_url or "http://data.austintexas.gov/api/search/views.json"
        self.migrations_url = self.migrations_url or "http://data.austintexas.gov/api/migrations/"
        self.request_url = self.request_url or "http://data.austintexas.gov/api/views/"
        self.log_file = self.log_file or "portal_analyzer.log"

    def _parse_config(self, configfile):
        """Parses provided config file for values"""
        config = ConfigParser.ConfigParser()
        config.read(configfile)

        try:
            self.views_url = config.get('Urls', 'views_url')
            self.migrations_url = config.get('Urls', 'migrations_url')
            self.request_url = config.get('Urls', 'request_url')
            self.log_file = config.get('Logs', 'logfile')
        except ConfigParser.NoOptionError as e:
            print "Config Warning: {0}".format(e.strerror)