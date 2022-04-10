from flask import Flask, send_from_directory, render_template, jsonify, request, Response
  
import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
from torchvision import  transforms
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
torch.manual_seed(42)


import jsonpickle
import numpy as np
import cv2

#=============================== Model =============================================================
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output
#-----------------------------------------------------------------------------------------------------


app = Flask(__name__)

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)


@app.route('/canvas', methods=['POST'])
def canvas():
    r = request
    # convert string of image data to uint8
    # nparr = np.fromstring(r.data, np.uint8)
    nparr = np.frombuffer(r.data,'u1') 
    # decode image
    img = cv2.imdecode(nparr, 0)

    # ====================== Machine Learning Processing Here =========================================
    transform=transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
    ])

    # Load model here
    model = Net().to(device)
    model.load_state_dict(torch.load('mnist_cnn.pt',map_location=torch.device('cpu')))
    model.eval()

    # img_read = cv2.imread('img.jpg')
    resized_image = cv2.resize(img, (28, 28)) 
    # resized_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    img_to_pred=transform(resized_image).to(device)
    pred = model(img_to_pred.reshape(1,1,28,28)).to(device)
    ps = torch.exp(pred)
    probab = list(ps.detach().numpy()[0])
    result_pred = probab.index(max(probab))
    #-------------------------------------------------------------------------------------------------


    # build a response dict to send back to client

    msg=f'The Predicted Digit is: {result_pred}'
    response = {'message': msg}

    
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route("/")
def home():
    return render_template('index.html')




if __name__ == "__main__":
    app.run()