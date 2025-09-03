# shop-api

### django 실행 방법
#### 1. 실행 환경
- python 3.8
- django 2.2.24
- Django REST Framework
- SQLite
#### 2. 설치 및 설정
- 가상환경 생성 및 활성화
  ```
  python3.8 -m venv .venv
  source .venv\Scripts\activate  # Windows가 아닌 경우: .venv\bin\activate
  ```
- 패키지 설치
  ```
  pip install --upgrade pip
  pip install -r requirements.txt
  ```
- 데이터베이스 초기화
  ```
  python manage.py migrate
  ```
#### 3. 서버 실행
```
python manage.py runserver
```
http://127.0.0.1:8000 접속

---
### Docker 실행 방법
#### 1. 이미지 빌드
```
docker build -f dockerfile -t [docker 이미지 이름 부여]
```
#### 2. 컨테이너 실행
```
docker run -p 8000:8000 [docker 이미지 이름]
```
#### 3. docker-compose
```
docker-compose up --build
```
---
### URL 실행 방법
#### 1. API 루트
- http://localhost:8000/shop/products
#### 2. 관리자 페이지
- http://localhost:8000/admin/
#### 3. API 문서
- http://localhost:8000/doc/
