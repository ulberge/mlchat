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

def channel_attr_simple(img, layer, class_name, n_show=4):

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

  # Now we just need to present the results.
  
  # Get spritemaps
  
  
  spritemap_n, spritemap_url = googlenet_spritemap(layer)

  # Let's pick the most extreme channels to show
  ns_pos = list(np.argsort(-channel_attr)[:n_show])
  
  print ns_pos
  
  return ns_pos
  
@app.route('/dreams', methods=['GET', 'POST'])
def dreams():
  imgUrl = request.args.get('url')
  n_show = request.args.get('n_show')
  img = load(imgUrl)
  ns_pos = channel_attr_simple(img, "mixed4d", "Labrador retriever", n_show=3)
  print ns_pos
  return jsonify(ns_pos)

@app.route('/intent/new', methods=['POST'])
def newIntent():
  imgUrl = request.args.get('url')
  n_show = request.args.get('n_show')
  img = load(imgUrl)
  ns_pos = channel_attr_simple(img, "mixed4d", "Labrador retriever", n_show=3)
  print ns_pos
  return jsonify(ns_pos)

if __name__ == '__main__':
    app.run()