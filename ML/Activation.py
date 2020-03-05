#import keras 
#import keras.layers.Activation
from keras.layers import Activation as activ
#from keras.layers import advanced_activations as adv_activ
import keras.layers.advanced_activations as adv_activ

class Activation():

    def __init__( self, activation_name ) :
        # activationLayerDict = {
        #     'relu' : keras.layers.ReLU,
        #     'prelu' : keras.layers.PReLU,
        #     'leakyrelu' : keras.layers.LeakyReLU,
        #     'elu' : keras.layers.ELU
        # }
        activationLayerDict = {
            'relu' : activ('relu'),
            'prelu' : adv_activ.PReLU,
            'leakyrelu' : adv_activ.LeakyReLU,
            'elu' : activ('elu')
        }
       # activationLayerDict = {
       #      'relu' : keras.layers.Activation('relu'),
       #      'prelu' : keras.layers.Activation('prelu'),
       #      'leakyrelu' : keras.layers.Activation('LeakyReLU'),
       #      'elu' : keras.layers.Activation('ELU')
       #  }

        if not activation_name in activationLayerDict:
            raise KeyError( 'Error in Activation::__init__() : activation {} not found.'.format( activation_name ) )

        self.__keras_activation_layer = activationLayerDict[ activation_name ]


    def kerasActivationLayer( self ):
        return self.__keras_activation_layer
