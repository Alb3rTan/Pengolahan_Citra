

import glob
import cv2 
import numpy as np
import imutils 


def WM_Detection():
    # load template
    template_data = []
    template_files = glob.glob('template/WM5000.jpg', recursive=True)
    print("template loaded:", template_files)
    # prepare template
    for template_file in template_files:
        tmp = cv2.imread(template_file)

        # scalling
        tmp = imutils.resize(tmp, width=int(tmp.shape[1]*0.5))

        # grayscale
        tmp = cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY)  
        	
        (thresh, blackAndWhiteImage) = cv2.threshold(tmp, 135, 220, cv2.THRESH_BINARY)
        	
        cv2.imshow('Black white image', blackAndWhiteImage)
        #kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

        # sharpening
        #tmp = cv2.filter2D(tmp, -1, kernel)

        # smoothing
        # blur
        #tmp = cv2.blur(tmp, (1, 1))
        # GaussianBlur
        #tmp = cv2.GaussianBlur(tmp,(5,5),0)

        # Edge 
        # with Canny
        #tmp = cv2.Canny(tmp, 100, 220)  
        # with adaptiveThreshold
        #tmp = cv2.adaptiveThreshold(tmp,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,5)

        #tmp = imutils.rotate_bound(tmp,-90)
               

        nominal = template_file.replace('template\\', '').replace('.jpg', '')
        template_data.append({"glob":tmp, "nominal":nominal})
     
    # template matching
    for image_glob in glob.glob('test/5000.jpg'):
        for template in template_data:
            image_test = cv2.imread(image_glob)
            (tmp_height, tmp_width) = template['glob'].shape[:2]
            #cv2.imshow("Template Pembanding", template['glob'])  

            image_test_p = cv2.cvtColor(image_test, cv2.COLOR_BGR2GRAY) 
            #cv2.imshow("Step: Grayscal", image_test_p) 
            (thresh, blackAndWhiteImageTest) = cv2.threshold(image_test_p, 135, 220, cv2.THRESH_BINARY)
        	
            cv2.imshow('Black white image test', blackAndWhiteImageTest)

            #image_test_p = cv2.Canny(image_test_p, 50, 200)
            #cv2.imshow("Step: edge with canny", image_test_p) 

            #image_test_p = cv2.adaptiveThreshold(image_test_p,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,15,10)
            #cv2.imshow("Step: edge with adaptiveThreshold", image_test_p)

            found = None
            thershold = 0.4
            for scale in np.linspace(0.2, 1.0, 20)[::-1]: 
                # scalling uang
                resized = imutils.resize(
                    image_test_p, width=int(image_test_p.shape[1] * scale))
                r = image_test_p.shape[1] / float(resized.shape[1]) 
                cv2.imshow("Step: rescale", resized) 
                if resized.shape[0] < tmp_height or resized.shape[1] < tmp_width:
                    break

                # template matching
                result = cv2.matchTemplate(resized, template['glob'], cv2.TM_CCOEFF_NORMED)
                (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
                if found is None or maxVal > found[0]:
                    found = (maxVal, maxLoc, r)
                    if maxVal >= thershold: 
                        print("money:", template['nominal'], "detected")

                if found is not None: 
                    (maxVal, maxLoc, r) = found
                    (startX, startY) = (int(maxLoc[0]*r), int(maxLoc[1] * r))
                    (endX, endY) = (
                        int((maxLoc[0] + tmp_width) * r), int((maxLoc[1] + tmp_height) * r))
                    if maxVal >= thershold:
                        cv2.rectangle(image_test, (startX, startY),
                                    (endX, endY), (0, 0, 255), 2)
                    cv2.imshow("Result", image_test)

            cv2.waitKey(0)


if __name__ == "__main__": 
    WM_Detection()

