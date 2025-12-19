# 1) Single Responsibility Principle (SRP)

Each module in the project has only one responsibility.

app.py – User Interface (Streamlit)

predict.py – Image preprocessing and prediction

train_model.py – Model training

auth_service.py – Authentication logic

database.py – Database operations

model_config.py – Model path configuration




# 2) Open–Closed Principle (OCP)

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



