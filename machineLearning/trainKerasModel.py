from keras import models
from keras import layers
from keras.layers import Activation
from keras import optimizers
from keras import callbacks
from keras import backend as K
from keras import Input
from keras import Model
import h5py
import tensorflow as tf

#import other parts of framework
import os
import sys
main_directory = os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) )
sys.path.insert( 0, main_directory )
from diagnosticPlotting import *


def tensorFlowSetNumThreads( number_of_threads ):
    K.set_session(K.tf.Session(config=K.tf.ConfigProto(intra_op_parallelism_threads = number_of_threads, inter_op_parallelism_threads = number_of_threads ) ) )


def cleanModelFile( model_file_name ):

    #delete weights in saved model to cirumvent a bug in Keras when loading the model
    trained_model_file = h5py.File( model_file_name, 'r+' )
    del trained_model_file[ 'optimizer_weights' ]
    trained_model_file.close()


def plotModelTrainingHistory( training_history, model_name, fullData = False ):

    #plot loss and accuracy as a function of epochs
    plotAccuracyComparison( training_history, model_name, fullData)
    plotLossComparison( training_history, model_name, fullData )

    #to avoid random tensorflow crashes
    K.clear_session()


class KerasClassifierTrainer():

    def __init__( self, model_name ):
        self.__model_name = model_name


    @property
    def model( self ):
        try:
            return self.__model
        except AttributeError:
            return None


    def buildDenseClassifier( self, input_shape, number_of_hidden_layers = 5, units_per_layer = 256, activation_layer = None, dropout_first = True, dropout_all = False, dropout_rate = 0.5, batchnorm_first = True, batchnorm_hidden = False, batchnorm_before_activation = False ):


        model = models.Sequential()

        #start with normalization layer to deal with potentially unprocessed data if requested
        if batchnorm_first:
            model.add( layers.BatchNormalization( input_shape = input_shape ) )

        #add hidden densely connected layers 
        for x in range(number_of_hidden_layers) :

            #if first layer was not batchnorm, input_shape needs to be defined on first hidden layer 
            if batchnorm_first:
                model.add( layers.Dense( units_per_layer, activation = 'linear' ) )
            else :
                model.add( layers.Dense( units_per_layer, activation = 'linear', input_shape = input_shape ) )

            #add batchnormalization before activation if requested
            if ( batchnorm_hidden and batchnorm_before_activation ):
                model.add( layers.BatchNormalization() )

            #activation layer 

            if type(activation_layer) == str:

                model.add(Activation(activation_layer))

            else:

                model.add( activation_layer() )

            #add batchnormalization after activation if requested
            if( batchnorm_hidden and not batchnorm_before_activation ):
                model.add( layers.BatchNormalization() )

            #add droput ( always after batchnormalization! )
            if (dropout_first and x == 0) or dropout_all:
                model.add( layers.Dropout( dropout_rate ) )

        #output layer
        model.add( layers.Dense( 1, activation = 'sigmoid' ) )

        self.__model = model 



    def __compileModel( self, optimizer ):
    
        #set model objectives
        self.__model.compile( 
        	optimizer = optimizer,
        	loss = 'binary_crossentropy',
        	metrics = [ 'acc' ]
        )

	
    #cut off training at convergence and save model with best validation
    def __callback_list( self ):
        callback_list = [
        	callbacks.EarlyStopping(
        		monitor = 'val_loss',
        		patience = 10
        	),
        	callbacks.ModelCheckpoint(
        		monitor = 'val_acc',
        		filepath = self.__model_name + '.h5',
        		save_best_only = True
        	)
        ]
        return callback_list


    def trainModelArrays( self, train_data, train_labels, validation_data, validation_labels, train_weights = None, validation_weights = None, optimizer = optimizers.Nadam(), number_of_epochs = 20, batch_size = 512, number_of_threads = 1 ):

        self.__compileModel( optimizer )
        
        #set number of threads to use in training        
        #tensorFlowSetNumThreads( number_of_threads )
        
        #train model
        training_history = self.__model.fit(
            train_data,
            train_labels,
            sample_weight = ( None if train_weights.size == 0 else train_weights ),
            epochs = number_of_epochs,
            batch_size = batch_size,
            validation_data = ( validation_data, validation_labels, ( None if validation_weights.size == 0 else validation_weights ) ),
            callbacks = self.__callback_list(),
            verbose = 2
        )
        
        cleanModelFile( self.__model_name + '.h5' )
        plotModelTrainingHistory( training_history, self.__model_name )
	

    def trainModelArraysFullData( self, train_data, train_labels, train_weights = None, optimizer = optimizers.Nadam(), number_of_epochs = 20, batch_size = 512, number_of_threads = 1 ):

        self.__compileModel( optimizer )

        #set number of threads to use in training                                                                                                                      
        #tensorFlowSetNumThreads( number_of_threads )                                                                                                                  

        #train model                                                                                                                                                   
        training_history = self.__model.fit(
            train_data,
            train_labels,
            sample_weight = ( None if train_weights.size == 0 else train_weights ),
            epochs = number_of_epochs,
            batch_size = batch_size,
            verbose = 2
        )
        self.__model.save(self.__model_name + '.h5')
        cleanModelFile( self.__model_name + '.h5' )                                                                                                                  
        plotModelTrainingHistory( training_history, self.__model_name, fullData = True )




if __name__ == '__main__':
	pass
