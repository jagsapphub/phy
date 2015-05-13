# -*- coding: utf-8 -*-

"""Tests of view model."""

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

# import numpy as np
from pytest import mark

from ....utils.logging import set_level, debug
from ....utils.testing import (show_test_start,
                               show_test_stop,
                               show_test_run,
                               )
from ....io.mock import MockModel
# from ..clustering import Clustering
from ..kwik import (WaveformViewModel,
                    FeatureViewModel,
                    CorrelogramViewModel,
                    TraceViewModel,
                    )


# Skip these tests in "make test-quick".
pytestmark = mark.long()


#------------------------------------------------------------------------------
# View model tests
#------------------------------------------------------------------------------

_N_FRAMES = 2


def setup():
    set_level('info')


def _test_empty(view_model_class, stop=True, **kwargs):

    model = MockModel(n_spikes=1, n_clusters=1)

    vm = view_model_class(model, **kwargs)
    vm.on_open()
    vm.on_select([0])

    # Show the view.
    show_test_start(vm.view)
    show_test_run(vm.view, _N_FRAMES)

    if stop:
        show_test_stop(vm.view)

    return vm


def _test_view_model(view_model_class, stop=True, do_cluster=False, **kwargs):

    model = MockModel()
    # clustering = Clustering(model.spike_clusters)

    clusters = [3, 4]
    # spikes = clustering.spikes_in_clusters(clusters)

    vm = view_model_class(model, **kwargs)
    vm.on_open()
    vm.on_select(clusters)

    # Show the view.
    show_test_start(vm.view)
    show_test_run(vm.view, _N_FRAMES)

    if do_cluster:
        # Merge the clusters and update the view.
        debug("Merging.")
        # up = clustering.merge(clusters)
        # vm.on_select(up.added)
        # show_test_run(vm.view, _N_FRAMES)

        # # Split some spikes and update the view.
        # debug("Splitting.")
        # spikes = spikes[::2]
        # up = clustering.assign(spikes, np.random.randint(low=0, high=5,
        #                                                  size=len(spikes)))
        # vm.on_select(up.added)
        # show_test_run(vm.view, _N_FRAMES)

    if stop:
        show_test_stop(vm.view)

    return vm


def test_waveforms_full():
    _test_view_model(WaveformViewModel)


def test_waveforms_empty():
    _test_empty(WaveformViewModel)


def test_features_full():
    _test_view_model(FeatureViewModel)


def test_features_lasso():
    vm = _test_view_model(FeatureViewModel,
                          stop=False,
                          do_cluster=False,
                          )
    show_test_run(vm.view, _N_FRAMES)
    vm.view.lasso.box = 1, 2
    vm.view.lasso.add((0, 0))
    vm.view.lasso.add((1, 0))
    vm.view.lasso.add((1, 1))
    vm.view.lasso.add((0, 1))
    show_test_run(vm.view, _N_FRAMES)
    # spikes = vm.spikes_in_lasso()
    # clustering = Clustering(vm.model.spike_clusters)
    # up = clustering.split(spikes)
    # vm.on_select(up.added)
    show_test_run(vm.view, _N_FRAMES)
    show_test_stop(vm.view)


def test_features_empty():
    _test_empty(FeatureViewModel)


def test_ccg_full():
    vm = _test_view_model(CorrelogramViewModel,
                          binsize=20,
                          winsize_bins=51,
                          n_excerpts=100,
                          excerpt_size=100,
                          stop=False,
                          )
    show_test_run(vm.view, _N_FRAMES)
    vm.change_bins(half_width=100., bin=1.)
    show_test_run(vm.view, _N_FRAMES)
    show_test_stop(vm.view)


def test_ccg_empty():
    _test_empty(CorrelogramViewModel,
                binsize=20,
                winsize_bins=51,
                n_excerpts=100,
                excerpt_size=100,
                )


def test_traces():
    vm = _test_view_model(TraceViewModel, stop=False)
    vm.move_right()
    show_test_run(vm.view, _N_FRAMES)
    vm.move_left()
    show_test_run(vm.view, _N_FRAMES)

    show_test_stop(vm.view)