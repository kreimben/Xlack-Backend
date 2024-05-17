# Xlack
## 슬랙 클론 코딩 프로젝트
워크스페이스 및 소통 용도로 많이 쓰이는 슬랙을 클론 코딩 하였습니다.
백엔드는 django, django rest framework, django channels로 구현하였고, 프론트엔드는 restapi 및 websocket을 이용하여 react.js로 구현됐습니다.


## 기능 구현 중 어려웠던 사항
백엔드 구현 중 어려웠던 것으로 실시간 채팅 및 알림, 파일 업로드&다운로드 관리가 있었습니다.
실시간 채팅 자체는 웹소켓으로 구현하면 되지만 채팅을 쳤을 때 실시간으로 알림을 보내주는 시스템 구현에 어려움이 있었고,
이용자들이 플랫폼에 파일을 업로드 했을 때 그 파일을 어디서 어떻게 관리 할 것인지, 다운로드까지의 API 설계에 있어서 고민을 많이 했습니다.


## 전체 기능
* 워크스페이스별 채널 관리 (CRUD)
* 프로필 수정
* 채널info 수정
* 채널별 멤버 권한편집 및 수정
* 멘션 닉네임 자동완성
* History
* 실시간 채팅
* 채팅 북마크
* 실시간 알림(on off)
* 실시간 채팅 리액션
* 파일 드래그 앤 드롭 업로드/다운로드
* 유저 실시간 상태 설정

## 사용 라이브러리
* django
* mysqlclient
* djangorestframework
* drf-yasg[validation]
* channels
* channels_redis
* djangorestframework-simplejwt[crypto]
* dj-rest-auth[with_social]
* django-allauth
* django-storages
* django-silk

## 로그인 하는 방법
**깃헙 계정으로 로그인 합니다.**

<img src="https://github.com/Team-Discipline/Xlack-Frontend/assets/85392646/4da7ae26-3980-4002-b8b1-dc0302a40f5a" width="80%" height="45%">

## 워크스페이스 추가하기
<img src="https://github.com/Team-Discipline/Xlack-Frontend/assets/85392646/96a54c99-66e4-465b-b025-96bd97de0e9a" width="80%" height="45%">


# 채널
## 워크스페이스에 채널을 추가하는 법
<img src="https://github.com/Team-Discipline/Xlack-Frontend/assets/85392646/48fdcd1b-5842-40d7-abf0-36bcf8928ade" width="80%" height="45%">


## 채널에 멤버를 추가하는 법
<img src="https://github.com/Team-Discipline/Xlack-Frontend/assets/85392646/154c8b0e-9b7f-4a21-a223-13f8f8db1d76" width="80%" height="45%">


## 채널 정보를 수정하는 법
<img src="https://github.com/Team-Discipline/Xlack-Frontend/assets/85392646/4d2f7ac0-a6e2-4ee1-84ac-8ba5cb00be78" width="80%" height="45%">


## 채널을 삭제하는 법
<img src="https://github.com/Team-Discipline/Xlack-Frontend/assets/85392646/804999a3-befe-40d1-a8bf-465876e7c28e" width="80%" height="45%">


# 채팅

## 리얼타임 채팅
### 기능 설명
- 채팅 북마크 (즐겨찾기)
- 북마크 확인하기
- 리액션 추가
- 파일 업로드 & 다운로드

<img src="https://github.com/Team-Discipline/Xlack-Frontend/assets/85392646/34a237fd-9a6a-4669-802f-f33b22e2f0ea" width="80%" height="45%">


## 파일 업로드 & 다운로드
<img src="https://github.com/Team-Discipline/Xlack-Frontend/assets/85392646/c77a5f35-74c0-4cbe-880e-2a687c46ba86" width="80%" height="45%">

# 알림
## 실시간 채팅 알림
### 기능 설명
- 팝업 알림
- 읽지않은 채팅 기능
- 알림 클릭 시 채널로 이동
- 알림 중지 기능

<img src="https://github.com/Team-Discipline/Xlack-Frontend/assets/85392646/65603bc1-5a35-4824-b3a9-6a036345249b" width="80%" height="45%">

# 프로필
### 기능 설명
- 모달 액션으로 구현
- 자신의 정보 (이름, 전화번호, 이메일 등등)
- 지금 상태
- 수정 기능
- 알림 중지 기능 설정을 프로필에서 설정 가능함

## 프로필 수정하는 방법
<img src="https://github.com/Team-Discipline/Xlack-Frontend/assets/85392646/184f0184-f814-4280-9665-bf80cc32c52a" width="80%" height="45%">

# 상태
### 기능 설명
- 더블 모달 액션으로 구현
- 상태 아이콘, 메세지, 알림 중지 기간 설정 가능
  
## 상태 수정하는 방법
<img src="https://github.com/Team-Discipline/Xlack-Frontend/assets/85392646/6ce33964-3375-4403-95f9-84e1faffb59d" width="80%" height="45%">
