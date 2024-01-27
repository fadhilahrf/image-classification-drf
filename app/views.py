from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import ModelSerializer
from keras.models import load_model
from PIL import Image
from io import BytesIO
import numpy as np
from keras.preprocessing import image

MODEL_LIST = [
    {
        'title': 'Cat and Dog Model',
        'name':'cat_dog_model',
        'slug': 'cat-dog-model',
        'class': ['CAT', 'DOG'],
        'description': 'Classification for cat and dog',
        'inputSize': 128
    },
    {
        'title': 'MNIST Model',
        'name':'mnist_model',
        'slug': 'mnist-model',
        'class': ['0', '1', '2', '3' ,'4' , '5', '6', '7', '8', '9'],
        'description': 'Classification for handwritten numbers',
        'inputSize': 28
    }
]

def predict(image, model_name):
    model = load_model('app/model_ml/'+model_name+'.h5')
    input_shape = model.layers[0].input_shape
    if input_shape[-1] == 1:
        image = Image.open(BytesIO(image)).resize((input_shape[1],input_shape[2])).convert('L')
    else:
        image = Image.open(BytesIO(image)).resize((input_shape[1],input_shape[2]))
    image = image_to_np(image)
    result = model.predict(image)
    return np.argmax(result)

def image_to_np(image, size=128):
    image = np.array(image)
    image = np.expand_dims(image, axis=0)
    return image

@api_view(['POST'])
def hello_world(request: Request):
    if request.method == 'POST':
        serializer = ModelSerializer(data=request.data)
        if serializer.is_valid():
            model = next(m for m in MODEL_LIST if m['name']==request.data['name'])
            return Response({"result": model['class'][predict(request.FILES['image'].read(), model['name'])]})
    return Response({"message": "Failed"})