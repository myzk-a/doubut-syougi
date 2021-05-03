# -*- coding: utf-8 -*-
"""dual_network.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IfXF24RiPIJrJsySZSaAUNb61yS_oE6-
"""

#!pip uninstall tensorflow
#!pip install tensorflow==1.13.1
#!pip uninstall keras
#!pip install keras==2.2.4
#import tensorflow as tf
#import keras
#print(tf.__version__)
#print(keras.__version__)

from tensorflow.keras.layers import Activation, Add, BatchNormalization, Conv2D, Dense, GlobalAveragePooling2D, Input
from tensorflow.keras.models import Model
from tensorflow.keras.regularizers import l2
from tensorflow.keras import backend as K
import os

DN_FILTERS = 128
DN_RESIDUAL_NUM = 16
DN_INPUT_SHAPE = (3, 4, 14)
DN_OUTPUT_SIZE = 132

def conv(filters):
  return Conv2D(filters, 3, padding='same', use_bias=False, kernel_initializer='he_normal', kernel_regularizer=l2(0.0005))

def residual_block():
  def f(x):
    sc = x
    x = conv(DN_FILTERS)(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = conv(DN_FILTERS)(x)
    x = BatchNormalization()(x)
    x = Add()([x, sc])
    x = Activation('relu')(x)
    return x
  return f

def dual_network():
  if os.path.exists('./model/best.h5'):
    return
  
  input = Input(shape=DN_INPUT_SHAPE)

  x = conv(DN_FILTERS)(input)
  x = BatchNormalization()(x)
  x = Activation('relu')(x)

  for i in range(DN_RESIDUAL_NUM):
    x = residual_block()(x)

  x = GlobalAveragePooling2D()(x)

  p = Dense(DN_OUTPUT_SIZE, kernel_regularizer=l2(0.00005), activation='softmax', name='pi')(x)

  v = Dense(1, kernel_regularizer=l2(0.00005))(x)
  v = Activation('tanh', name='v')(v)

  model = Model(inputs=input, outputs=[p,v])

  os.makedirs('./model/', exist_ok=True)
  model.save('./model/best.h5')

  K.clear_session()
  del model

if __name__== '__main__':
  dual_network()



