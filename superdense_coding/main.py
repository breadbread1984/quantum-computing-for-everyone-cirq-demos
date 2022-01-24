#!/usr/bin/python3

import numpy as np;
import cirq;
from absl import app, flags;
from models import superdense_coding;

FLAGS = flags.FLAGS;
flags.DEFINE_string('message', default = None, help = 'message to send');

def main(unused_argv):
  
