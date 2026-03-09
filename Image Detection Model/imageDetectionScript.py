import json
import os
import subprocess
import sys
try: #test if ultralytics is here. if not, install ultralytics
    import ultralytics 
except ImportError:
    print("Ultralytics is not installed. Installing ultralytics...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "ultralytics"])
from ultralytics import YOLO
from PIL import Image



model = YOLO("detectionModel/YOLOv8_OIv7_pretrain.pt") # Load the model and predict
results = model.predict("detectImage/scannedObject.png")
result = results[0]



def tagCheck(itemCategory,itemType): #check if a given item type fits a certain category
    path = os.path.join('imageCategories/OIv7', itemCategory + '.json') #json file only contains items that fit in a given category e.g "Fragile.json" only contains fragile items
    
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return False

    with open(path, 'r') as file:
        categoryList = json.load(file)
        for entry in categoryList:
            if entry.get("id") == itemType:
                return True
    return False
#print(tagCheck('Stackable',1)) #for testing



def categoryCheck(itemType): #yung categories lang natin sa app na nilgay ko is Miscellaneous, Electronics, Food, Fragile -Jamie
    if tagCheck('Electronic',itemType):
        return 'Electronic'
    elif tagCheck('Food',itemType):
        return 'Food'
    elif tagCheck('Fragile',itemType): #until i figure out multiple categories, elec and food supersede fragile. see imageCategories\Dejis Interpratation of the Categories.png
        return 'Fragile' #why is fragile a tag AND a category? i don't actually know. might be handled on the swift side
    else:
        return 'Misc'

class scannedItem:
    def __init__(self,itemID,itemType):
        self.itemID = itemID #int, used when multiple objects are detected in the image
        self.itemType = itemType #int, used when looking up category .json files for item tags
        self.itemTypeName = result.names[box.cls[0].item()] #string, what is this item
        self.itemStackable = tagCheck('Stackable',itemType) #bool, is the item stackable?
        self.itemFragile = tagCheck('Fragile',itemType) #bool, is the item fragile?
        self.itemCategory = categoryCheck(itemType) #string, what category does it fall into?



scannedObjects = []
i = 0
for box in result.boxes: #work through scanned items and convert them into scannedItem class
    class_id = int(box.cls[0].item())
    item = scannedItem(i,class_id)
    scannedObjects.append(item)
    #print('Object #'+ str(item.itemID) + ' added') #checking if the class works
    i += 1



for item in scannedObjects:
    print('Item #' + str(item.itemID) + ": " + item.itemTypeName)
    print('Category: ' + item.itemCategory)
    print('Stackable?: ' + str(item.itemStackable))
    print('Fragile?: ' + str(item.itemFragile))
    print('---')



# Show the image with detection
Image.fromarray(result.plot()[:, :, ::-1]).show()