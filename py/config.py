
import ConfigParser

defaults = {
    'hrsehome': '/home/hrseweb/hrse'
}

defpath = defaults['hrsehome']+'/etc/hrse.conf'
section = 'options'


class Config:
    """Initialize a Config class.

    If path is not provided, then we will use the default path, defpath, as
    the path to the configuration file.  If the file is unreadable, an
    exception will be raised.  Any values that are not present in the file
    will take on their default values.

    """
    def __init__(self, path=None):
        self.conf = ConfigParser.SafeConfigParser(defaults)

        if path is None:
            path = defpath

        p = self.conf.read(path)
        if len(p) == 0:
            raise IOError, "Cannot open the configuration file, '"+path+"'."

        if not self.conf.has_section(section):
            raise IOError, "Cannot locate the '"+section+"' section in the configuration file '"+path+"'."

    def get(self, attr):
        """Retrieve the given attribute's value from the working config."""
        return self.conf.get(section, attr)


def get(attr):
    """Retrieve the given attribute's value from the configuration."""
    return Config().get(attr)

