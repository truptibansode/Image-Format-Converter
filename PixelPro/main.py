#pip install flask
#pip install Opencv-python

from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import os
import cv2
#import numpy as np

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'webp', 'jpeg', 'jpg', 'gif'}

app = Flask(__name__)
app.secret_key='super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


"""kernel= np.array([[1,2,1],
                      [2,4,2],
                      [1,2,1],])/16.0"""

def processImage(filename, operation):
    print(f"the operation is {operation} and the filename is {filename}")
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFilename = f"static/{filename}"
            cv2.imwrite(f"static/{filename}", imgProcessed)
            return newFilename
        case "cwebp":
            newFilename = f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cjpg":
            newFilename = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cpng":
            newFilename = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newFilename, img)
            return newFilename
    pass

"""def apply_filter(filename, kernel):
    img = cv2.imread(f"uploads/{filename}")
    if img is None:
        print("ERROR: Please select an image to proceed.")
        exit()
      #Applying image filter using Convolution:
    filtered_img= cv2.filter2D(img, -1, kernel)
    newFilename = f"static/{filename}"
    #display image
    cv2.imshow('original image', img)
    cv2.imshow('Filtered Image', filtered_img)

    #wait for a key to press and then close the window.
    cv2.waitKey(0)
    cv2.destroyAllWindows()"""
        
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method=="POST":
        operation= request.form.get("operation")
         # check if the post request has the file part
        if 'file' not in request.files:
            #flash('No file part')
            return "error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "please select a file to proceed further." 
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, operation)
            flash(f"thank you for waiting! your image has been processed and is available here: <a href='  /{new}' target='_blank'> please click HERE!</a>")
            return render_template("index.html")
    return render_template("index.html")
    
                      

app.run(debug=True, port=5001)
