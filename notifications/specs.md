1. 기능 이름: notification backend using websocket (django channels)
2. 구현 담당자: @ds1sqe
3. 작업 시작일: 2022-12-22
4. 작업 완료일: 2022-12-26 예상 /

## 만들어야 하는 notification model

- id는 자동으로 생성 됨으로 구현하지 않음.
- channel: 알림이 발생한 채널 이름. => django models ForeignField를 사용하면 id만 들어가니깐 field이름 자체는 channel로 넣고 client에게 전달 해 줄 때 channel_name을 전달 해 줌. nullable = true
- dm: user_id를 저장해 두고, client에 전달 해 줄때 dm-{user_name}으로 변환해서 보내줌. nullable =true
- has_read: client에 준 count 기준으로 notification 객체를 관리함. 예) count 5일때 client에서 확인 함 (has_read: True 값으로 서버에 보냄) => 백엔드에서는 has_read 처리를 해주고, 새로운 notification에 대해서는 새로운 notification 객체를 생성해야함. has_read가 false인 객체들만 모아서 (논리상 has_read가 true인 db row는 채널(dm)당 하나여야 함.) 뿌려주면 됨.

## 백엔드

1. 엔드포인트: websocket
2. `ws://api.xlack.kreimben.com/ws/notification/`
3. query, parameter, body등등 client 요구사항:
4. response 타입 (반드시 들어가야 하는 것들):
5. 기타 사항:
6. 연결하면 자신이 속해있는 모든 workspace의 notification을 받을 수 있음.
7. notification model 만들어서 구현하기.

response로

```
{
    "id": {notification_id},
    "channel_name": {channel_name}, # 만약 dm일 경우 dm-{user_name}
    "count": {count}, # db에 쌓인 has_read가 false인 notification row 수.
    "has_read": {boolean}
}
```

# request는 notification을 읽었다고 보내는 것이고, response로 남은 notification을 보내줌. (위 참조)

# response 받고 새로 화면에 뿌려줘야 함.

```
{
    "id": {notification_id},
    "has_read": true
}
```

ref
signal from django
=>

Logic

1. Model
1. Data

1. Method

1. Serializer
1. Field
1. relation
1. method?

1. Consumer
1. method

1. urls/endpoint

#
