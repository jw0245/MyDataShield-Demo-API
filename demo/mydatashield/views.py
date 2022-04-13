from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render
import re
import hashlib
import uuid
from faker import Faker

class pseudonymy :

    def p_data(data):
        # Data processing that is longer than 4 characters and has no special format
        if len(data) >= 4 :
            data_list = list(data)
            data_list[len(data) // 2 : - (len(data) // 4)] = '*' * (len(data) - (len(data) // 2 + len(data) // 4))
            return ''.join(data_list)

        # Data processing that is shorter than 4 characters and has no special format
        elif len(data) < 4 :
            data_list = list(data)
            data_list[len(data) // 2 :] = '*' * (len(data) - (len(data) // 2))
            return ''.join(data_list)
        
    # name pseudonymization function (All except last name are treated as *)
    def p_name(name) :
        if len(name) >= 2:
            name_l = list(name)
            name_l[1:] = '*' * (len(name_l) -1) 
            return''.join(name_l)
        else :
            return ''
   
    # Vehicle number format processing
    def p_car_num(car_num):
        if len(car_num) >= 4:
            p_car = list(car_num)
            p_car[-4:] = '****'
            return ''.join(p_car)
        else :
            return ''
    # Mobile number and customer number processing
    def p_phone(tel) :
        tel_re = re.compile(r'(\d{2,3})-(\d{3,4})-(\d{4})$')
        # Mobile number
        if tel_re.match(tel):
            return tel_re.sub('\g<1>-\g<2>-****',tel)

        # Customer information other than mobile phone number
        else :    
            num = list(tel)
            num[len(tel)//2:] = '*' * (len(tel) - len(tel)//2)
            return ''.join(num)

    # Pseudonymization of account numbers, card numbers and other payment methods
    def p_num(num):
        payment_re = re.compile(r'(\d{2,6})-(\d{2,6})-(\d{2,6})-(\d{2,4})$')
        account_re = re.compile(r'(\d{3,5})-(\d{2,6})-(\d{2,6})$')

        # card_num or account_num
        if payment_re.match(num):
            ac_s = num.split('-')
            result = ac_s[0] + '-' + len(ac_s[1])*'*' + '-' + ac_s[2] + '-' + len(ac_s[3])*'*'   
            return payment_re.sub('\g<1>-****-\g<3>-****',num)
        # account_num
        elif account_re.match(num):
            ac_s = num.split('-')
            result = ac_s[0] + '-' + len(ac_s[1])*'*' + '-' + len(ac_s[2])*'*'  
            return result
        # other payment methods
        else :
            a = list(num)
            a[len(a)//2 : ] = '*' * (len(num)-len(num) // 2)
            return ''.join(a)

    # adrress type data      
    def address(ads) :
        ads_re = re.compile(r'([ㄱ-ㅣ가-힣]+[\s]+[ㄱ-ㅣ가-힣]+'')')
        if ads_re.match(ads) :
            return ads_re.findall(ads)[0]
        else :
            return ''

class h_encryption :
    
    def __init__():
        return ''
    
    # 비 가역적인 가명처리 방법 sha256 이름과 계좌, 전화번호를 섞어서 만듬. sha256
    def comb_data(name, num):
        
        # 동적 salt 생성
        salt = uuid.uuid4().hex
        
        comb_data = name + '/' + num
        comb_h = hashlib.sha256(salt.encode() + comb_data.encode()).hexdigest()
        print(comb_data + ' -> SHA256 Convert ' + 'secret: ')
        print(comb_h)
        return comb_h
    
            
    def hashText(text):

        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + text.encode()).hexdigest()
        #+ ':' + salt
        
    # 가역적인 가명처리 방법 보안적으로 취약하며 키 관리 및 보안 유지가 필요함 

target_data = {
                'client_id' : pseudonymy.p_data,
                'client_secret' : pseudonymy.p_data,
                'account_num' : pseudonymy.p_num,
                'pp_id' : pseudonymy.p_data,
                'trans_id' : pseudonymy.p_num,
                'bond_num' : pseudonymy.p_num,
                'trans_memo' : pseudonymy.p_name,
                'repay_account_num' : pseudonymy.p_num,
                'card_num' : pseudonymy.p_num,
                'account_name' : pseudonymy.p_name,
                'account_id' : pseudonymy.p_name,
                'charge_account_num' : pseudonymy.p_num,
                'address' : pseudonymy.address,
                'car_number' : pseudonymy.p_car_num,
                'holder_name' : pseudonymy.p_name,
                'name' : pseudonymy.p_name,
                'pay_id' : pseudonymy.p_num,
                'trans_id' : pseudonymy.p_num,
                'insured_name' : pseudonymy.p_name,
                'telecom_num' : pseudonymy.p_num
              }

def anonymization(processed, target_data, temp_dict):
        
    for key_r, value_r in processed.items():
        
        for key_p, value_p in target_data.items():
            if key_r == key_p:
                print(processed[key_r] +' -> ' + value_p(value_r))
                temp_dict[key_r] = value_p(value_r)
    return temp_dict

def anonymization1(processed, target_data, temp_dict):
    
    # request.data
    if ('account_name' in processed.keys() and 'account_num' in processed.keys()):
        temp_dict['id'] = h_encryption.comb_data(processed['account_name'], processed['account_num'])
        del processed['account_name']
        del processed['account_num']
        
    if ('telecom_num' in processed.keys()):
        
        
        faker = Faker('ko_KR')
        temp_dict['telecom_num'] = faker.phone_number()
        del processed['telecom_num']

    for key_r, value_r in processed.items():
        
        for key_p, value_p in target_data.items():                
            if key_r == key_p:
                print(processed[key_r] +' -> ' + value_p(value_r))
                temp_dict[key_r] = value_p(value_r)
    return temp_dict


def Demo(request):
    return render(request,'Demo.html',{})

def old(request):
    return render(request,'old.html',{})

def old2(request):
    return render(request,'old2.html',{})


@api_view(["POST"])
def Mydatashield(request):

    response_data = dict()
    if request.data['Response_type'] == '0':
        anonymization(request.data, target_data, response_data)
    elif request.data['Response_type'] == '1':
        anonymization1(request.data, target_data, response_data)
    return Response(response_data)

   
