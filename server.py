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
import numpy as np

# import matplotlib.pyplot as plt

model = models.InceptionV1()
model.load_graphdef()

canon = []
canon = [-0.035, -0.148, -0.097, 0.302, -0.283, 1.417, 0.095, 0.206, -0.118, 0.477, 0.037, 0.008, -0.134, -0.144, 0.418, 1.444, 0.031, -0.273, -0.194, 0.026, -0.102, 0.438, -0.002, 0.032, 0.719, -0.685, 0.037, -0.106, 0.236, -0.246, 0.14, 0.174, 1.054, 0.03, 0.45, -0.28, 0.002, 0.17, 0.901, -0.143, -0.421, -0.025, -0.199, -0.01, -0.408, 0.015, -0.061, -0.163, -0.002, -0.083, -0.214, 0.26, -0.286, -0.065, -0.345, -0.052, -0.077, 0.008, -0.077, 0.014, -0.42, -0.204, 0.076, -0.183, -0.027, 0.944, 0.306, -0.353, 0.325, -0.05, 0.571, 0.059, 0.351, 0.269, 0.378, -0.017, 0.476, 0.031, -0.254, -0.521, -0.075, -0.194, 0.408, 0.196, 0.313, 0.004, -0.169, 0.004, 0.01, 0.202, 0.491, -0.221, 0.098, -0.019, 0.005, -0.028, 0.171, 0.311, 0.131, -0.028, -0.423, 0.097, 0.097, -0.017, -0.069, -0.077, -0.053, 0.04, 0.076, -0.048, -0.182, 0.325, -0.304, 0.01, -0.174, -0.017, 0.012, -0.438, 0.06, 0.023, 0.052, 0.225, 0.006, -0.439, -0.116, -0.022, -0.093, 0.377, 0.018, 0.014, -0.234, -0.143, 0.088, 0.043, 0.158, 0.108, 0.176, 0.063, -0.011, -0.043, -0.064, -0.041, 0.006, -0.088, -0.12, -0.058, -0.048, 0.003, 0.119, 0.032, 0.038, 0.094, -0.011, -0.081, 0.0, -0.01, 0.049, 0.063, -0.072, 0.045, 0.335, 0.143, -0.03, 0.31, 0.337, -0.203, 0.291, -0.005, 0.016, -0.032, 0.293, -0.271, 0.242, 0.041, -0.169, 0.015, -0.052, 0.474, -0.077, -0.074, 0.056, -0.153, 0.093, 0.083, 0.018, -0.104, 0.004, 0.006, -0.031, 0.038, 0.002, -0.015, -0.279, -0.131, 0.272, -0.007, 0.058, -0.082, -0.126, 0.135, -0.026, 0.148, 0.158, 0.03, -0.04, -0.053, -0.025, 0.019, 0.097, 0.031, -0.072, -0.106, -0.075, -0.152, 0.164, 0.521, -0.481, -0.03, -0.052, 0.009, 0.006, 0.013, 0.002, 0.358, 0.406, -0.054, 0.026, -0.022, 0.011, 0.165, 0.045, 0.13, 0.006, 0.155, -0.034, 0.11, -0.017, -0.105, 0.1, -0.048, 0.052, 0.004, -0.122, 0.006, -0.033, -0.301, 0.141, 0.053, 0.025, -0.036, -0.01, 0.537, 0.035, -0.012, 0.017, -0.079, -0.187, -0.038, -0.32, 0.26, -0.033, -0.001, 0.297, -0.0, 0.872, -0.0, 0.028, 0.212, 0.056, -0.018, 0.009, 0.007, -0.02, -0.316, 0.103, 0.112, 0.01, 0.032, -0.063, 0.087, -0.098, -0.006, -0.013, 0.177, -0.038, -0.096, -0.03, 0.226, -0.027, -0.268, 0.021, 0.18, 0.056, 0.42, -0.095, -0.126, 0.008, 0.052, 0.201, -0.038, -0.198, 0.047, -0.037, 0.05, -0.079, -0.087, 0.268, -0.053, -0.008, 0.315, 0.07, -0.08, 0.178, 0.013, -0.119, 0.059, -0.022, -0.035, 0.058, 0.012, 0.11, 0.126, 0.149, 0.033, 0.094, 0.306, -0.076, -0.087, -0.119, -0.086, -0.018, 0.013, -0.025, 0.0, -0.057, 0.086, 0.137, 0.036, -0.037, 0.04, 0.009, -0.004, -0.045, -0.664, 0.111, 0.168, -0.265, -0.011, 0.05, 0.005, -0.117, 0.097, -0.104, 0.013, -0.128, 0.115, 0.121, 0.283, -0.175, -0.043, -0.073, 0.144, 0.095, -0.312, 0.151, 0.03, 0.072, 0.267, 0.008, 0.019, 0.002, -0.043, 0.125, -0.298, 0.028, 0.132, 0.142, -0.136, -0.052, 0.043, -0.03, -0.052, -0.099, 0.062, -0.092, 0.121, 0.077, -0.116, 0.062, 0.06, 0.212, -0.278, -0.013, -0.031, -0.096, 0.017, 0.089, 0.016, -0.153, -0.061, 0.068, -0.033, -0.074, -0.025, 0.009, 0.034, 0.133, 0.153, 0.002, -0.042, -0.163, 0.014, -0.223, -0.041, -0.034, -0.069, 0.038, -0.006, 0.092, -0.016, -0.005, 0.108, -0.045, 0.017, -0.071, 0.065, 0.061, 0.063, 0.084, -0.119, 0.043, -0.022, 0.011, -0.441, -0.102, 0.04, -0.045, 0.032, 0.079, -0.09, -0.183, 0.087, 0.007, 0.238, -0.06, -0.003, 0.191, -0.001, -0.02, 0.002, -0.009, 0.26, 0.096, 0.093, 0.004, -0.163, -0.059, 0.004, -0.085, -0.219, -0.198, 0.0, 0.168, -0.016, -0.062, 0.053, 0.021, 0.11, 0.225, -0.005, 0.241, -0.165, 0.133, -0.009, 0.018, 0.192, -0.007, 0.005, -0.024, -0.116, 0.294, 0.031, 0.022, -0.747, 0.11, -0.102, -0.036, -0.009, -0.002, 0.024, -0.041, 0.038, 0.056, 0.047, -0.087, -0.033, 0.279, -0.113, -0.011, 0.023, 0.002, 0.015, 0.009, -0.001, -0.046, -0.036, 0.798, -0.11, 0.042, -0.002, 0.049, -0.014]
# canon = [(83, 0.3608406186103821), (21, 0.6859855055809021), (472, 0.5928131937980652), (73, 0.35273274779319763), (79, 0.07347352802753448), (137, 0.1606243997812271), (24, 0.3085823655128479), (262, 0.6414108276367188), (38, 0.5003306269645691), (65, 0.32130348682403564), (11, 0.004320118110626936), (242, 0.059146683663129807), (177, 0.20023991167545319), (215, 0.6726974844932556), (506, 0.6906414031982422), (18, 0.6846585273742676), (15, 0.7115497589111328), (219, 0.28957152366638184), (76, 0.2330869436264038), (37, 0.2546364665031433), (160, 0.27863195538520813)]
# neuron_ids = [83, 21, 472, 73, 79, 137, 24]
# neuron_ids = [262, 38, 65, 11, 242, 177, 215]
# neuron_ids = [506, 18, 15, 219, 76, 37, 160]
# neuron_ids = [15, 506, 262, 23, 18, 343, 215, 109, 73, 114, 70, ]

eyes = [472, 24, 262, 38, 65, 11, 506, 18, 219, 76, 37]
snout = [83, 21, 472, 73, 79, 24, 262, 38, 65, 11, 506, 76, 37, 160]
legs = [435, 5, 137, 242, 177, 215]
ears = [15]
ears_4D = [11, 167, 50, 436, 100, 81, 104]  # 436, 11, maybe 100
legs_4D = [121, 428, 391, 325, 421, 328, 422]  # 428, 422 look good
snout_4D = [308, 453, 477, 436, 81, 230, 374]  # 477, maybe 374, 308
# neuron_ids = [15, 215, 21]  # ears, legs, snout?
# neuron_ids = [5, 293, 51, 90, 107, 109, 9, 198, 417]  # ears, legs, snout?

ears_n = [436, 11, 100]
legs_n = [428, 422]
snout_n = [477, 374, 308]

# neuron_ids = [472, 24, 262, 38, 65, 11, 1, 2, 3, 4, 5]
# neuron_ids = [i for i in range(528)]
neuron_ids = ears_n + legs_n + snout_n


# fur (5, 0.8828659057617188),
# fur (435, 0.4943612813949585),

ra_window = 10
baseline_threshold = 0.7
class_name = "Labrador retriever"
local_file_path = "file:///Users/erikulberg/Desktop/mlchat"


data_file = open("data.txt", "w")


class NeuronData:
    def __init__(self, idx):
        self.idx = idx
        self.running_avg = 0
        self.mse = float('inf')
        self.baseline = None
        self.baseline_history = []
        self.locked = False
        self.history = []
        self.ra_history = []
        self.var = 0

    def update(self, attr, canon_attr):
        self.history.append(attr)

        # update running avg based on window of history
        if len(self.history) >= ra_window:
            self.running_avg = sum(self.history[-ra_window:]) / float(ra_window)
        else:
            self.running_avg = sum(self.history) / float(len(self.history))

        self.mse = self.running_avg
        # self.mse = (canon_attr - self.running_avg) ** 2
        # start checking baselines after window filled
        # baseline is used for looking for significant changes
        # if len(self.history) >= ra_window:
        #     self.ra_history.append(self.running_avg)
        #     self.var = abs(np.var(self.ra_history) / np.amax(self.ra_history))
        #     if self.baseline is None:
        #         self.baseline = self.mse * baseline_threshold
        #     elif self.mse < self.baseline:
        #         # looks like there was a change!
        #         self.locked = True
        #         self.baseline_history.append(self.baseline)
        #         self.baseline = self.mse * baseline_threshold
            # elif self.locked:  # remove lock
            #     original_baseline = self.baseline_history[0]
            #     improvement = original_baseline - self.mse
            #     if improvement < 0:
            #         self.locked = False


neuron_data_map = dict([(idx, NeuronData(idx)) for idx in neuron_ids])


# Support for gomix"s "front-end" and "back-end" UI.
app = Flask(__name__, static_folder="public", template_folder="views")


@app.route("/")
def homepage():
    """Displays the homepage."""
    return render_template("index.html")


@app.route("/test2")
def testpage():
    """Displays the homepage."""
    return render_template("test2.html")


@app.route("/test")
def runtestpage():
    """Displays the homepage."""
    return render_template("runtests.html")


def update_neuron_history(channel_attr):
    for i, idx in enumerate(neuron_ids):
        attr = channel_attr[idx]
        # canon_attr = canon[idx]
        canon_attr = None
        neuron_data = neuron_data_map[idx]
        neuron_data.update(attr, canon_attr)


def total_diff():
    total = 0
    for i, idx in enumerate(neuron_ids):
        neuron_data = neuron_data_map[idx]
        total += neuron_data.mse

    print "total diff: ", total


def get_neuron_suggestions():
    suggestions = []
    for i, idx in enumerate(neuron_ids):
        neuron_data = neuron_data_map[idx]
        if not neuron_data.locked:
            suggestions.append((idx, neuron_data.mse))

    suggestions.sort(key=lambda x: x[1], reverse=True)

    return suggestions


def get_neuron_improvements():
    improvements = []
    for i, idx in enumerate(neuron_ids):
        neuron_data = neuron_data_map[idx]
        if neuron_data.locked:
            original_baseline = neuron_data.baseline_history[0]
            recent_baseline = neuron_data.baseline_history[-1]
            improvement = original_baseline - neuron_data.mse
            recent_imp = recent_baseline - neuron_data.mse
            improvements.append((idx, [int(neuron_data.mse * 100000), int(improvement * 100000)]))
            # improvements.append((idx, [int(neuron_data.mse * 100000), int(improvement * 100000), int(neuron_data.var * 100000)]))

    improvements.sort(key=lambda x: x[1][1], reverse=True)

    return improvements


def get_neuron_improvement_history():
    improvement_history = []
    for i, idx in enumerate(neuron_ids):
        neuron_data = neuron_data_map[idx]
        if neuron_data.locked:
            improvement_history.append((idx, neuron_data.baseline_history))

    return dict(improvement_history)


def score_f(logit, name):
    # print model.labels
    if name is None:
        return 0
    elif name == "logsumexp":
        base = tf.reduce_max(logit)
        return base + tf.log(tf.reduce_sum(tf.exp(logit-base)))
    elif name in model.labels:
        return logit[model.labels.index(name)]
    else:
        raise RuntimeError("Unsupported")

attr_hist = dict([idx, []] for idx in neuron_ids)
hist_window = 20
hist_window_short = 5
act_id = 15

def get_channel_attr(img, layer):
    # Set up a graph for doing attribution...
    with tf.Graph().as_default(), tf.Session() as sess:
        t_input = tf.placeholder_with_default(img, [None, None, 3])
        T = render.import_model(model, t_input, t_input)

        # Compute activations
        acts = T(layer).eval()

        # Compute gradient
        logit = T("softmax2_pre_activation")[0]
        # score = score_f(logit, class_name) - score_f(logit, "cockroach")
        score = score_f(logit, class_name)
        t_grad = tf.gradients([score], [T(layer)])[0]
        grad = t_grad.eval()

        # Let"s do a very simple linear approximation attribution.
        # That is, we say the attribution of y to x is
        # the rate at which x changes y times the value of x.
        attr = (grad*acts)[0]

        # Then we reduce down to channels.
        channel_attr = attr.sum(0).sum(0)

        print "what is going on?", neuron_ids
        data_arr = ""
        for idx in neuron_ids:
            print idx
            neuron_attr = channel_attr[idx]
            neuron_attr_hist = attr_hist[idx]
            neuron_attr_hist.append(neuron_attr)

            if len(neuron_attr_hist) >= hist_window_short:
                ra_attr_s = sum(neuron_attr_hist[-hist_window_short:]) / hist_window_short
            else:
                ra_attr_s = sum(neuron_attr_hist) / len(neuron_attr_hist)

            if len(neuron_attr_hist) >= hist_window:
                ra_attr = sum(neuron_attr_hist[-hist_window:]) / hist_window
            else:
                ra_attr = sum(neuron_attr_hist) / len(neuron_attr_hist)

            data_arr += str(idx) + ',' + str(neuron_attr) + ',' + str(ra_attr_s) + ',' + str(ra_attr) + '/'

        print data_arr

        # attr_hist.append(channel_attr[act_id])
        # if len(attr_hist) >= hist_window:
        #     ra_attr = sum(attr_hist[-hist_window:]) / hist_window
        # else:
        #     ra_attr = sum(attr_hist) / len(attr_hist)

        # if len(attr_hist) >= hist_window_short:
        #     ra_attr_s = sum(attr_hist[-hist_window_short:]) / hist_window_short
        # else:
        #     ra_attr_s = sum(attr_hist) / len(attr_hist)
        # act_hist.append(acts[0].sum(0).sum(0)[act_id])
        # if len(act_hist) >= hist_window:
        #     ra_act = sum(act_hist[-hist_window:]) / hist_window
        # else:
        #     ra_act = sum(act_hist) / len(act_hist)
        # if len(act_hist) >= hist_window_short:
        #     ra_act_s = sum(act_hist[-hist_window_short:]) / hist_window_short
        # else:
        #     ra_act_s = sum(act_hist) / len(act_hist)
        # print 'ra_act: ', f(ra_act), ', ra_attr: ', f(ra_attr)
        # print 'ra_act_s: ', f(ra_act_s), ', ra_attr_s: ', f(ra_attr_s)
        # print 'act', f(act_hist[-1]), ', attr:', f(attr_hist[-1])
        # print ''
        # data_arr = str(f(act_hist[-1])) + ',' + str(f(ra_act_s)) + ',' + str(f(ra_act)) + ',' + str(f(attr_hist[-1])) + ',' + str(f(ra_attr_s)) + ',' + str(f(ra_attr))
        data_file.write(data_arr + '\n')
        # record_data(len(attr_hist), f(ra_attr_s))

    return channel_attr


def f(num):
    return float("{0:.3f}".format(num))


def processJSON(idxAttr):
    processed = []
    for p in idxAttr:
        idx, attr = p
        processed.append((idx, int(attr * 100000)))

    return processed


# Judge an image and return the differences with the canon
@app.route("/judge", methods=["GET", "POST"])
def judge():
    img_url = local_file_path + request.values.get("url")
    layer = request.values.get("layer")
    print "judge ", img_url, " for ", layer

    img = load(img_url)
    channel_attr = get_channel_attr(img, layer)
    update_neuron_history(channel_attr)
    suggestions = get_neuron_suggestions()

    return jsonify(processJSON(suggestions))


@app.route("/judge_data_url", methods=["GET", "POST"])
def judgeDataUrl():
    try:
        data_uri = request.values.get("dataURL")
        meta, data = data_uri.split(',')

        # create temp file to send for processing
        url = "/tmp/curr.png"
        fh = open(url, "wb")
        fh.write(data.decode('base64'))
        fh.close()
        img = load(url)
        layer = request.values.get("layer")

        # print "realtime processing for", layer
        channel_attr = get_channel_attr(img, layer)
        update_neuron_history(channel_attr)
        # total_diff()

        # print "ra_history 15 ", neuron_data_map[15].ra_history
        # print "ra_history 215 ", neuron_data_map[215].ra_history
        # hist = get_neuron_improvement_history()
        # if 15 in hist:
        #     print "baseline history: ", hist[15]

        # get the neurons with the biggest diff that are not locked
        suggestions = get_neuron_suggestions()
        # print 'suggestions', suggestions

        improvements = get_neuron_improvements()

        return jsonify(processJSON(suggestions), improvements)

    except:  # catch *all* exceptions
        return jsonify([])


@app.route("/intent/add_all", methods=["POST"])
def addIntents():
    global canon
    global neuron_data_map

    urlsAll = request.values.get("urls")
    urls = urlsAll.split(',')
    layer = request.values.get("layer")
    print "add intents from ", urls, " for ", layer

    channel_attr_all = []
    count = 0
    for url in urls:
        img_url = local_file_path + url
        print "processing: ", img_url
        img = load(img_url)
        channel_attr = get_channel_attr(img, layer)

        if len(channel_attr_all) == 0:
            for i, attr in enumerate(channel_attr):
                channel_attr_all.append(attr)
        else:
            for i, attr in enumerate(channel_attr):
                channel_attr_all[i] += attr

        count += 1

    canon = []
    idxAttr = []
    for i, attr in enumerate(channel_attr_all):
        avg_attr = attr / float(count)
        avg_attr = float("{0:.3f}".format(avg_attr))
        canon.append(avg_attr)
        idxAttr.append((i, avg_attr))

    neuron_data_map = dict([(idx, NeuronData(idx)) for idx in neuron_ids])

    print 'canon', canon
    idxAttr.sort(key=lambda x: x[1], reverse=True)
    return jsonify(processJSON(idxAttr))


# Get ready for live version
@app.route("/clear", methods=["POST"])
def clear():
    global neuron_data_map
    global ra_window
    # set the window to 1 for good measure
    ra_window = 6
    neuron_data_map = dict([(idx, NeuronData(idx)) for idx in neuron_ids])

    return jsonify([])


@app.route("/test/reset", methods=["POST"])
def test_reset():
    global neuron_data_map
    global ra_window
    # set the window to 1 for good measure
    ra_window = 1
    neuron_data_map = dict([(idx, NeuronData(idx)) for idx in neuron_ids])

    return jsonify([])


@app.route("/test/judge", methods=["POST"])
def test_judge():
    img_url = local_file_path + request.values.get("url")
    layer = request.values.get("layer")
    print "judge ", img_url, " for ", layer

    img = load(img_url)
    channel_attr = get_channel_attr(img, layer)
    update_neuron_history(channel_attr)
    suggestions = get_neuron_suggestions()
    improvements = get_neuron_improvements()

    return jsonify(processJSON(suggestions), improvements)


if __name__ == "__main__":
    app.run()
    show()
