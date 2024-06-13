import math
import cv2
import cadquery as cq

points = []
reference_size = 242.5515409145034

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        cv2.circle(resized_image, (x, y), 2, (0, 0, 255), -1)  # 繪製紅色小點
        cv2.imshow("Image", resized_image)

image = cv2.imread(r" ")

# 縮小圖片
resized_image = cv2.resize(image, (851, 639))

cv2.namedWindow("Image")
cv2.setMouseCallback("Image", mouse_callback)
cv2.imshow("Image", resized_image)
cv2.waitKey(0)
print("儲存的點座標：")
for point in points:
    print(point)
cv2.destroyAllWindows()

ref_x_pixels = float(abs(points[0][0]-points[1][0]))
ref_y_pixels = float(abs(points[0][1]-points[1][1]))
ref_pixels = math.sqrt(ref_x_pixels**2 + ref_y_pixels**2)
print("pixels=",ref_pixels)
pixels_per_cm = ref_pixels/reference_size
print("pixelspercm=",pixels_per_cm)

v1height_pixels = abs(points[2][1]-points[3][1])
v1length_pixels = abs(points[2][0]-points[3][0])
v1ref_pixels = math.sqrt(v1length_pixels**2 + v1height_pixels**2)
v1 = v1ref_pixels/pixels_per_cm


print("height=",v1)

variable_height = v1

box1_length = 106.2757704572517
box1_width = 30
box1_height = 10
box2_length = 30
box2_width = 30
box2_height = variable_height
box3_length = 106.2757704572517
box3_width = 30
box3_height = 26

box2tranx = (abs(box1_length-box2_length)/2)+box2_length
box2tranz = ((box2_height-box1_height)/2)

box3tranx = (abs(box1_length-box3_length)/2)+box1_length+box2_length
box3tranz = ((box3_height-box1_height)/2)

cytranx = ((box1_length+box2_length)/2)
cytranz = box2_height-(box1_height/2)

# Create a CadQuery Workplane
result = cq.Workplane("XY")

# Generate the first box
box1 = result.box(box1_length, box1_width, box1_height)

# Generate the second box
box2 = result.box(box2_length, box2_width, box2_height).translate((box2tranx, 0, box2tranz))

# Generate the third box
box3 = result.box(box3_length, box3_width, box3_height).translate((box3tranx, 0, box3tranz))

cylinder = result.circle(2).extrude(10).translate((cytranx, 0, cytranz))

text1 = cq.Workplane("XY").text("length="+ str(box1_length+box2_length+box3_length)+" cm.",8, 1).translate((50,-55,-(box1_height/2)))
text2 = cq.Workplane("XY").text("heightl="+ str(box2_height)+" cm.",8, 1).translate((50,-70,-(box1_height/2)))

# Combine all the boxes
combined_boxes = box1.union(box2).union(box3).union(cylinder).union(text1).union(text2)

combined_boxes.val().exportStl(r"C:\Users\asus\Desktop\combined_boxes.stl")
