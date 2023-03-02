# When had-read information(counter) needs

- 1.  when get whole chat list,
- 2.  when someone had read notifications

# How-to implement counter?

- 1. Create & Update
  - when someone had read notifications, get most-high number of chat id,
    and create read counter
- 2. Get or Send
  - when Someone read, broadcast to others

# Data hierarchy

```
(DB)
Counter : {
  channel : {channel},
    list : [
      {
         user : {user}
         most-recent readed chat : {chat}
      }
      ...
      ]
    }

(Return)
Form : {
    channel : {channel}
    list : [
    {since : {highest chat_id}
    count : number},
    {since : {second-highest chat_id}
    num : number-1},
    {since : {third-highest chat_id}
    num : number-2},
    ...
    ]
  }
```
