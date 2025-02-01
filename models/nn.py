import numpy as np

from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Input, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.regularizers import l1_l2

class NeuralNetwork(BaseModel):
    def fit(self):
        Y_train = to_categorical(self.Y_train, num_classes=10)
        Y_test = to_categorical(self.Y_test, num_classes=10)

        model = Sequential()
        model.add(Input(shape=(self.X_train.shape[1],)))
        model.add(Dense(128, activation='relu', kernel_regularizer=l1_l2(l1=0.0002, l2=0.0002)))
        model.add(Dropout(0.33))
        model.add(Dense(96, activation='relu', kernel_regularizer=l1_l2(l1=0.0002, l2=0.0002)))
        model.add(Dropout(0.33))
        model.add(Dense(48, activation='relu', kernel_regularizer=l1_l2(l1=0.0002, l2=0.0002)))
        model.add(Dropout(0.33))
        model.add(Dense(10, activation='softmax'))

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        early_stopping = EarlyStopping(monitor='val_accuracy', patience=100, restore_best_weights=True)

        history = model.fit(
            self.X_train, Y_train,
            epochs=300,
            batch_size=32,
            validation_data=(self.X_test, Y_test),
            callbacks=[early_stopping],
            verbose=2
        )

        test_loss, test_acc = model.evaluate(self.X_test, Y_test, verbose=2)

        print(f"Test Accuracy: {test_acc:.4f}")
        print(f"Test Loss: {test_loss:.4f}")
        self.model = model

    def predict(self):
        self.Y_pred = np.argmax(self.model.predict(self.X_test), axis=1)
