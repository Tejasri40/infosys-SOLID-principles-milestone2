Model Training & Testing

This milestone focuses on training and testing deep learning models for crop disease detection using image datasets. Two separate models were trained for Rice and Pulse (Bean) crops using Convolutional Neural Networks (ResNet-18).

Datasets Used

Pulse Dataset
bean_rust, healthy, leaf_spot

Number of classes: 3

Rice Dataset
blast, blight, tungro

Number of classes: 3

Training Process

Dataset loaded using ImageFolder Data split into training and validation sets Model trained for multiple epochs Validation accuracy monitored at each epoch Best performing model saved

Sample training output:

Epoch 1/20

Train Loss: 10.46 | Train Acc: 71.05%

Val Loss: 10.16 | Val Acc: 52.08%

✓ Best model saved!

Model Testing

Trained models were tested using validation data Class predictions and confidence scores verified Model performance confirmed before deployment

Sample Output

Loading trained model...

Model loaded successfully

Classes: ['blast', 'blight', 'tungro']

Testing multiple images...

Image: blast_001.jpg

Prediction: blast (99.75%)

Outcome

Successfully trained Rice and Pulse disease detection models Verified prediction accuracy on validation data Saved best-performing models for deployment Prepared models for integration with Streamlit application
**1) Single Responsibilty Principle (SRP)**

Each module in the project has only one responsibility.

app.py – User Interface (Streamlit)

predict.py – Image preprocessing and prediction

train_model.py – Model training

auth_service.py – Authentication logic

database.py – Database operations

model_config.py – Model path configuration




**2) Open/Closed Principle (OCP)**

The system is open for extension but closed for modification.

- New crops or models can be added in **model_config.py**
 
- Existing prediction logic does not need to be changed

Example:

MODELS = {

    "Rice": "models/rice_model.pth",
    
    "Pulse": "models/pulse_model.pth"
    
}


**3) Liskov Substitution Principle (LSP)**

All crop models are interchangeable during prediction.

Rice model and Pulse model follow the same structure

Prediction works with any valid model path

prediction_service.predict(model_path, image)


**4) Interface Segregation Principle (ISP)**

Interfaces are small and focused.

The prediction interface contains only required methods (like predict).

Clients (UI in app.py) depend only on the methods they use.

Unnecessary methods are avoided in interfaces.

**Interfaces:**

auth_interface.py

prediction_interface.py

**Implementations:**

auth_service.py

prediction_service.py



**5) Dependency Inversion Principle (DIP)**

High-level modules(app.py) do not depend on low-level modules directly.

Both depend on abstractions(interfaces)

Dependencies are provided using a service method (for example: get_prediction_service())






