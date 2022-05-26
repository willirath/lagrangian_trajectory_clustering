def wrapped_metric(metric_function=None, sequences_mapping=None, normalize=False):
    """Decorator for wrapped metric.
    
    Parameters
    ----------
    metric_function: function
        An edit-distance like metric function.
    sequences: list
        Will be used to look up sequences.
    normalize: book
        If set to True, the resulting metric will be normalized
        with the length of the longer sequence.
        Defaults to False.
    
    Returns
    -------
    function
        Wrapped metric accepting two arguments x and y.
    
    """
    if normalize:

        def _wrapped_metric(x, y):
            i = int(x[0])
            j = int(y[0])
            s0 = sequences_mapping[i]
            s1 = sequences_mapping[j]
            max_len = max(len(s0), len(s1))
            return metric_function(s0, s1) / max_len

    else:

        def _wrapped_metric(x, y):
            i = int(x[0])
            j = int(y[0])
            s0 = sequences_mapping[i]
            s1 = sequences_mapping[j]
            return metric_function(s0, s1)

    return _wrapped_metric

