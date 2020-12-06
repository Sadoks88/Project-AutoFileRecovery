SOF_list=[match.start() for match in re.finditer(re.escape(PDF1_SOF),data)]
EOF_list1=[match.start() for match in re.finditer(re.escape(PDF1_EOF),data)]
EOF_list2=[match.start() for match in re.finditer(re.escape(PDF2_EOF),data)]
EOF_list3=[match.start() for match in re.finditer(re.escape(PDF3_EOF),data)]
EOF_list4=[match.start() for match in re.finditer(re.escape(PDF4_EOF),data)]
i = 0
for SOF in SOF_list:
    for EOF1 in EOF_list1:
            for EOF2 in EOF_list2:
                if int(EOF1)<int(EOF_list2[i]) and int(EOF2) < int(SOF_list[i]):
                    for EOF3 in EOF_list3:
                        if int(EOF2)<int(EOF_list3[i]) and int(EOF3) < int(SOF_list[i+1]):
                            for EOF4 in EOF_list4:
                                if int(EOF3)<int(EOF_list4[i]) and int(EOF4) < int(SOF_list[i+1]):
                                    subdata=data[SOF:EOF4]
                                    carve_filename="file"+ str(filecounter) + ".pdf Start Offset: 0x" + str(SOF)+ " End Offset: 0x" + str(EOF4)
                                    filename="file"+ str(filecounter) + "_"+str(SOF)+"_"+str(EOF4)+"pdf" 
                                    #carve_obj=open(filename,'wb')
                                    #carve_obj.write(subdata)
                                    #carve_obj.close()
                                    #i=i+1  
                                    print(carve_filename)
                                    #hash(carve_filename)
                                    filecounter += 1
                                    break
                        else:
                            i+=1
                            subdata=data[SOF:EOF3]
                            carve_filename="file"+ str(filecounter) + ".pdf Start Offset: 0x" + str(SOF)+ " End Offset: 0x" + str(EOF3)
                            filename="file"+ str(filecounter) + "_"+str(SOF)+"_"+str(EOF3)+"pdf" 
                            #carve_obj=open(filename,'wb')
                            #carve_obj.write(subdata)
                            #carve_obj.close()
                            #i=i+1  
                            print(carve_filename)
                            #hash(carve_filename)
                            filecounter += 1
                            break 
                else:
                    subdata=data[SOF:EOF2]
                    carve_filename="file"+ str(filecounter) + ".pdf Start Offset: 0x" + str(SOF)+ " End Offset: 0x" + str(EOF2)
                    filename="file"+ str(filecounter) + "_"+str(SOF)+"_"+str(EOF2)+"pdf" 
                    #carve_obj=open(filename,'wb')
                    #carve_obj.write(subdata)
                    #carve_obj.close()
                    #i=i+1  
                    print(carve_filename)
                    #hash(carve_filename)
                    filecounter += 1
                    break
        else:
            subdata=data[SOF:EOF1]
            carve_filename="file"+ str(filecounter) + ".pdf Start Offset: 0x" + str(SOF)+ " End Offset: 0x" + str(EOF1)
            filename="file"+ str(filecounter) + "_"+str(SOF)+"_"+str(EOF1)+"pdf" 
            #carve_obj=open(filename,'wb')
            #carve_obj.write(subdata)
            #carve_obj.close()
            #i=i+1  
            print(carve_filename)
            #hash(carve_filename)
            filecounter += 1
            break                  
