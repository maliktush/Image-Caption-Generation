from flask import Flask, request
import os
import base64
import googleapiclient.discovery
from google.api_core.client_options import ClientOptions


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "image-caption-generator-347802-5b09c524dbde.json" 

app = Flask(__name__)

def predict_json(image_string, version=None):
    """Send json data to a deployed model for prediction.
    Args:
        project (str): project where the Cloud ML Engine Model is deployed.
        model (str): model name.
        instances ([Mapping[str: Any]]): Keys should be the names of Tensors
            your deployed model expects as inputs. Values should be datatypes
            convertible to Tensors, or (potentially nested) lists of datatypes
            convertible to Tensors.
        version (str): version of the model to target.
    Returns:
        Mapping[str: any]: dictionary of prediction results defined by the 
            model.
    """
    # Create the ML Engine service object
    api_endpoint = "https://ml.googleapis.com"
    client_options = ClientOptions(api_endpoint=api_endpoint)

    # Setup model path
    model_path = "projects/image-caption-generator-347802/models/image_cap_gen_v2"
    if version is not None:
        model_path += "/versions/{}".format(version)

    # Create ML engine resource endpoint and input data
    ml_resource = googleapiclient.discovery.build(
        "ml", "v1", cache_discovery=False, client_options=client_options).projects()
    instances_list = [image_string] # turn input into list (ML Engine wants JSON)
    
    input_data_json = {"signature_name": "serving_default",
                       "instances": instances_list}

    request = ml_resource.predict(name=model_path, body=input_data_json)
    response = request.execute()
    
    # # ALT: Create model api
    # model_api = api_endpoint + model_path + ":predict"
    # headers = {"Authorization": "Bearer " + token}
    # response = requests.post(model_api, json=input_data_json, headers=headers)

    if "error" in response:
        raise RuntimeError(response["error"])

    return response["predictions"][0]

@app.route('/')
def home():
    return 'Hello World'


@app.route('/generate_caption',methods = ['POST'])
def generate_caption():
    imagefile = request.files['imagefile']
    image_string = base64.b64encode(imagefile.read()).decode("utf-8")
    print('Hitting the Google Cloud AI platform API now...')
    return predict_json(image_string)



if __name__ == '__main__':
    app.run(debug=True)