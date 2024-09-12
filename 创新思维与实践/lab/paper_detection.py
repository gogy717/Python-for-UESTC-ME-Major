import cv2
import numpy as np

def get_gray(file_path: str) -> np.ndarray:
    """
    helper function that reads in a gray scale image in dim 640*360
    :param file_path: path to the image
    
    :return: gray scale image
    """
    gray = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    gray = cv2.resize(gray, (640, 360))
    gray = cv2.GaussianBlur(gray, (5,5), 0)
    return gray


def get_edges(gray: np.ndarray) -> np.ndarray:
    """
    helper function that reads in a gray scale image 
    and returns edges detected by Canny
    :param gray: gray scale image
    
    :return: edges detected by Canny
    """
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    # connect edges that are close to each other
    
    kernel = np.ones((5, 5), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    
    
    return edges


def find_paper(edges: np.ndarray) -> np.ndarray:
    """
    helper function that reads in edges detected by Canny
    and returns the paper's contour
    
    :param edges: edges detected by Canny
    
    :return: paper's contour
    """
    (contours, _) = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for contour in contours:
        
        # if cv2.contourArea(contour) < 350 or cv2.arcLength(contour, True) < 100:
        #     cv2.drawContours(edges, [contour], -1, (0, 0, 0), 2)
        #     cv2.imshow('edges', edges)
        #     cv2.waitKey(0)
        #     cv2.destroyAllWindows()
        #     continue
        
        
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        
        
        dark = np.zeros_like(edges)
        cv2.drawContours(dark, [contour], -1, (255, 255, 255), -1)
        cv2.putText(dark, 'Area: ' + str(cv2.contourArea(contour)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(dark, 'Number of approx: ' + str(len(approx)), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow('dark', dark)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        # Show images in parallel
        cv2.imshow('edges', edges)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        


        if len(approx) == 4:
            cv2.drawContours(edges, [approx], -1, (255, 0, 0), 2)
            cv2.imshow('edges', edges)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return approx
        

def rectify(h):
    h = h.reshape((4,2))
    hnew = np.zeros((4,2),dtype = np.float32)

    add = h.sum(1)
    hnew[0] = h[np.argmin(add)]
    hnew[2] = h[np.argmax(add)]

    diff = np.diff(h,axis = 1)
    hnew[1] = h[np.argmin(diff)]
    hnew[3] = h[np.argmax(diff)]

    return hnew


def map_a4_paper(paper: np.ndarray, image: np.ndarray) -> np.ndarray:
    """
    helper function that maps the paper to an A4 paper
    
    :param paper: paper's contour
    :para, image: image
    
    :return mapped paper's contour
    """
    approx = rectify(paper)
    
    # Print rectified corners
    print("Rectified corners:", approx)
    
    # A4 paper size in pixels (Portrait mode)
    pts2 = np.float32([[0, 0], [842, 0], [842, 595], [0, 595]])

    # Get perspective transform
    M = cv2.getPerspectiveTransform(approx, pts2)
    
    # Warp the image using the perspective transformation
    dst = cv2.warpPerspective(image, M, (842, 595))
    
    # Check the output image size
    print("Warped image size:", dst.shape)
    
    return dst


    
    

if __name__ == "__main__":
    file_path = "/Users/luozhufeng/Desktop/Python-for-UESTC-ME-Major/创新思维与实践/images/captures/frame0.png"
    gray = get_gray(file_path)
    edges = get_edges(gray)
    paper = find_paper(edges)
    image = cv2.imread(file_path)
    image = cv2.resize(image, (640, 360))
    if paper is None:
        print("Paper not found")
        # create mouse click event to find paper
        # cv2.setMouseCallback('edges', mouse_click_event)
        
    mapped_paper = map_a4_paper(paper, image)
    cv2.imshow('mapped_paper', mapped_paper)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    