#!/usr/bin/env python
# -*- coding: utf-8 -*-

#             _
#            | |
#        __| |_ __ ___    __ _ _ __ ___    ___
#     / _` | "__/ _ \/ _` | "_ ` _ \/ __|
#    | (_| | | |    __/ (_| | | | | | \__ \
#     \__,_|_|    \___|\__,_|_| |_| |_|___/ .
#
# A "Fog Creek"–inspired demo by Kenneth Reitz™

import os
from flask import Flask, request, render_template, jsonify

import numpy as np
import tensorflow as tf

import lucid.modelzoo.vision_models as models
from lucid.misc.io import show, load
import lucid.optvis.render as render

import base64
import math
import time

model = models.InceptionV1()
model.load_graphdef()

# Support for gomix"s "front-end" and "back-end" UI.
app = Flask(__name__, static_folder="public", template_folder="views")


@app.route("/")
def homepage():
    """Displays the homepage."""
    return render_template("index.html")


@app.route("/test")
def runtestpage():
    """Displays the homepage."""
    return render_template("runtests.html")


@app.route("/judge_data_url", methods=["GET", "POST"])
def judgeDataUrl():
    # try:
        data_uri = request.values.get("dataURL")
        meta, data = data_uri.split(',')
        layer = request.values.get("layer")
        class_name = request.values.get("className")
        print('request', layer, class_name)

        # create temp file to send for processing
        url = "/tmp/curr.png"
        fh = open(url, "wb")
        fh.write(data.decode('base64'))
        fh.close()
        img = load(url)

        channel_attr = get_channel_attr(img, layer, class_name)

        # format the numbers
        channel_attr = map(f, channel_attr)

        return jsonify(channel_attr)

    # except:  # catch *all* exceptions
    #     return jsonify([])


def f(num):
    return float("{0:.8f}".format(num))


def score_f(logit, name):
    # print(model.labels
    if name is None:
        return 0
    elif name == "logsumexp":
        base = tf.reduce_max(logit)
        return base + tf.log(tf.reduce_sum(tf.exp(logit-base)))
    elif name in model.labels:
        return logit[model.labels.index(name)]
    else:
        raise RuntimeError("Unsupported")


def get_channel_attr(img, layer, class_name):
    ts0 = time.time()
    # Set up a graph for doing attribution...
    with tf.Graph().as_default(), tf.Session() as sess:
        t_input = tf.placeholder_with_default(img, [None, None, 3])
        T = render.import_model(model, t_input, t_input)

        ts1 = time.time()
        print('t1 ', (ts1 - ts0))
        # Compute activations
        acts = T(layer).eval()
        ts2 = time.time()
        print('t2 ', (ts2 - ts1))
        # Compute gradient
        logit = T("softmax2_pre_activation")[0]
        ts2b = time.time()
        print('t2b ', (ts2b - ts2))
        # score = score_f(logit, class_name) - score_f(logit, "cockroach")
        score = score_f(logit, class_name)
        tensor_layer = T(layer)
        t_grad = tf.gradients([score], [tensor_layer])[0]
        grad = t_grad.eval()
        ts3 = time.time()
        print('t3 ', (ts3 - ts2b))

        # Let"s do a very simple linear approximation attribution.
        # That is, we say the attribution of y to x is
        # the rate at which x changes y times the value of x.
        attr = (grad*acts)[0]
        ts4 = time.time()
        print('t4 ', (ts4 - ts3))

        # Then we reduce down to channels.
        channel_attr = attr.sum(0).sum(0)
        ts5 = time.time()
        print('t5 ', (ts5 - ts4))

        return channel_attr


if __name__ == "__main__":
    app.run()
