import cv2

# 定义捕获视频的分辨率
frame_width = 640
frame_height = 480

# 创建视频捕捉对象。参数0表示第一个摄像头
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

# 定义视频编码器和创建 VideoWriter 对象
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (frame_width, frame_height))

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("Error: Camera is not opened.")
    exit()

try:
    while True:
        # 从摄像头读取一帧
        ret, frame = cap.read()
        
        # 如果正确读取帧，ret 是 True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # 写入帧到文件
        out.write(frame)

        # 显示帧
        cv2.imshow('Frame', frame)
        
        # 按 'q' 键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # 释放摄像头和文件句柄并关闭所有窗口
    cap.release()
    out.release()
    cv2.destroyAllWindows()