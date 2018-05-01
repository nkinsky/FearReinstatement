from cell_reg import load_cellreg_results, trim_match_map
import calcium_events as ca_events
import data_preprocessing as d_pp
import calcium_traces as ca_traces
import numpy as np
from session_directory import load_session_list
from helper_functions import ismember
import ff_video_fixer as ff

session_list = load_session_list()


def find_most_active(session_index, percentile):
    session = ff.load_session(session_index)
    events, _ = ca_events.load_events(session_index)
    events = d_pp.trim_session(events, session.mouse_in_cage)
    events = events > 0

    n_events = []
    for event in events:
        n_events.append(np.sum(event))

    threshold = np.percentile(n_events, percentile)

    neurons_above_threshold = [neuron for neuron, n
                               in enumerate(n_events)
                               if n >= threshold]

    return neurons_above_threshold


def find_most_active_overlap(session_1, session_2, percentile=50):
    mouse = session_list[session_1]["Animal"]

    assert mouse == session_list[session_2]["Animal"], \
        "Mouse names don't match!"

    s1_most_active = find_most_active(session_1, percentile)
    s2_most_active = find_most_active(session_2, percentile)

    match_map = load_cellreg_results(mouse)
    match_map = trim_match_map(match_map, [session_1, session_2])

    _, idx = ismember(match_map[:, 1], s2_most_active)
    s1_cells_active_on_s2 = match_map[idx, 0]
    s1_overlap_with_s2 = list(set(s1_cells_active_on_s2)
                              & set(s1_most_active))

    # Number of cells that were highly active on session 1 and also registered
    # to session 2.
    _, idx = ismember(match_map[:, 0], s1_most_active)
    n_cells = np.sum((match_map[idx, :] > -1).all(axis=1))

    n_overlap = len(s1_overlap_with_s2)
    percent_overlap = n_overlap / n_cells

    return percent_overlap


if __name__ == '__main__':
    percentile = 50
    p = []
    p.append(find_most_active_overlap(10, 11, percentile=percentile))
    p.append(find_most_active_overlap(10, 12, percentile=percentile))
    p.append(find_most_active_overlap(10, 14, percentile=percentile))

    pass