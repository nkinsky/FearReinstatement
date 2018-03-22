from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split, StratifiedKFold, permutation_test_score
from session_directory import load_session_list
import calcium_traces as ca_traces
import numpy as np
from matplotlib import pyplot as plt
import ff_video_fixer as FF
from mpl_toolkits.mplot3d import Axes3D
import data_preprocessing as d_pp
import calcium_events as ca_events
from scipy.stats import zscore
from random import randint

session_list = load_session_list()

def NB_session(session_index, bin_length=2, randomize=False):
    session = FF.load_session(session_index)

    # Get accepted neurons.
    traces, accepted, t = ca_traces.load_traces(session_index)
    # traces = ca_events.make_event_matrix(session_index)
    neurons = d_pp.filter_good_neurons(accepted)
    n_neurons = len(neurons)

    # Trim the traces to only include instances where mouse is in the chamber.
    t = d_pp.trim_session(t,session.mouse_in_cage)
    traces = d_pp.trim_session(traces,session.mouse_in_cage)
    n_samples = len(t)

    if randomize:
        for n,trace in enumerate(traces):
            traces[n,:] = np.roll(trace,randint(-n_samples,n_samples))

    samples_per_bin = bin_length * 20
    bins = d_pp.make_bins(t,samples_per_bin)
    n_samples = len(bins)+1

    X = np.zeros([n_samples,n_neurons])
    for n,this_neuron in enumerate(neurons):
        binned_activity = d_pp.bin_time_series(traces[this_neuron],bins)
        X[:, n] = [np.mean(chunk) for chunk in binned_activity]


    binned_freezing = d_pp.bin_time_series(session.imaging_freezing, bins)
    binned_freezing = [i.all() for i in binned_freezing]

    # Build train and test sets.
    X_train, X_test, y_train, y_test = train_test_split(X, binned_freezing,
                                                        test_size=0.2)
    classifier = make_pipeline(StandardScaler(), GaussianNB())
    classifier.fit(X_train, y_train)
    predict_test = classifier.predict(X_test)

    accuracy = metrics.accuracy_score(y_test, predict_test)

    return accuracy


    # lda = LinearDiscriminantAnalysis(solver='eigen',n_components=2,shrinkage='auto')
    # lda.fit(X,binned_freezing)
    # Y = lda.transform(X)


if __name__ == '__main__':
    n = 1
    accuracy = NB_session(n)
    shuffle_accuracy = []
    for i in np.arange(0,100):
        x = NB_session(n,randomize=True)
        shuffle_accuracy.append(x)

    pass