# MyDataShield-Demo-API
MyData Shield API는 마이데이터 서비스에 포함되어 있는 정보 주체의 개인 정보데이터를 가명/익명 처리하는 API입니다.

### MyData Shield API 활용
* 정보 주체의 개인 정보데이터가 서비스에 포함
* Restful 통신을 통해 Json 형태의 응답값을 받아 가명/익명처리
* Restful 통신을 통해 가명/익명처리 된 JSON 데이터 전송

### 외부 라이브러리
* Django
* django-cors-headers
* djangorestframework
* Faker 11.3.0

### 구성
* 초기 url에서 데모 화면을 통해 API 기능 테스트가능
* /mydata 의 주소를 통해 API 활용

### 기능 제공
* 마스킹을 통한 가명처리 방식
* 동적 Salt를 활용한 단방향 SHA256 암호화 방식 가명처리
* Faker 라이브러리를 사용한 가명처리
* Response_type 항목명 값에 따른 마스킹, 암호화, Faker 기능 제공('0' = Masking, '1' = 암호화, '2' = Faker)
* 
### 화면
![image](https://user-images.githubusercontent.com/61214962/163522671-3212b02e-b9f0-49d1-ad7e-d0616538bcc4.png)
![image](https://user-images.githubusercontent.com/61214962/163523833-436d059d-319f-4af0-be96-6c2cf716458c.png)
![image](https://user-images.githubusercontent.com/61214962/163523945-76b1c0aa-034f-43e1-852b-2d8fb2e674d0.png)
![image](https://user-images.githubusercontent.com/61214962/163523763-b2b8728d-d28a-46e8-be32-19c240825e64.png)

