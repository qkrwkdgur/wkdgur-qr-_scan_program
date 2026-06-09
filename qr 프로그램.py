import pyzbar.pyzbar as pyzbar
import cv2
import os
import time

DATA_FILE = "qr_database.txt"

def load_qr_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

def save_all_qr_data(qr_list):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        for qr in qr_list:
            f.write(qr + "\n")
def append_qr_data(new_qr):
    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(new_qr + "\n")

TARGET_QR_DATA = load_qr_data()
print(f" 현재 파일에 저장된 QR 개수: {len(TARGET_QR_DATA)}개")

cap = cv2.VideoCapture(0)

is_finished = False  
delete_mode = False  

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        continue
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    decoded = pyzbar.decode(gray)
    if delete_mode:
        cv2.putText(img, "MODE: DELETE (f key pressed)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
    else:
        cv2.putText(img, "MODE: SCAN / REGISTER", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

    for d in decoded: 
        barcode_data = d.data.decode("utf-8")

        if delete_mode:
            if barcode_data in TARGET_QR_DATA:
                TARGET_QR_DATA.remove(barcode_data) 
                save_all_qr_data(TARGET_QR_DATA)        
                print(f"\n텍스트 파일에서 다음 QR을 삭제했습니다: {barcode_data}")
            else:
                print(f"\n 유효하지 QR입니다. ): {barcode_data}")
            
            cv2.imshow('QR Code Scanner', img)
            cv2.waitKey(1)
            time.sleep(3) 
            is_finished = True
            break
        else:
            if barcode_data in TARGET_QR_DATA:
                print(f"\n 이미 등록된 QR코드입니다. 데이터: {barcode_data}")
            else:
                TARGET_QR_DATA.append(barcode_data) 
                append_qr_data(barcode_data)          
                print(f"\n 새로운 QR코드가 파일에 저장되었습니다: {barcode_data}")
            cv2.imshow('QR Code Scanner', img) 
            cv2.waitKey(1)
            time.sleep(3) 
            is_finished = True
            break

    cv2.imshow('QR Code Scanner', img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or is_finished:
        break
    if key == ord('f'):
        delete_mode = True
    else:
        delete_mode = False

cap.release()
cv2.destroyAllWindows()
