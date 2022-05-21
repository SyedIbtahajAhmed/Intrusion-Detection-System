import cv2
import numpy as np


framelist=[0,0,0,0,"n","img","confidance",1,2,3,4]
def YoloSSPModelDetection(image):
    
    # framelist=["x","y","w","h","label","img"]
    model=1  #0 tiny(fast)   #1 medium  #2 heavy
    if model==0:
        weights="yoloModelData\\yolov3_tiny_fast\\yolov3.weights"
        cfg="yoloModelData\\yolov3_tiny_fast\\yolov3.cfg"
    if model==1:
        weights="yoloModelData\\yolov3_medium\\yolov3.weights"
        cfg="yoloModelData\\yolov3_medium\\yolov3.cfg"
    if model==2:
        weights="yoloModelData\\yolov3_heavy\\yolov3.weights"
        cfg="yoloModelData\\yolov3_heavy\\yolov3.cfg"

    
    net = cv2.dnn.readNet(weights, cfg)
    classes = []
    with open("yoloModelData\coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    # Loading image


    
    
 
        
        # Capture the video frame
    # by frame
    img = image
    height, width, channels = img.shape
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:

        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            framelist[6]=confidence
            if confidence > 0.7:
                # print(confidence,"conf")
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            person_confidence=confidences[i]
            print("Confidance: ",person_confidence)
            color = colors[0]
            if label=="person":
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y + 30), font, 3, color, 2)
                framelist[0]=x
                framelist[1]=y
                framelist[2]=w
                framelist[3]=h
                framelist[4]=label
                framelist[6]=confidences
                
            else:
                pass
    
    framelist[7]=boxes
    framelist[8]=indexes
    framelist[9]=class_ids   
    framelist[10]=classes  

    framelist[5]=img
        # print(framelist,"inside yolo")
    return img
    # Display the resulting frame
    
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    
  
