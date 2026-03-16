import os
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# defer cv2 import until needed; avoids sys dependency when building model



def extract_features(image_path):
    """Read an image from disk, resize it to 128x128 and normalize.

    Returns a numpy array of shape (1, 128, 128, 1) or raises an
    exception if the image cannot be loaded.
    """
    # import cv2 here to avoid requiring system-level graphics libraries
    # when the module is only used for model construction.
    import cv2

    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Failed to load image: {image_path}")

    img = cv2.resize(img, (128, 128))
    img = img.astype(np.float32) / 255.0
    img = np.reshape(img, (1, 128, 128, 1))
    return img


# build and save a simple CNN model suitable for fingerprint recognition
def build_and_save_model(output_path="fingerprint_model.h5"):
    model = Sequential([
        Conv2D(32, (3, 3), activation="relu", input_shape=(128, 128, 1)),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation="relu"),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation="relu", name="feature_dense"),
        Dense(10, activation="softmax", name="output_dense"),
    ])

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    model.save(output_path)
    print(f"Model saved to {output_path}")


def load_model_and_feature_extractor(model_path="fingerprint_model.h5"):
    """Load the full model and return (model, feature_extractor).

    "feature_extractor" produces a 128-dimensional vector from an input image.
    """
    from tensorflow.keras.models import load_model, Model
    full = load_model(model_path)
    # try to identify an input tensor from the first layer
    first_layer = full.layers[0]
    input_tensor = getattr(first_layer, 'input', None)
    if input_tensor is None:
        # create a new Input and rebuild sequential
        from tensorflow.keras import Input
        input_tensor = Input(shape=(128, 128, 1))
        # reapply for building a functional model version
        x = input_tensor
        for layer in full.layers:
            x = layer(x)
        full = Model(inputs=input_tensor, outputs=x)
    # assume the layer just before output is named 'feature_dense'
    feat_layer = full.get_layer("feature_dense").output
    # use first_layer.input if available or full.input
    in_tensor = input_tensor if input_tensor is not None else full.input
    feature_extractor = Model(inputs=in_tensor, outputs=feat_layer)
    return full, feature_extractor


def image_to_vector(image_path, feature_extractor=None, model_path="fingerprint_model.h5"):
    """Return 1-d numpy vector for given image.

    If feature_extractor is provided it will be used directly; otherwise the
    function will load it from disk.
    """
    if feature_extractor is None:
        _, feature_extractor = load_model_and_feature_extractor(model_path)

    data = extract_features(image_path)
    vec = feature_extractor.predict(data)
    # output shape is (1, 128)
    return vec.flatten()


# similarity metrics
def cosine_similarity(u, v):
    u = np.asarray(u, dtype=np.float32)
    v = np.asarray(v, dtype=np.float32)
    if u.ndim != 1 or v.ndim != 1:
        raise ValueError("cosine_similarity expects 1-d vectors")
    dot = np.dot(u, v)
    norm = np.linalg.norm(u) * np.linalg.norm(v)
    return dot / norm if norm != 0 else 0.0


def euclidean_distance(u, v):
    u = np.asarray(u, dtype=np.float32)
    v = np.asarray(v, dtype=np.float32)
    return np.linalg.norm(u - v)


if __name__ == "__main__":
    # example usage
    sample_image = "example.jpg"
    try:
        features = extract_features(sample_image)
        print("Extracted feature shape", features.shape)
    except Exception as e:
        print(e)

    build_and_save_model()