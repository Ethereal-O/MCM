
import cv2
import random
img = cv2.imread("./map.jpg") # 读取图片

points = [(39,299),(161,201),(257,285),(298,325),(310,450),(184,303),(165,371)]

for point in points:
    cv2.circle(img,point,2,(0,0,255),-1)
    
elephant_circle_points = [(82,275),(161,241),(185,331),(260,380)]
elephant_points = []

for point in elephant_circle_points:
    for i in range(100):
        elephant_points.append((int(point[0]+50*random.random()),int(point[1]+50*random.random())))
        
for point in elephant_points:
    cv2.circle(img,point,2,(0,0,255),-1)

# cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
# cv2.circle(输入的图片data,圆心位置,圆的半径,圆的颜色,圆形轮廓的粗细（如果为正）负数(-1)表示要绘制实心圆,圆边界的类型,中心坐标和半径值中的小数位数)

# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
# imgErode = cv2.dilate(gray, kernal, borderType=cv2.BORDER_CONSTANT, borderValue=0)
# canny = cv2.Canny(imgErode, 50, 150)
# cv2.imshow("canny", canny)
cv2.imshow("img",img)
cv2.waitKey()