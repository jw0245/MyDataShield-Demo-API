from rest_framework.response import Response
from rest_framework.decorators import api_view
import re
    
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
        name_l = list(name)
        name_l[1:] = '*' * (len(name_l) -1) 
        return''.join(name_l)

    # Vehicle number format processing
    def p_car_name(car_name):
        p_car = list(car_name)
        p_car[-4:] = '****'
        return ''.join(p_car)

    # Mobile number and customer number processing
    def p_phone(tel) :
        tel_re = re.compile(r'(\d{3})(\d{3,4})(\d{4})$')
        # Mobile number
        if tel_re.match(tel):
            return tel_re.sub('\g<1>\g<2>****',tel)

        # Customer information other than mobile phone number
        else :    
            num = list(tel)
            num[len(tel)//2:] = '*' * (len(tel) - len(tel)//2)
            return ''.join(num)

    # Pseudonymization of account numbers, card numbers and other payment methods
    def p_num(num):
        card_re = re.compile(r'(\d{16,19})$')
        account_re = re.compile(r'(\d{12,14})$')

        # card_num
        if card_re.match(num):
            a = list(num)
            a[5:-4] = '*' * (len(num)-9)
            return ''.join(a)
        # account_num
        elif account_re.match(num):
            a_list = list(num)
            a_list[4:-3] = '*' * (len(num)-7)
            return ''.join(a_list)
        # other payment methods
        else :
            a = list(num)
            a[len(a)//2 : ] = '*' * (len(num)-len(num) // 2)
            return ''.join(a)

    # adrress type data      
    def address(ads) :
        ads_re = re.compile(r'([ㄱ-ㅣ가-힣]+[\s]+[ㄱ-ㅣ가-힣]+'')')
        return ads_re.findall(ads)[0]

target_data = {
                'client_id' : pseudonymy.p_data,
                'client_secret' : pseudonymy.p_data,
                'account_num' : pseudonymy.p_num,
                'pp_id' : pseudonymy.p_data,
                'trans_id' : pseudonymy.p_num,
                'bon_num' : pseudonymy.p_num,
                'trans_memo' : pseudonymy.p_name,
                'repay_account' : pseudonymy.p_num,
                'card_num' : pseudonymy.p_num,
                'account_name' : pseudonymy.p_name,
                'account_id' : pseudonymy.p_name,
                'charge_account_num' : pseudonymy.p_num,
                'address' : pseudonymy.address,
                'car_num' : pseudonymy.p_car_name,
                'holder_name' : pseudonymy.p_name,
                'name' : pseudonymy.p_name
              }


def anonymization(processed, target_data, temp_dict):
        
    for key_r, value_r in processed.items():
        
        for key_p, value_p in target_data.items():
            if key_r == key_p:
                print(processed[key_r] +' -> ' + value_p(value_r))
                temp_dict[key_r] = value_p(value_r)
    return temp_dict

@api_view(["GET"])
def MydatashieldAPI(request):

    response_data = dict()
    anonymization(request.data, target_data, response_data)
   
    return Response(response_data)
