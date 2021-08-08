import random
import matplotlib.pyplot as plt 

key=[]
msg=[]

def get_randomness(a,b):     # compare 2 cipher_texts
	diff=[]

	for i in range(0,len(a)):
		diff.append(a[i]^b[i])   # so, len(diff)= len(msg)*11

	#print("diff: ",diff)	
	
	counter_array=[]
	for i in range(0,2048):      # pow(2,11)=2048
		counter_array.append(0)


	for i in range(0,len(diff)-11+1):
		cnt=0
		for j in range(0,11):
			cnt+=pow(2,11-j-1)*diff[(i+j)]
		#print("cnt: ",cnt)	
		counter_array[cnt]+=1	


	#print("counter_array: ",counter_array)	
		
	mean = sum(counter_array) / len(counter_array) 
	#print("mean: ",mean)
	variance = sum([((x - mean) ** 2) for x in counter_array]) / len(counter_array) 
	#print("variance: ",variance)
	D = variance ** 0.5		
	#print("D: ",D)
	C=len(counter_array)  # =2048
	N=len(diff)

	R=(D*C)/N

	return R


# val1 = int(input("Enter key length(a factor of 2048): "))
# for i in range(0,val1):
# 	key.append(random.randint(0,1))

# val2= int(input("Enter message length: "))
# for i in range(0,val2):
# 	msg.append(random.randint(0,1))

#print("Key: ",key)
#print("Message: ",msg)

def get_cipher_text(msg,key):
	print("msg: ",msg)
	S=[]
	for i in range(0,2048):
		S.append(i)

	T=[]
	mm=2048//len(key)
	for i in range(0,mm):
		for j in range(0,len(key)):
			T.append(int(key[j]))

	j=0
	for i in range(0,len(T)):	        # len(T)=len(S)=2048			
		j=(j+S[i]+T[i])%2048
		S[i],S[j]=S[j],S[i]

	j=0
	i=0

	keystream=[]
	for k in range(0,len(msg)):
		i=(i+1)%2048
		j=(j+S[i])%2048
		S[i],S[j]=S[j],S[i]
		t=(S[i]+S[j])%2048
		keystream.append(S[t])


	enc=[]
	for i in range(0,len(msg)):
		enc.append(int(msg[i])^keystream[i])
	print("enc: ",enc)	

	cipher_text=[]
	for i in range(0,len(enc)):
		x=len(bin(enc[i])[2:])
		for j in range(0,11-x):
			cipher_text.append(0)
		y=bin(enc[i])[2:]	
		for j in range(0,x):
			cipher_text.append(int(y[j]))

	##print("Encoded message: ",enc)
	print("cipher_text: ",cipher_text)
	##print("len(msg): ",len(msg))
	##print("len(cipher_text): ",len(cipher_text))


	S=[]
	for i in range(0,2048):
		S.append(i)

	T=[]
	mm=2048//len(key)
	for i in range(0,mm):
		for j in range(0,len(key)):
			T.append(int(key[j]))

	j=0
	for i in range(0,len(T)):	        # len(T)=len(S)=2048			
		j=(j+S[i]+T[i])%2048			# len(enc)=len(msg), but enc has big integers as elements
		S[i],S[j]=S[j],S[i]				# To handle that, as each element of enc <2-48 and 2048 has 12 bits, so , each element of 
										# enc is broken to corresponding 12 bits, and placed in cipher text. While decoding, enc
										# will be reformed from cipher_text by grouping together 12 consecutive bits of cipher_text												
	j=0
	i=0

	keystream=[]
	for k in range(0,len(msg)):
		i=(i+1)%2048
		j=(j+S[i])%2048
		S[i],S[j]=S[j],S[i]
		t=(S[i]+S[j])%2048
		keystream.append(S[t])


	dec=[]
	msg2=[]

	for i in range(0,len(msg)):
		num=0
		for j in range(0,11):
			num+=pow(2,11-j-1)*cipher_text[11*i+j]
		dec.append(num)		
		msg2.append(num^keystream[i])	


	print("Decrypted message: ",msg2)

	return cipher_text
	

msg_size_for_key_toggle=[1,3,6,23,93,745]
randomness_for_toggle_size_for_messages_sizes=[]
for k in range(0,6):
	randomness_for_toggle_size=[]   # has lists as elements. List corresponding to index i means toggle_size is (i+1). i can be from 0 to 31, corresponding to 1 toggle to 32 bit toggle.Each such list has 6000 entries of randomness.
	for k in range(1,33):
		randomness_for_toggle_size.append([])
	randomness_for_toggle_size_for_messages_sizes.append(randomness_for_toggle_size)	


for size in range(0,len(msg_size_for_key_toggle)):   # for different size messages
	msg=[]
	key=[]

	print("-------------------------------------------------------------------------------------------------")
 
	for i in range(0,50):             # for 300 such messages
		print("i: ",i)
		msg=[]

		for k in range(0,msg_size_for_key_toggle[size]):  
			msg.append(random.randint(0,1))

		for j in range(6,12):	
			key=[]
			for k in range(0,2**j):            # 6 different-sized keys
				key.append(random.randint(0,1))	
			
			for toggle_size in range(1,33):      
				key2=[]
				for f in range(0,len(key)):
					key2.append(key[f])
				#print("key: ",key)
				sub_size=len(key)//32        # always an integer. key is broken into 32 sub-parts, each of sub_size length
				for k in range(0,toggle_size):
					key2[sub_size*k]=key2[sub_size*k]^1	
				
				# kk=0
				# for h in range(0,len(key)):
				# 	if(key[h]!=key2[h]):
				# 		kk+=1

						
				print("")			
				print("message_size: ",msg_size_for_key_toggle[size])
				print("key size: ",len(key))
				print("toggle_size: ",toggle_size)
				#print("kk: ",kk)

				#print("key1: ",key)
				#print("key2: ",key2)

				cipher1=get_cipher_text(msg,key)
				cipher2=get_cipher_text(msg,key2)

				print("cipher1: ",cipher1)
				print("cipher2: ",cipher2)
				ran=get_randomness(cipher1,cipher2)

				print("ran: ",ran)

				randomness_for_toggle_size_for_messages_sizes[size][toggle_size-1].append(ran)


print(len(randomness_for_toggle_size_for_messages_sizes))

for k in range(0,len(randomness_for_toggle_size_for_messages_sizes)):
	print("-----------")
	print(len(randomness_for_toggle_size_for_messages_sizes[k]))
	for j in range(0,len(randomness_for_toggle_size_for_messages_sizes[k])):
		print(len(randomness_for_toggle_size_for_messages_sizes[k][j]))



avg_list_of_messages=[]
for i in range(0,len(randomness_for_toggle_size_for_messages_sizes)):  # 6
	avg_list=[]
	for j in range(0,len(randomness_for_toggle_size_for_messages_sizes[i])):  # 32
		#print("len(randomness_for_toggle_size_for_messages_sizes[i][j]: ",len(randomness_for_toggle_size_for_messages_sizes[i][j]))
		x=sum(randomness_for_toggle_size_for_messages_sizes[i][j])/len(randomness_for_toggle_size_for_messages_sizes[i][j])                   # 
		avg_list.append(x)
	avg_list_of_messages.append(avg_list)

print("avg_list_of_messages: ",avg_list_of_messages)  # len is 6


toggle=[]
for i in range(1,33):
	toggle.append(i)

for i in range(0,len(avg_list_of_messages)):
	plt.plot(toggle,avg_list_of_messages[i],label=msg_size_for_key_toggle[i]*11)

plt.xlabel("No_of_toggles")
plt.ylabel("Randomness_score")

plt.title("Randomness of cipher_text with toggles in key bits in RC4")
plt.legend()

plt.show()



