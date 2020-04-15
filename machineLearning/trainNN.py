import numpy as np
from diagnosticPlotting import *
from Optimizer import Optimizer
from Activation import Activation
# from Dataset import concatenateAndShuffleDatasets
# from DataCollection import DataCollection
from trainKerasModel import KerasClassifierTrainer
from keras.models import load_model
from tensorflow import set_random_seed
set_random_seed(2)


def trainNN(model_name, configuration, training_data, validation_data, test_data, val_frac, signal_collection, background_collection):

    #make keras optimizer object 
    keras_optimizer = Optimizer( configuration['optimizer'], configuration['learning_rate'], configuration['learning_rate_decay'] ).kerasOptimizer()

    #retrieve keras activation layer class
    keras_activation_layer = Activation( configuration['activation'] ).kerasActivationLayer()

    model_builder = KerasClassifierTrainer( model_name )

    model_builder.buildDenseClassifier(
        input_shape = configuration['input_shape'],
        number_of_hidden_layers = configuration['number_of_hidden_layers'], 
        units_per_layer = configuration['units_per_layer'], 
        activation_layer = keras_activation_layer, 
        dropout_first = configuration['dropout_first'],
        dropout_all = configuration['dropout_all'],
        dropout_rate = configuration['dropout_rate'],
        batchnorm_first = configuration['batchnorm_first'],
        batchnorm_hidden = configuration['batchnorm_hidden'],
        batchnorm_before_activation = configuration['batchnorm_before_activation'],
        )
    if val_frac == 0:

        model_builder.trainModelArraysFullData(
            train_data = training_data.samples,
            train_labels = training_data.labels,
            train_weights = training_data.weights,
            optimizer = keras_optimizer,
            number_of_epochs = configuration['number_of_epochs'],
            batch_size = configuration['batch_size'],
            number_of_threads = configuration['number_of_threads']
        )

    else:

        model_builder.trainModelArrays(
            train_data = training_data.samples,
            train_labels = training_data.labels,
            validation_data = validation_data.samples,
            validation_labels = validation_data.labels,
            train_weights = training_data.weights,
            validation_weights = validation_data.weights,
            optimizer = keras_optimizer,
            number_of_epochs = configuration['number_of_epochs'],
            batch_size = configuration['batch_size'],
            number_of_threads = configuration['number_of_threads']
        )

    model = load_model( model_name + '.h5' )

    signal_collection.training_set.addOutputs( model.predict( signal_collection.training_set.samples ) )
    signal_collection.validation_set.addOutputs( model.predict( signal_collection.validation_set.samples ) )
    signal_collection.test_set.addOutputs( model.predict( signal_collection.test_set.samples ) )

    background_collection.training_set.addOutputs( model.predict( background_collection.training_set.samples ) )
    background_collection.validation_set.addOutputs( model.predict( background_collection.validation_set.samples))
    background_collection.test_set.addOutputs( model.predict( background_collection.test_set.samples ) )


    print(signal_collection.training_set.outputs)
