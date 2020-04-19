import sys
import json
import time
import getopt
import cv2
import numpy as np
import mvnc.mvncapi as mvncapi
import movidus_utils
import yolo_utils

def detect_object_in_video(graph_file, meta_file, video_in_name, video_out_name, threshold): 
    # Retrieve meta data from YOLO
    meta = yolo_utils.get_meta(meta_file)
    # Set threshold
    meta['thresh'] = threshold

    # Set up mvnc device using movidius
    device = movidus_utils.get_mvnc_device()
    graph, input_fifo, output_fifo = movidus_utils.load_graph(device, graph_file)

    # Load and configure video file using cv2
    video_in = cv2.VideoCapture()
    video_in.open(video_in_name)
    fps = int(video_in.get(cv2.CAP_PROP_FPS))  
    width = int(video_in.get(cv2.CAP_PROP_FRAME_WIDTH) ) 
    height= int(video_in.get(cv2.CAP_PROP_FRAME_HEIGHT)) 
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_out = cv2.VideoWriter(video_out_name, fourcc, fps, (width,height))

    times = []

    while True:
        has_video, frame = video_in.read()
        # Check if we have finished loading video
        if not has_video:
            print("Video Ended")
            break   

        # Pre-process image using frame and meta data
        original_frame = np.copy(frame)
        original_image_dimensions = original_frame.shape
        frame = yolo_utils.pre_proc_img(frame, meta)

        start = time.time()

        # Perform object detection
        graph.queue_inference_with_fifo_elem(input_fifo, output_fifo, frame, 'user object')
        output, _ = output_fifo.read_elem()

        end = time.time()
        
        print('FPS: {:.2f}'.format((1 / (end - start))))
        
        times.append((1/ (end - start)))
        
        # Present result in output video
        y_out = np.reshape(output, (13, 13,125))
        y_out = np.squeeze(y_out)
        boxes = yolo_utils.procces_out(y_out, meta, original_image_dimensions)
        yolo_utils.add_bb_to_img(original_frame, boxes)
        video_out.write(original_frame)

    video_in.release()
    video_out.release()

def print_usage():
    print("python3 obj_detect.py --input=video_in.mp4 --output=video_out.mp4 --graph=yolov2-tiny.graph --meta=yolov2-tiny.meta --threshold=0.3")

def main(argv):
    # Default Threshold value
    threshold = 0.3

    try:
        opts, args = getopt.getopt(argv, "hiomgt", ["help", "input=", "output=", "meta=", "graph=", "threshold="])
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_usage()
            sys.exit(0)
        elif opt in ("-i", "--input"):
            video_in = arg
        elif opt in ("-o", "--output"):
            video_out = arg
        elif opt in ("m", "--meta"):
            meta = arg
        elif opt in ("-g", "--graph"):
            graph = arg
        elif opt in ("-t", "--threshold"):
            threshold = int(arg)

    # Check that all parameters were correctly received
    try:
        video_in
        video_out
        meta
        graph
        threshold
    except NameError:
        print_usage()
        sys.exit(2)

    detect_object_in_video(graph, meta, video_in, video_out, threshold)

if __name__ == '__main__':
    main()