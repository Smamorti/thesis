import keras.layers.advanced_activations as adv_activ

class Activation():

    def __init__( self, activation_name ) :

        activationLayerDict = {
            'relu' : 'relu',
            'prelu' : adv_activ.PReLU,
            'leakyrelu' : adv_activ.LeakyReLU,
            'elu' : 'elu',
            'selu' : 'selu'
        }

        if not activation_name in activationLayerDict:
            raise KeyError( 'Error in Activation::__init__() : activation {} not found.'.format( activation_name ) )

        self.__keras_activation_layer = activationLayerDict[ activation_name ]


    def kerasActivationLayer( self ):
        return self.__keras_activation_layer
