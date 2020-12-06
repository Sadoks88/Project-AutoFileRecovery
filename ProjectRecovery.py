import re
import hashlib
import struct
import binascii
import ast

#This section we get to establish the
#file signature and file footers
#

JPG_SOF = b'\xFF\xD8\xFF\xE0'
JPG_EOF = b'\xFF\xD9'
PNG_SOF = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
PNG_EOF = b'\x49\x45\x4E\x44\xAE\x42\x60\x82'
DOCX_SOF =b'\x50\x4B\x03\x04\x14\x00\x06\00'
DOCX_EOF = b'\x50\x4B\x05\x06'
BMP_SOF = b'\x42\x4D'
BMP_EOF = b'\x00\x00\x00\x00'
PDF1_SOF = b'\x25\x50\x44\x46'
PDF1_EOF = b'\x0A\x25\x25\x45\x4F\x46'
PDF2_EOF = b'\x0D\x0A\x25\x25\x45\x4F\x46\x0D\x0A'
PDF3_EOF = b'\x0D\x25\x25\x45\x4F\x46\x4D'
PDF4_EOF = b'\x0A\x25\x25\x45\x4F\x46\x0A'
GIF_SOF = b'\x47\x49\x46\x38\x39\x61'
GIF_EOF = b'\x00\x3B'
AVI_SOF = b'\x52\x49\x46\x46'
AVI_EOF = b'\x41\x56\x49\x20'
MGP_SOF = b'\x00\x00\x01\xBA'
MGP_EOF = b'\x00\x00\x01\xB7'
filecounter = 1



#This is the hashing encryption method
def hash(file):
    with open(file, "rb") as i:
        # read entire file as bytes
        bytes = i.read()
        readable_hash = hashlib.sha256(bytes).hexdigest()
        print("SHA-256: " + readable_hash + '\n')
        print("\n")

##
##HERE IS WHERE THE MAGIC HAPPENS
file_obj = open(input("Enter file name: "), 'rb')
print("")
data = file_obj.read()
file_obj.close()

##We begin with JPG
##the headers are in one list and the footers are in another
SOF_list=[match.start() for match in re.finditer(re.escape(JPG_SOF),data)]
EOF_list=[match.start() for match in re.finditer(re.escape(JPG_EOF),data)]
i = 0
##We kind of 
for SOF in SOF_list:
    for EOF in EOF_list:
        if int(SOF) < int(EOF):
            subdata=data[SOF:EOF]
            carve_filename="file"+ str(filecounter) + ".jpg Start Offset: 0x" + str(SOF)+ " End Offset: 0x" + str(EOF)
            filename="file" + str(filecounter) +".jpg" 
            carve_obj=open(filename,'wb')
            carve_obj.write(subdata)
            carve_obj.close()
            i=i+1  
            print(carve_filename)
            hash(filename)
            filecounter += 1
            break

SOF_list=[match.start() for match in re.finditer(re.escape(PNG_SOF),data)]
EOF_list=[match.start() for match in re.finditer(re.escape(PNG_EOF),data)]
i = 0
for SOF in SOF_list:
    for EOF in EOF_list:
        if int(SOF) < int(EOF):
            subdata=data[SOF:EOF]
            carve_filename="file"+ str(filecounter) + ".png Start Offset: 0x" + str(SOF)+ " End Offset: 0x" + str(EOF)
            filename="file"+ str(filecounter) +".png" 
            carve_obj=open(filename,'wb')
            carve_obj.write(subdata)
            carve_obj.close()
            i=i+1  
            print(carve_filename)
            hash(filename)
            filecounter += 1
            break
        
            
SOF_list=[match.start() for match in re.finditer(re.escape(MGP_SOF),data)]
EOF_list=[match.start() for match in re.finditer(re.escape(MGP_EOF),data)]
i = 0
for SOF in SOF_list:
    for EOF in EOF_list:
        if int(SOF) < int(EOF):
            subdata=data[SOF:EOF]
            carve_filename="file"+ str(filecounter) + ".mgp Start Offset: 0x" + str(SOF)+ " End Offset: 0x" + str(EOF)
            filename="file"+ str(filecounter)+".mgp" 
            carve_obj=open(filename,'wb')
            carve_obj.write(subdata)
            carve_obj.close()
            i=i+1  
            print(carve_filename)
            hash(filename)
            filecounter += 1
            break

SOF_list=[match.start() for match in re.finditer(re.escape(DOCX_SOF),data)]
EOF_list=[match.start() for match in re.finditer(re.escape(DOCX_EOF),data)]
EOF_list_reverse = EOF_list.reverse()
i = 0
j = 0
while i < len(SOF_list):
    for EOF in EOF_list:
        subdata=data[SOF_list[i]:EOF+18]
        carve_filename="file"+ str(filecounter) + ".docx Start Offset: 0x" + str(SOF_list[i])+ " End Offset: 0x" + str(EOF + 18)
        filename="file"+ str(filecounter) +".docx" 
        carve_obj=open(filename,'wb')
        carve_obj.write(subdata)
        carve_obj.close()
        i=i+1  
        print(carve_filename)
        hash(filename)
        filecounter += 1
        break
    break


SOF_list = [match.start() for match in re.finditer(b'RIFF',data)]
if not SOF_list:
    SOF_list=[match.start() for match in re.finditer(re.escape(AVI_SOF),data)]
EOF_list = [match.start() for match in re.finditer(b'AVI',data)]
if not SOF_list:
    EOF_list=[match.start() for match in re.finditer(re.escape(AVI_EOF),data)]
i = 0
for SOF in SOF_list:
    for EOF in EOF_list:
        if int(SOF) < int(EOF):
            size=data[SOF+4:EOF]
            hi, mid, midone, lo = struct.unpack('<BBBB', size)
            hi = hex(hi)
            mid = hex(mid)
            midone = hex(midone)
            lo = hex(lo)
            n = lo + midone + mid + hi
            n = n.replace("0x","")
            size = int(n,16)
            subdata=data[SOF:SOF + size]
            carve_filename="file"+ str(filecounter) + ".avi Start Offset: 0x" + str(SOF)+ " End Offset: 0x" + str(EOF)
            filename="file"+ str(filecounter) +"avi" 
            carve_obj=open(filename,'wb')
            carve_obj.write(subdata)
            carve_obj.close()
            i=i+1  
            print(carve_filename)
            hash(filename)
            filecounter += 1
            break

SOF_list=[match.start() for match in re.finditer(re.escape(GIF_SOF),data)]
EOF_list=[match.start() for match in re.finditer(re.escape(GIF_EOF),data)]
i = 0
for SOF in SOF_list:
    for EOF in EOF_list:
        if int(SOF) < int(EOF):
            subdata=data[SOF:EOF]
            carve_filename="file"+ str(filecounter) + ".gif Start Offset: 0x" + str(SOF)+ " End Offset: 0x" + str(EOF)
            filename="file"+ str(filecounter) +"gif" 
            carve_obj=open(filename,'wb')
            carve_obj.write(subdata)
            carve_obj.close()
            i=i+1  
            print(carve_filename)
            hash(filename)
            filecounter += 1
            break

SOF_list=[match.start() for match in re.finditer(re.escape(BMP_SOF),data)]
EOF_list=[match.start() for match in re.finditer(re.escape(BMP_EOF),data)]
i=0
previousfooter=0
for SOF in SOF_list:
    checker=data[SOF+6:SOF+10]
    hi, mid, midone, lo = struct.unpack('<BBBB', checker)
    hi = hex(hi)
    mid = hex(mid)
    midone = hex(midone)
    lo = hex(lo)
    n = lo + midone + mid + hi
    #print(n)
    n = n.replace("0x","")
    check = int(n,16)
    if check == 0:
        if (int(SOF) > previousfooter):
            try:
                size=data[SOF+2:SOF+6]
                hi, mid, midone, lo = struct.unpack('<BBBB', size)
                hi = hex(hi)
                mid = hex(mid)
                midone = hex(midone)
                lo = hex(lo)
                n = lo + midone + mid + hi
                n = n.replace("0x","")
                size = int(n,16)
                previousfooter = int(SOF) + size
                subdata=data[SOF:SOF + size]
                carve_filename="file"+ str(filecounter) + ".bmp Start Offset: 0x" + str(SOF)+ " End Offset: 0x" + str(size)
                filename="file"+ str(filecounter) + "bmp" 
                carve_obj=open(filename,'wb')
                carve_obj.write(subdata)
                carve_obj.close()  
                print(carve_filename)
                hash(filename)
                filecounter += 1
                break
            except struct.error:
                break
    #i += 1
    #print("i: " + str(i))

   


SOF_list=[match.start() for match in re.finditer(re.escape(PDF1_SOF),data)]
EOF_list1=[match.start() for match in re.finditer(re.escape(PDF1_EOF),data)]
EOF_list2=[match.start() for match in re.finditer(re.escape(PDF2_EOF),data)]
EOF_list3=[match.start() for match in re.finditer(re.escape(PDF3_EOF),data)]
EOF_list4=[match.start() for match in re.finditer(re.escape(PDF4_EOF),data)]
i = 0


for SOF in SOF_list:
    for EOF1 in EOF_list1:
        for EOF2 in EOF_list2:
            for EOF3 in EOF_list3:
                for EOF4 in EOF_list4:
                    if int(EOF3) < int(EOF4) and int(EOF4) < int(SOF_list[i+1]):
                        subdata=data[SOF:EOF4]
                        carve_filename="file"+ str(filecounter) + ".pdf Start Offset: 0x" + str(SOF)+ " End Offset: 0x" + str(EOF4)
                        filename="file"+ str(filecounter) +".pdf" 
                        carve_obj=open(filename,'wb')
                        carve_obj.write(subdata)
                        carve_obj.close()
                        i=i+1  
                        print(carve_filename)
                        hash(filename)
                        filecounter += 1
                        i+=1
                        break
                try:    
                    if int(EOF2) < int(EOF3) and int(EOF3) < int(SOF_list[i+1]):
                        subdata=data[SOF:EOF2]
                        carve_filename="file"+ str(filecounter) + ".pdf Start Offset: 0x" + str(SOF)+ " End Offset: 0x" + str(EOF3)
                        filename="file"+ str(filecounter)+".pdf" 
                        carve_obj=open(filename,'wb')
                        carve_obj.write(subdata)
                        carve_obj.close()
                        i=i+1  
                        print(carve_filename)
                        hash(filename)
                        filecounter += 1
                        i+=1
                        break
                except IndexError:
                    exit()
            try:    
                if int(EOF1) < int(EOF2) and int(EOF2) < int(SOF_list[i+1]):
                    subdata=data[SOF:EOF2]
                    carve_filename="file"+ str(filecounter) + ".pdf Start Offset: 0x" + str(SOF)+ " End Offset: 0x" + str(EOF2)
                    filename="file"+ str(filecounter)+".pdf" 
                    carve_obj=open(filename,'wb')
                    carve_obj.write(subdata)
                    carve_obj.close()
                    i=i+1  
                    print(carve_filename)
                    hash(filename)
                    filecounter += 1
                    i+=1
                    break
            except IndexError:
                exit()
        if int(SOF) < int(EOF1):
            subdata=data[SOF:EOF1]
            carve_filename="file"+ str(filecounter) + ".pdf Start Offset: 0x" + str(SOF)+ " End Offset: 0x" + str(EOF1)
            filename="file"+ str(filecounter) +".pdf" 
            carve_obj=open(filename,'wb')
            carve_obj.write(subdata)
            carve_obj.close()
            i=i+1  
            print(carve_filename)
            hash(filename)
            filecounter += 1
            i+=1
            break

