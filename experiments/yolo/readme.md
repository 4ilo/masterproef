## Recreate results

# Clone this repo
```
    git clone https://github.com/4ilo/masterproef
    cd masterproef/experiments/yolo
```

# Install yolo
```
    git clone https://github.com/pjreddie/darknet
    cd darknet
    make -j8
```

# Run detector
```
    ./darknet detector test ../cust.data ../yolov2-tiny-cust.cfg ../yolov2-tiny-cust.weights ../img/hospital_corridors_2Hz-016.png
    
    Replace image path to the location of your images
```