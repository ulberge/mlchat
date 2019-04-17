#!/usr/bin/env python
# -*- coding: utf-8 -*-

#       _                              
#      | |                             
#    __| |_ __ ___  __ _ _ __ ___  ___ 
#   / _` | '__/ _ \/ _` | '_ ` _ \/ __|
#  | (_| | | |  __/ (_| | | | | | \__ \
#   \__,_|_|  \___|\__,_|_| |_| |_|___/ .
#
# A 'Fog Creek'–inspired demo by Kenneth Reitz™

import os
from flask import Flask, request, render_template, jsonify

import numpy as np
import tensorflow as tf

import lucid.modelzoo.vision_models as models
from lucid.misc.io import show, load
import lucid.optvis.render as render


# Support for gomix's 'front-end' and 'back-end' UI.
app = Flask(__name__, static_folder='public', template_folder='views')

# Set the app secret key from the secret environment variables.
app.secret = os.environ.get('SECRET')

# Dream database. Store dreams in memory for now. 
DREAMS = ['Python. Python, everywhere.']


@app.after_request
def apply_kr_hello(response):
    """Adds some headers to all responses."""
  
    # Made by Kenneth Reitz. 
    if 'MADE_BY' in os.environ:
        response.headers["X-Was-Here"] = os.environ.get('MADE_BY')
    
    # Powered by Flask. 
    response.headers["X-Powered-By"] = os.environ.get('POWERED_BY')
    return response


@app.route('/')
def homepage():
    """Displays the homepage."""
    return render_template('index.html')

model = models.InceptionV1()
model.load_graphdef()

layer_spritemap_sizes = {
  'mixed3a' : 16,
  'mixed3b' : 21,
  'mixed4a' : 22,
  'mixed4b' : 22,
  'mixed4c' : 22,
  'mixed4d' : 22,
  'mixed4e' : 28,
  'mixed5a' : 28,
}

def googlenet_spritemap(layer):
  assert layer in layer_spritemap_sizes
  size = layer_spritemap_sizes[layer]
  url = "https://storage.googleapis.com/lucid-static/building-blocks/googlenet_spritemaps/sprite_%s_channel_alpha.jpeg" % layer
  return size, url

def score_f(logit, name):
  if name is None:
    return 0
  elif name == "logsumexp":
    base = tf.reduce_max(logit)
    return base + tf.log(tf.reduce_sum(tf.exp(logit-base)))
  elif name in model.labels:
    return logit[model.labels.index(name)]
  else:
    raise RuntimeError("Unsupported")

def get_channel_attr(img):
  layer = "mixed4d"
  class_name = "Labrador retriever"
  # Set up a graph for doing attribution...
  with tf.Graph().as_default(), tf.Session() as sess:
    t_input = tf.placeholder_with_default(img, [None, None, 3])
    T = render.import_model(model, t_input, t_input)
    
    # Compute activations
    acts = T(layer).eval()
    
    # Compute gradient
    logit = T("softmax2_pre_activation")[0]
    score = score_f(logit, class_name)
    t_grad = tf.gradients([score], [T(layer)])[0]
    grad = t_grad.eval()
    
    # Let's do a very simple linear approximation attribution.
    # That is, we say the attribution of y to x is 
    # the rate at which x changes y times the value of x.
    attr = (grad*acts)[0]
    
    # Then we reduce down to channels.
    channel_attr = attr.sum(0).sum(0)

  return channel_attr

canon = []
avg_intent_order = []
neuronCount = 100

@app.route('/judge', methods=['GET', 'POST'])
def judge():
  img_url = request.args.get('url')
  print img_url
  img = load(img_url)
  print 'get channel from layer'
  channel_attr = get_channel_attr(img)
  
  # Let's pick the most extreme channels to show
  ns_pos = list(np.argsort(-channel_attr)[:100])
  
  for i in ns_pos:
    canon[i] = (i, channel_attr[i])
    
  
  
  
  print 'finished get channel from layer'
  
  idxMap = dict([(channel_attr[i],i) for i in range(len(channel_attr))])
  
  # Let's get all the diffs between avgs and current
  # diffs will be in order of avg_intent_order
  diffs = channel_attr
  for i in range(len(avg_intent_order)):
    j = avg_intent_order[i]
    diffs[j] = avg_intent[j] - channel_attr[j]
  
  # this is the order of the avg_intents
  diffs_order = list(np.argsort(diffs))[::-1]
  neuron_indexes_ordered = []
  neuron_diffs_ordered = []
  for diff_index, avg_intent_index in diffs_order:
    neuron_diffs_ordered.append(diffs[diff_index])
    neuron_index = avg_intent_order[avg_intent_index]
    neuron_indexes_ordered.append(neuron_index)
  
  #  reorder the ns_pos by diffs
  ns_pos_ordered = []
  ns_pos_diff_ordered = []
  for i in diffs_order:
    ns_pos_ordered.append(ns_pos[i])
    ns_pos_diff_ordered.append(diffs[i])
  print order_diffs[:10]
  print ns_pos_ordered[:10]
  
  # return ''
  return jsonify(ns_pos_ordered)

@app.route('/intent/new', methods=['POST'])
def newIntent():
  img_url = request.values.get('url')
  print img_url
  print 'loading intent image'
  img = load(img_url)
  print 'loaded intent image'
  channel_attr = get_channel_attr(img)
  
  # Let's pick the most important channels of the cannon
  ns_pos = list(np.argsort(-channel_attr)[:100])
  
  # Replace the canon
  for i in ns_pos:
    canon[i] = (i, channel_attr[i])
  
  return jsonify(success=True)

if __name__ == '__main__':
    app.run()