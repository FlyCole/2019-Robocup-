
# import dlib
# import qi
# import cv2
# import sys
#
#
# def sit(img_name):
#     detector = dlib.get_frontal_face_detector()
#     print"detector succeed"
#     #img=img_name
#     img = cv2.imread(img_name)
#     rects = detector(img, 2)
#     ave = 0
#     sit_num = 0
#     stand_num = 0
#     count = 0
#
#     font = cv2.FONT_HERSHEY_SIMPLEX
#
#     #calculate total center average
#     if len(rects) != 0:
#         for rect in rects:
#             count += 1
#             ave += (rect.bottom()+rect.top()) / 2
#         ave = ave / count
#
#     #find  sitting  people num
#     count = 0
#
#     for rect in rects:
#         count += 1
#         if (rect.bottom() + rect.top()) / 2 > ave:
#             sit_num += 1
#             cv2.putText(img, 'sit', (rect.left() - 20, rect.top() - 20), font, 1.2, (255, 0, 0),
#                               2)
#             cv2.rectangle(img, (rect.left(), rect.top()), (rect.right(), rect.bottom()), (0, 0, 255), 2, 8)
#         else:
#             stand_num+=1
#             cv2.putText(img, 'stand', (rect.left() - 20, rect.top() - 20), font, 1.2, (255, 0, 0),
#                               2)
#             cv2.rectangle(img, (rect.left(), rect.top()), (rect.right(), rect.bottom()), (0, 0, 255), 2, 8)
#
#     cv2.imwrite("./sitting_person_detect.jpg", img)
#
#     print "The number of the sitting people is :", sit_num
#     print "The number of the standing people is :", stand_num
#     return sit_num, stand_num







import dlib
import qi
import cv2
import sys

def sit(img_name):
    detector = dlib.get_frontal_face_detector()
    print"detector succeed"
    img = cv2.imread(img_name)
    rects = detector(img, 2)
    ave = 0
    sit_num = 0
    stand_num = 0
    count = 0
    std = 0
    std_acc = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    if len(rects) != 0:
        for rect in rects:
            count += 1
            if (rect.bottom() + rect.top()) / 2 > 480 * 3 / 7:
                sit_num += 1
                cv2.putText(img, 'sit', (rect.left() - 20, rect.top() - 20), font, 1.2, (0, 0, 255), 4)
                cv2.rectangle(img, (rect.left(), rect.top()), (rect.right(), rect.bottom()), (0, 0, 255), 2, 8)
            else:
                stand_num += 1
                cv2.putText(img, 'stand', (rect.left() - 20, rect.top() - 20), font, 1.2, (0, 0, 255), 3)
                cv2.rectangle(img, (rect.left(), rect.top()), (rect.right(), rect.bottom()), (0, 0, 255), 2, 8)
    cv2.imwrite("./sitting_person_detect.jpg", img)
    print "The number of the sitting people is :", sit_num
    print "The number of the standing people is :", stand_num
    return sit_num, stand_num








