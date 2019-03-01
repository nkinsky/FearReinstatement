import numpy as np
from itertools import groupby

def find_closest(array, value):
    value = float(value)
    idx = (np.abs(array - value)).argmin()

    return array[idx], idx


def ismember(A, B):
    """
    Returns an array containing logical True where data in A is found in B. Also returns
    indices in B for every value of A.
    """

    B_in_A = np.in1d(B, A)

    A = list(A)
    try:
        B_idx = np.zeros(len(B), dtype=int)
        for i,element in enumerate(B):
            try:
                B_idx[i] = int(A.index(element))
            except:
                B_idx[i] = 0
    except:
        B_idx = int(A.index(B))

    return B_in_A, B_idx


def find_dict_index(list, key, value):
    idx = []
    for i, dic in enumerate(list):
        if dic[key] == value:
            idx.append(i)

    return idx


def shift_rows(data):
    n_rows, n_cols = data.shape
    max_shift = n_cols - 1

    col_start = np.random.randint(0, max_shift, n_rows)

    idx = np.mod(col_start[:,None] + np.arange(n_cols), n_cols)

    out = data[np.arange(n_rows)[:,None], idx]

    return out


def get_longest_run(list):
    length = max(sum(1 for _ in items) for val, items
        in groupby(list) if val)

    return length


def get_event_rate(events):
    assert np.max(events) <= 1, 'Binarize input first.'

    # Duration in seconds.
    if events.ndim == 1:
        duration = len(events) / 20
        event_rate = np.sum(events)
    elif events.ndim == 2:
        duration = events.shape[1] / 20
        event_rate = np.sum(events, axis=1)
    else:
        raise ValueError('Unknown operation.')

    event_rate = event_rate / duration

    return event_rate


def get_true_epochs(bool_in):
    padded_bool = np.concatenate(([False], bool_in, [False]))
    status_changes = np.abs(np.diff(padded_bool))

    # Find where freezing begins and ends.
    true_epochs = np.where(status_changes == 1)[0].reshape(-1, 2)

    # freezing_epochs[freezing_epochs >= self.video_t.shape[0]] = \
    #     self.video_t.shape[0] - 1

    # Only take the middle.
    true_epochs = true_epochs[1:-1]

    return true_epochs
