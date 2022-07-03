#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests for base gnn"""

import unittest

import numpy as np
from sknetwork.data.test_graphs import test_graph
from sknetwork.gnn.gnn_classifier import GNNClassifier
from sknetwork.gnn.base import BaseGNNClassifier


class TestBaseGNN(unittest.TestCase):

    def setUp(self) -> None:
        """Test graph for tests."""
        self.adjacency = test_graph()
        self.n = self.adjacency.shape[0]
        self.features = self.adjacency
        self.labels = np.array([0]*5 + [1]*5)

    def test_base_gnn_fit(self):
        gnn = BaseGNNClassifier()
        with self.assertRaises(NotImplementedError):
            gnn.fit(self.adjacency, self.features, self.labels, test_size=0.2)

    def test_base_gnn_fit_transform(self):
        gnn = GNNClassifier(layer='GCNConv', n_hidden=2, activation='Relu', optimizer='None', verbose=False)
        embedding = gnn.fit_transform(self.adjacency, self.features, labels=self.labels, max_iter=1, val_size=0.2)
        self.assertTrue(len(embedding) == self.n)
        self.assertTrue(embedding.shape == (self.n, 2))

    def test_base_gnn_custom(self):
        gnn = GNNClassifier(layer=['GCNConv', 'GCNConv', 'GCNConv'], n_hidden=[20, 8, 2],
                            activation=['Relu', 'Sigmoid', 'Softmax'], optimizer='Adam', verbose=False)
        self.assertTrue(isinstance(gnn, GNNClassifier))
        self.assertTrue(gnn.conv3.activation == 'softmax')
        y_pred = gnn.fit_predict(self.adjacency, self.features, labels=self.labels, max_iter=1, val_size=0.2)
        self.assertTrue(len(y_pred) == self.n)

    def test_base_check_fitted(self):
        gnn = BaseGNNClassifier()
        with self.assertRaises(ValueError):
            gnn._check_fitted()
        gnn = GNNClassifier(layer='GCNConv', n_hidden=2, activation='Relu', optimizer='None', verbose=False)
        gnn.fit_transform(self.adjacency, self.features, labels=self.labels, max_iter=1, val_size=0.2)
        fit_gnn = gnn._check_fitted()
        self.assertTrue(isinstance(fit_gnn, GNNClassifier))
        self.assertTrue(fit_gnn.embedding_ is not None)

    def test_base_gnn_repr(self):
        gnn = GNNClassifier(layer=['GCNConv', 'GCNConv'], n_hidden=[8, 2],
                            activation=['Relu', 'Softmax'], optimizer='Adam')
        print(gnn)
        layers_str = "    GCNConv(out_channels: 8, activation: relu, use_bias: True, norm: both, self_loops: True)\n" \
                     "    GCNConv(out_channels: 2, activation: softmax, use_bias: True, norm: both, " \
                     "self_loops: True)"
        gnn_str = f"GNNClassifier(\n{layers_str}\n)"
        self.assertTrue(gnn.__repr__() == gnn_str)
