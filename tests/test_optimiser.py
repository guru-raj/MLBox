#!/usr/bin/env python
# coding: utf-8
# Author: Axel ARONIO DE ROMBLAY <axelderomblay@gmail.com>
# License: BSD 3 clause
import pytest
import pandas as pd
import numpy as np

from mlbox.optimisation.optimiser import Optimiser
from mlbox.preprocessing.drift_thresholder import Drift_thresholder
from mlbox.preprocessing.reader import Reader


def test_init_optimiser():
    with pytest.warns(UserWarning) as record:
        optimiser = Optimiser()
    assert len(record) == 1
    assert not optimiser.scoring
    assert optimiser.n_folds == 2
    assert optimiser.random_state == 1
    assert optimiser.to_path == "save"
    assert optimiser.verbose


def test_get_params_optimiser():
    with pytest.warns(UserWarning) as record:
        optimiser = Optimiser()
    assert len(record) == 1
    dict = {'scoring': None,
            'n_folds': 2,
            'random_state': 1,
            'to_path': "save",
            'verbose': True}
    assert optimiser.get_params() == dict


def test_set_params_optimiser():
    with pytest.warns(UserWarning) as record:
        optimiser = Optimiser()
    assert len(record) == 1
    optimiser.set_params(scoring='accuracy')
    assert optimiser.scoring == 'accuracy'
    optimiser.set_params(n_folds=3)
    assert optimiser.n_folds == 3
    optimiser.set_params(random_state=2)
    assert optimiser.random_state == 2
    optimiser.set_params(to_path="name")
    assert optimiser.to_path == "name"
    optimiser.set_params(verbose=False)
    assert not optimiser.verbose
    with pytest.warns(UserWarning) as record:
        optimiser.set_params(wrong_key=3)
    assert len(record) == 1


def test_evaluate_and_optimise():
    reader = Reader(sep=",")
    dict = reader.train_test_split(Lpath=["data_for_tests/train.csv",
                                          "data_for_tests/test.csv"],
                                   target_name="Survived")
    drift_thresholder = Drift_thresholder()
    drift_thresholder = drift_thresholder.fit_transform(dict)

    with pytest.warns(UserWarning) as record:
        opt = Optimiser(scoring='accuracy', n_folds=3)
    assert len(record) == 1
    score = opt.evaluate(None, dict)
    assert np.round(score, 6) == 0.784512

    space = {'ne__numerical_strategy': {"search": "choice", "space": [0]},
             'ce__strategy': {"search": "choice",
                              "space": ["label_encoding",
                                        "random_projection",
                                        "entity_embedding"]},
             'fs__threshold': {"search": "uniform",
                               "space": [0.01, 0.3]},
             'est__max_depth': {"search": "choice",
                                "space": [3, 4, 5, 6, 7]}

             }

    best = opt.optimise(space, dict, 1)
    assert type(best) == type(dict)