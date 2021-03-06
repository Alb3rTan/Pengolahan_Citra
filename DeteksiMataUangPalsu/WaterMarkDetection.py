import glob
import cv2 
import numpy as np
import imutils 
import tkinter
from tkinter import messagebox
import Main


def WM_Detection():
    # load WM template
    WM_data = []    
    WM_files = glob.glob('template/'+Main.Tamplate_wm, recursive=True)
    print("Template WM loaded:", WM_files)
    # prepare WM template==============================================================
    for WM_files in WM_files:
        tmp = cv2.imread(WM_files)        
        # grayscale====================================================================
        tmp = cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY)
        # Contrast & Brightness========================================================
        alpha = 1 # Contrast control (1.0-3.0)
        beta = 10 # Brightness control (0-100)
        tmp = cv2.convertScaleAbs(tmp, alpha=alpha, beta=beta)
        cv2.imshow("Template CB", tmp)         
        #===========================================================================================
        WaterMark = WM_files.replace('WaterMark\\', '').replace('.jpg', '')
        WM_data.append({"glob_WM":tmp, "WaterMark":WaterMark})
        #===========================================================================================
    
    # Image Testing
    for image_glob in glob.glob('test/'+Main.Image):
        for WM_data in WM_data:
            image_test_WM = cv2.imread(image_glob)
            (tmp_height, tmp_width) = WM_data['glob_WM'].shape[:2]            
            # grayscale====================================================================
            image_test_W = cv2.cvtColor(image_test_WM, cv2.COLOR_BGR2GRAY) 
            # Contrast & Brightness========================================================
            alpha = 1 # Contrast control (1.0-3.0)
            beta = 10 # Brightness control (0-100)
            image_test_W = cv2.convertScaleAbs(image_test_W, alpha=alpha, beta=beta)
            cv2.imshow("Image CB", image_test_W)
            #===========================================================================================
            
            # template matching
            found = None
            thershold = 0.9
            for scale in np.linspace(0.2, 1.0, 20)[::-1]: 
                # scalling uang
                resized = imutils.resize(image_test_W, width=int(image_test_W.shape[1] * scale))
                r = image_test_W.shape[1] / float(resized.shape[1])                 

                if resized.shape[0] < tmp_height or resized.shape[1] < tmp_width:
                    break

                # template matching
                result1 = cv2.matchTemplate(resized, WM_data['glob_WM'], cv2.TM_CCOEFF_NORMED)
                (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result1)
                if found is None or maxVal > found[0]:
                    found = (maxVal, maxLoc, r)
                    if maxVal >= thershold: 
                        root = tkinter.Tk()
                        root.withdraw()
                        messagebox.showinfo(WM_data['WaterMark'], "Detected") 
                                       

                if found is not None: 
                    (maxVal, maxLoc, r) = found
                    (startX, startY) = (int(maxLoc[0]*r), int(maxLoc[1] * r))
                    (endX, endY) = (
                        int((maxLoc[0] + tmp_width) * r), int((maxLoc[1] + tmp_height) * r))
                    if maxVal >= thershold:
                        cv2.rectangle(image_test_WM, (startX, startY),
                                    (endX, endY), (0, 0, 255), 2)
                        
                
                    cv2.imshow("Result", image_test_WM)

            cv2.waitKey(0)


#if __name__ == "__main__": 
#    WM_Detection()
