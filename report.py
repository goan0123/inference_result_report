from PIL import Image, ImageDraw
import os
from pathlib import Path


img_ext = ["jpg", "gif", "bmp", "tif", "png", "jpeg"]


def get_txt_list(dir):
    #지정한 directory 속 텍스트 파일 이름을 저장한 list 반환
    list=[]
    label_list=os.path.join(dir,"labels")
    if os.path.exists(label_list):
        dir=label_list
    else:
        pass
    for files in os.listdir(dir):
        if files.endswith(r".txt") : #and not files=="classes.txt"
            list.append(files)
    return list

def get_img_list(dir):
    #지정한 directory 속 이미지 파일 이름을 저장한 list 반환
    list=[]
    for files in os.listdir(dir):
        for ext in img_ext:
            if files.endswith(ext) or files.endswith(ext.upper()):
                list.append(files)
    return list


def get_valid_list(txt_list, img_list):
    # 텍스트 파일과 이미지 파일의 이름을 비교하여 같은 이름이 존재하는 파일만 list에 저장하여 반환
    new_txt_list, new_img_list=[], []

    for img in img_list:
        for txt in txt_list:
            txt_path=Path(txt)
            img_path=Path(img)
            if img_path.stem==txt_path.stem:
                new_txt_list.append(txt)
                new_img_list.append(img)
            
    return new_txt_list, new_img_list



def get_list(dir_original, dir_result):
    # 원본 및 결과 directory를 지정하면 위에서 설명한 함수를 사용함
    # 각 폴더의 텍스트 및 이미지 list를 생성하고 반환
    label_txt=get_txt_list(dir_original)
    label_img=get_img_list(dir_original)
    result_txt=get_txt_list(dir_result)
    result_img=get_img_list(dir_result)


    list_original, list_original_img=get_valid_list(label_txt, label_img)

    result_img=[img for img in result_img if img in list_original_img]

    list_result, list_result_img=get_valid_list(result_txt, result_img)

    return list_original, list_original_img, list_result, list_result_img



def report_no_detect(list_original, list_result):
    no_detect_file=len(list_original)-len(list_result)

    #if no_detect_file < 0  -> error

    if no_detect_file > 0:
        
        #print("can't find ",no_detect_file," file(s).")

        for i in range(no_detect_file):
            list_result.append(0)
        
        for i in range(len(list_result)):
            if list_result[i] != list_original[i]:
                list_result.insert(i,0)
                list_result.pop()

    return no_detect_file, list_result
    



def split_data(list, dir):
    data_list=[]

    for file_name in list:
        label_list=os.path.join(dir,"labels")
        if os.path.exists(label_list):
            dir=label_list
            
        else:
            pass

        if file_name != 0:
            file_name=os.path.join(dir, file_name)
            f0=open(file_name,'r', encoding="utf-8")
            list1=f0.read().split("\n")
            f0.close()
            try:
                list1.remove("")    # yolo label always end with "\n" so that last elements is always ""
            except:
                pass
            list2=[[float(val) for val in subs.split()] for subs in list1]

            data_list.append(list2)
        else:
            data_list.append(0)
    
    return data_list


def get_classes(dir_original):
    classes_txt=os.path.join(dir_original,"classes.txt")
    if os.path.exists(classes_txt):
        with open(classes_txt, "r", encoding="utf-8") as f3:
            f_classes=f3.read()

        predefined_class=f_classes.split("\n")
        predefined_class.remove("") 
    else:
        predefined_class=['camera', 'scan', 'monitor', 'printer']

    return predefined_class


class Square():

    def __init__(self, list1, total_width, total_height):
        self.list = list1
        self.point_center_x, self.point_center_y, self.width_frac, self.height_frac =list1[1],list1[2],list1[3],list1[4]
        
        self.x1=(self.point_center_x - self.width_frac/2)*total_width
        self.x2=(self.point_center_x + self.width_frac/2)*total_width
        self.y1=(self.point_center_y - self.height_frac/2)*total_height
        self.y2=(self.point_center_y + self.height_frac/2)*total_height

        self.coord1=(self.x1, self.y1)
        self.coord2=(self.x2, self.y2)

        self.square=[self.x1, self.y1, self.x2, self.y2]

        self.width=self.x2-self.x1
        self.height=self.y2-self.y1
        self.area=self.width*self.height


    def draw_rec(self, img_draw, rec_color):
        
        img_draw.rectangle([self.coord1, self.coord2], outline=rec_color, width=5)


def overlap_area(square1, square2):

    [x1_1, y1_1, x2_1, y2_1] = square1.square
    [x1_2, y1_2, x2_2, y2_2] = square2.square

    overlap_area=0

    if x1_1>x1_2:
        x1=x1_1
    else:
        x1=x1_2

    if x2_1>x2_2:
        x2=x2_2
    else:
        x2=x2_1

    if y1_1>y1_2:
        y1=y1_1
    else:
        y1=y1_2

    if y2_1>y2_2:
        y2=y2_2
    else:
        y2=y2_1

    if x2>x1 and y2>y1:
        overlap_area=(x2-x1)*(y2-y1)
    else:
        pass

    return overlap_area


def define_dir_report(dir_result):
    dir_report=os.path.join(dir_result,"report")
    dir_temp=dir_report
    index=1
    while os.path.exists(dir_temp):
        if os.path.exists(dir_temp):
            index+=1
            dir_temp=dir_report+str(index)
        else:
            break

    dir_report=dir_temp

    return dir_report

def make_dir_report(dir_report):
    os.makedirs(dir_report)


def report(dir_original, dir_result):
    # report용 directory를 생성
    dir_report=define_dir_report(dir_result)
    make_dir_report(dir_report)

    # 각 directory에서 이미지 및 텍스트 list 추출
    list_original, list_original_img, list_result, _=get_list(dir_original, dir_result)

    # detection 없는 list 추출 및 print
    no_detect_file, list_result=report_no_detect(list_original, list_result) #[1,1,0,0,1,1,...] 1:image name

    # label 텍스트 파일 속 각 행마다 자르고, 그 행을 다시 분리함
    label_data_list=split_data(list_original, dir_original)
    result_data_list=split_data(list_result, dir_result)


    #########comparision

    predefined_class=get_classes(dir_original)

    report="file name, correct, incorrect, miss, class_right, class_miss\n"
    report2="file name, original_class, detected_ class, O/X\n"
    report_file="total_report.csv"
    report_file2="class_report.csv"
    report_path=os.path.join(dir_report, report_file)
    report_path2=os.path.join(dir_report, report_file2)
    f1=open(report_path, "w", encoding="utf-8")
    f2=open(report_path2, "w", encoding="utf-8")


    rate=0.7
    
    #total_correct=[]
    #total_incorrect=[]
    total_miss=[]
    total_rate_correct=[]
    total_rate_incorrect=[]
    total_rate_miss=[]

    total_class_right_or_not=[]
    total_report2=[]


    for i in range(len(list_original_img)):    #47
        
        file_name=list_original_img[i] 
        report+=file_name+","
        
        if list_original[i] == list_result[i]: # if file_names are the same, not 0
            img_name=list_original_img[i] #img_name_path=Path(img_name)
            img_path=os.path.join(dir_result, img_name) #dir_original => color x
            img = Image.open(img_path)
            img_draw = ImageDraw.Draw(img)

            total_width=img.width
            total_height=img.height

            correct=0
            incorrect=0
            miss=0
            
            class_miss=0
            class_right=0

            label_i_copy=label_data_list[i].copy()

            for j in range(len(label_data_list[i])): #0,0
                label1=label_data_list[i][j]

                square1=Square(label1, total_width, total_height)
                
                for k in range(len(result_data_list[i])): # (0,0) ~ (0,k)
                    label2=result_data_list[i][k]

                    square2=Square(label2, total_width, total_height)

                    condition1=(square1.area*rate<overlap_area(square1, square2))
                    condition2=(label1[0] == label2[0])
                    ox=""

                    
                    if condition1 : 
                        if condition2:
                            ox="O"
                            class_right+=1
                        else:
                            ox="X"
                            class_miss+=1

                        
                        total_report2.append([file_name, str(predefined_class[int(label1[0])]), str(predefined_class[int(label2[0])]),ox])
                        total_class_right_or_not.append(ox)
                        square2.draw_rec(img_draw,"green")
                        
                        result_data_list[i][k]=[-1 for nums in result_data_list[i][k]]
                        label_i_copy[j]=0
                        
                        correct+=1
                    else:
                        square2.draw_rec(img_draw,"blue")

            
            for label in label_i_copy:
                if label!=0:
                    square=Square(label, total_width, total_height)
                    square.draw_rec(img_draw,"black")
                    miss+=1
                    total_report2.append([file_name, predefined_class[int(label[0])], "none", "X"])
                    
            save_name=img_name
            save_path=os.path.join(dir_report,save_name)
            

            img.save(save_path)
            img.close()

            incorrect=len(result_data_list[i])-correct
            
            
            total_miss.append(miss)
            #total_correct.append(correct)
            #total_incorrect.append(incorrect)
            total_rate_correct.append(correct/(correct+incorrect+miss))
            total_rate_incorrect.append(incorrect/(correct+incorrect+miss))
            total_rate_miss.append(miss/(correct+incorrect+miss))
            
            report+=str(correct)+ ","+str(incorrect)+","+str(miss)+","+ str(class_right)+","+str(correct-class_right)+"\n"
            
        
        
        else:
            report+="none,none,none,none, none\n"
        

    miss_0=total_miss.count(0)
    miss_exist=len(list_original)-miss_0

    success=str(round(miss_0/len(list_original),4)*100)+"%"
    fail=str(round(miss_exist/len(list_original),4)*100)+"%"
    
    def avr_list(list1):
        result=0
        
        for ele in list1:
            result+=ele

        return round(result/len(list1),4)
    
    result_cor=str(avr_list(total_rate_correct)*100)+"%"
    result_incor=str(avr_list(total_rate_incorrect)*100)+"%"
    result_miss=str(avr_list(total_rate_miss)*100)+"%"

    total_o=[ele for ele in total_class_right_or_not if ele=="O"]


    report+="\n\ntotal, no_detect_file, success(no miss), fail, correct, incorrect, miss\n"
    report+=str(len(list_original))+ ","+ str(no_detect_file)+ ","+success + "," + fail+ "," + result_cor+ "," + result_incor+ "," + result_miss

    for list1 in total_report2:
        
        report2+=str(list1[0])+ "," +str(list1[1])+ "," +str(list1[2])+ "," +str(list1[3])+ "\n" 
            


    report2+="\n\ndetected_class_total, class_success,  class_success_rate\n"
    report2+=str(len(total_class_right_or_not)) + ","+str(len(total_o)) + ","+str(round(len(total_o)/len(total_class_right_or_not),4)*100)+ "%"

    f1.write(report)
    f2.write(report2)
    f1.close()
    f2.close()

    print("Results saved in: ", dir_report,"\n")

    return dir_report,report


# END OF DEFINITION

'''

#코드로 reporting tool을 사용하고 싶을 때 예시

dir_original=r"E:\Works\origin_label"
dir_result=r"E:\Works\result_label"

dir_report, report=report(dir_original, dir_result)

'''
