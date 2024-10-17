from pkg_resources import get_distribution


class BERClient(object):
    """Initialization method of the :code:`BERClient` class.

    Parameters
    ----------
    apikey : str
        API key to use.

    Returns
    -------
    Class
        BERClient Class
    """

    def __init__(self, **kwargs):
        __version__ = get_distribution("pyberdata").version

        kwargs.setdefault("output_format", "nested")
        self.interface = "api"
        self.platform = "python"
        self.apikey = kwargs["apikey"]

    from ._get_data import get_data
