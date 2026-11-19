import cv2, numpy as np
from PIL import Image, ImageFilter
src=cv2.imread('work/mockup.png')
img=src.copy()
def clean(img, boxes, fill_boxes):
    mask=np.zeros(img.shape[:2],np.uint8)
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    for (x0,y0,x1,y1) in boxes:
        sub=hsv[y0:y1,x0:x1]
        m=((sub[...,2]>150)&(sub[...,1]<170)).astype(np.uint8)*255  # light / gold text
        mask[y0:y1,x0:x1]|=m
    for (x0,y0,x1,y1) in fill_boxes: mask[y0:y1,x0:x1]=255
    mask=cv2.dilate(mask,np.ones((7,7),np.uint8))
    out=cv2.inpaint(img,mask,9,cv2.INPAINT_TELEA)
    blur=cv2.GaussianBlur(out,(0,0),14)
    bm=cv2.GaussianBlur(mask.astype(np.float32)/255,(0,0),10)[...,None]
    bm=np.clip(bm*1.4,0,1)
    return (out*(1-bm)+blur*bm).astype(np.uint8)
img=clean(img,
  [(75,175,590,345),(355,595,740,650),(283,650,805,682),(665,935,1015,1170)],
  [(195,322,300,342),(84,358,284,410),(296,358,484,410),(683,1078,843,1122)])
cv2.imwrite('work/clean.png',img)
def save(name,box,q=86):
    x0,y0,x1,y1=box
    c=Image.fromarray(cv2.cvtColor(img[y0:y1,x0:x1],cv2.COLOR_BGR2RGB))
    c=c.resize((c.width*2,c.height*2),Image.LANCZOS).filter(ImageFilter.UnsharpMask(2,60,3))
    c.save(f'img/{name}.jpg',quality=q,optimize=True,progressive=True)
save('hero-general-tso',(0,64,1086,428))
save('signature-plate',(0,612,480,884))
save('private-dining-room',(0,946,612,1180))
save('red-floral',(640,958,1086,1176))
