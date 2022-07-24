from plotnine.labels import labs


class zlab(labs):
    """
    Create z-axis label
    Parameters
    ----------
    zlab : str
        z-axis label
    """

    def __init__(self, zlab):
        if zlab is None:
            raise PlotnineError(
                "Arguments to zlab cannot be None")
        self.labels = {'z': zlab}
