import struct

file = open("studentinfo.txt","rb")


#print(struct.unpack("!1b",file.read(1)))
#print(file.read(9).decode()[0])
#print(struct.unpack("!2b",file.read(2)))
#print(struct.unpack("!4b",file.read(4)))

num_kim = 0
sum_kim_age = 0
most_older_lee = 0
lee=''
num_id ={}

while 1:
   student_id = file.read(1)
   if not student_id:
      break;
   else:
      decoded_student_id = struct.unpack("!1b", student_id)

      name = file.read(9)
      decoded_name = name.decode()
     # print(decoded_name[0])

      grade = file.read(2)
      decoded_grade = struct.unpack("!2b", grade)

      age = file.read(4)
      decoded_age = struct.unpack("!4b", age)

      if decoded_name[0] == '김':
         num_kim = num_kim + 1
         sum_kim_age += decoded_age[3]
      if decoded_name[0] == '이':
         if decoded_age[3] > most_older_lee:
            most_older_lee=decoded_age[3]  	
            lee = decoded_name[0]+decoded_name[1]+decoded_name[2]
      if decoded_student_id[0] not in num_id.keys():
         num_id[decoded_student_id[0]] = 1
      else:
         num_id[decoded_student_id[0]] = int(num_id.get(decoded_student_id[0])) + 1      
          
   
average_kim_age = sum_kim_age / num_kim
print('김씨들의 평균 나이는? ', average_kim_age)
print('이씨들 중 나이가 제일 많은 사람은? ', lee)
print('각 한번 별 인원수는? ',num_id.items())
