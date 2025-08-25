def passthrough(data, params=None):
    """Return input data unchanged."""
    return data


PROCESSING_FUNCTIONS = {
    'passthrough': passthrough
}