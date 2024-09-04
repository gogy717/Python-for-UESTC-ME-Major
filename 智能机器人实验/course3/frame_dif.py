import cv2
import numpy as np

def frame_difference(video_path):
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    
    # 读取第一帧
    ret, frame1 = cap.read()
    if not ret:
        print("Failed to read the video")
        return
    
    # 转换为灰度图像
    prev_frame = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    
    while True:
        # 读取下一帧
        ret, frame2 = cap.read()
        if not ret:
            break
        
        # 转换为灰度图像
        curr_frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        # 滤波
        curr_frame = cv2.GaussianBlur(curr_frame, (5,5), 1)
        curr_frame = cv2.medianBlur(curr_frame, 5)
        # 计算帧差
        frame_diff = cv2.absdiff(prev_frame, curr_frame)
        
        # 二值化处理
        _, thresh = cv2.threshold(frame_diff, 50, 255, cv2.THRESH_BINARY)
        
        # 显示结果        
        thresh = cv2.dilate(thresh, None, iterations=4)
        # thresh = cv2.erode(thresh, None, iterations=4)
        # draw countours larger than 5000
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
        for contour in contours:
            if cv2.contourArea(contour) > 1000:
                # rectangle around the contour
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame2, (x, y), (x+w, y+h), (0, 255, 0), 3)
                cv2.putText(frame2, 'Moving Object', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                
        cv2.imshow('Contours', frame2)
        cv2.imshow('Frame Difference', thresh)

        
        # 按'q'退出
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        
        # 更新前一帧
        prev_frame = curr_frame
    
    # 释放资源
    cap.release()
    cv2.destroyAllWindows()

# 调用函数
frame_difference("/Users/luozhufeng/Downloads/traffic_vid.mp4")
