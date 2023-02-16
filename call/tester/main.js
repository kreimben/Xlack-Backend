
// 1. get token from input
// 2. connect websocket
// 3. call or be called over server
// 4. exchange sdp over server
// 5. connect p2p

const websocket_url = "ws://127.0.0.1:8000/ws/call/"

const stun = { iceServers: [{
      urls: "stun:stun.l.google.com:19302"
    }]
}

let tokenInput = document.getElementById("login-token")
let tokenBtn = document.getElementById("login-btn")
let call = document.getElementById("call")
let callBtn = document.getElementById("call-btn")
let callBtnGroup = document.getElementById("call-btn-group")
let callBtnGroupInvite = document.getElementById("call-btn-group-invite")
let callId = document.getElementById("call-id")

let user_id = null
let token
let ws
let isAuthorized = false
let group = null
let peers = {}

let resentPeerConnection

tokenBtn.addEventListener('click',()=>{
  token = tokenInput.value;
  console.log("token:",token)
  console.log("ws:creating websocket connection")
  ws = new WebSocket(websocket_url)

  ws.addEventListener('open',(ev)=>
    console.log("ws:connection open")
  )
  ws.addEventListener('close',(ev)=>
    console.log("ws:connection close")
  )
  ws.addEventListener('error',(ev)=>
    console.log("ws:connection error")
  )
  ws.addEventListener('message',(ev)=>{
    if (isAuthorized == false) {
      wsAuthHandler(ev)
    } else {
      wsMessageHandler(ev)
    }
  })
  call.hidden= false
  callBtn.addEventListener("click",call_by_id)
  callBtnGroup.addEventListener("click",creategroup)
  callBtnGroupInvite.addEventListener("click",invite_by_id)
  }
)
function wsAuthHandler(event){
  let data = JSON.parse(event.data);
  console.log("ws:authrequest:",data)
  if (data['success'] == true) {
    isAuthorized = true
    user_id= data['user_id']
  }
  let t = {
    authorization : token
  }
  ws.send(JSON.stringify(t)) 
}

function wsMessageHandler(event){
  let data = JSON.parse(event.data);
  console.log("ws:message received:",data)

  let type = data['type']
  let req = data['request']
  let peer = data['peer']

  if (peer == user_id) {
    //ignore self generated msg
    return
  }

  if (req=="call.new") {
    // accept or reject call
    accept = confirm("Accept call from id:",peer," ?") 
    let answer = {
      target : peer
    }
    if (accept) {
      answer.request = 'call.accept'
    } else {
      answer.request = 'call.reject'
    }
    console.log("call answer:",answer)
    ws.send(JSON.stringify(answer))
  } else if (req=="call.accept") {
    console.log("handling:",req)
    console.log("creating Offer for",peer,group)
    createOffer(peer,group)
  } else if (req=="call.reject") {
    console.log("call rejected by:",peer)
    alert("Call rejected by id:",peer)

    // manage group
  } else if (req=="group.new"){
    console.log("converted to group call:",data['group'])
    alert("Converted to group call :",data['group'])
    group = data['group']
    
  } else if (req=="group.invite"){
    console.log("invited to group call:",data['group'])
    accept = confirm("Accept group call invite from id:" + peer +" ?") 
    let answer = {
      target : peer
    }
    if (accept) {
      answer.request = 'group.accept'
      group = data['group']
    } else {
      answer.request = 'group.reject'
    }
    ws.send(JSON.stringify(answer))
  } else if (req=="group.accept") {
    console.log(req)
    console.log(data)
    console.log(peer," accepted a group call:",data['group'])
    alert("Group call invitation has accepted by: "+ peer)
    createOffer(peer,group)
  } else if (req=="group.reject") {
    alert("Group call rejected by id:"+ peer)
  }
  else if (type=='sdp.offer') { // receive a call
    let offer = data['sdp']
    createAnswer(offer,data['peer'],group)
    return
  }
  else if (type=='sdp.answer') { // callee has answered
    let answer = data['sdp']
    let peer_id = data['peer']
    let peer = peers[peer_id][0] //array [peerConnection|data channel]
    console.log("setting remote description:",answer)
    peer.setRemoteDescription(answer)
    return
  } 
  else if (type=='ice.candidate') { // ice candidate info received
    const candidate = new RTCIceCandidate(data['candidate'])
    let peer_id = data['peer']
    let peer = peers[peer_id][0] //array [peerConnection|data channel]
    peer.addIceCandidate(candidate).catch((err)=>console.log(err))
  }
}


let localStream = new MediaStream();
let localVideo = document.getElementById("video-self")
let btnVideo = document.getElementById("video-btn-video")
let btnAudio = document.getElementById("video-btn-audio")

const constraints = {
  'local' : {
   'video' : true,
   'audio' : true
  },
}

function setLocalStream(){
  let localMedia = navigator.mediaDevices.getUserMedia(constraints.local)
      .then(stream => {
        localStream=stream;
        localVideo.srcObject = localStream;

        let vidTrack = stream.getVideoTracks();
        btnVideo.addEventListener("click",()=>{
        vidTrack[0].enabled= !vidTrack[0].enabled
        if (vidTrack[0].enabled) {
          btnVideo.innerHTML = "Hide Video"

        } else {
          btnVideo.innerHTML = "Turn On Video"
        }
        })

        let audTrack = stream.getAudioTracks();
        audTrack[0].enabled = false
        btnAudio.addEventListener("click",()=>{
        audTrack[0].enabled= !audTrack[0].enabled
        if (audTrack[0].enabled) {
          btnAudio.innerHTML = "Mute Audio"

        } else {
          btnAudio.innerHTML = "UnMute Audio"
        }
        })

      }).catch(error=>{
        console.log(error)
      })
}
setLocalStream()

function sendSignalSDP(type,target,sdp,group) {
  let t = {
    'type':type,
    'target':target,
    'sdp':sdp
  }
  if (group) {
    t.group = group
  }
  j = JSON.stringify(t)
  console.log("sendSignal:",j)
  ws.send(j)
}

function sendSignalCandidate(type,target,candidate,group) {
  let t = {
    'type':type,
    'target':target,
    'candidate':candidate
  }
  if (group) {
    t.group = group
  }
  j = JSON.stringify(t)
  console.log("sendSignal:",j)
  ws.send(j)
}

function createPeerConnection(){
  let peerConnection = new RTCPeerConnection(stun);
  addLocalTracks(peerConnection);
  return peerConnection
}

function createOffer(target,group){

  let peerConnection = new RTCPeerConnection()
  addLocalTracks(peerConnection)
  let dataChannel= peerConnection.createDataChannel('data_channel')

  dataChannel.addEventListener('open',()=> {
    console.log("Datachannel Opened")
  })

  let remoteVideo = createVideo(target)
  setOnTrack(peerConnection,remoteVideo)
  peers[target] = [peerConnection,dataChannel]

  peerConnection.addEventListener("iceconnectionstatechange",(ev)=>{
    let iceConnectionState = peerConnection.iceConnectionState
    if(iceConnectionState ==="failed"||iceConnectionState==="disconnected"||
    iceConnectionState==="closed") {
      console.log("ice connection state changed")
      console.log("remove peer connection:",target)
      delete peers[target];
      if(iceConnectionState!='closed'){
        peerConnection.close()
      }
      removeVideo(remoteVideo);
    }
  })

  peerConnection.addEventListener("icecandidate",(ev)=>{
    console.log("icecandidate event:",ev)
    if(ev.candidate){
      console.log("New icecandidate :",
        JSON.stringify(ev.candidate))
      sendSignalCandidate("ice.candidate",target,ev.candidate,group)
      return
    } else { // ice candidate gather completed
      sendSignalSDP('sdp.offer',target,
        peerConnection.localDescription,group
      )
    }
  })

  peerConnection.createOffer() // ice candidate gathering completed
    .then((offer)=>peerConnection.setLocalDescription(offer))
    .then(()=>{
      console.log('localDescription setted')
          })
    .catch((reason)=>{
      console.log('error on createOffer:',reason)
    })

  // peerConnection.addEventListener("onnegotiationneeded",(ev) =>{
  //   console.log("event occured:",ev)
  //   peerConnection.createOffer()
  //   .then((offer)=>peerConnection.setLocalDescription(offer))
  //   .then(()=>{
  //     console.log('localDescription setted')
  //     sendSignalSDP('sdp.offer',target,
  //       peerConnection.localDescription,group
  //     )
  //   })
  //   .catch((reason)=>{
  //     console.log('error on createOffer:',reason)
  //   })
  // })
}

function createAnswer(offer,target,group){

  const desc = new RTCSessionDescription(offer) 

  peerConnection = new RTCPeerConnection()
  addLocalTracks(peerConnection)

  recentPeerConnection=peerConnection

  let remoteVideo = createVideo(target)
  setOnTrack(peerConnection,remoteVideo)


  peerConnection.addEventListener("datachannel", e => {
    console.log("datachannel event occured:",e)
    peerConnection.dc = e.channel
    console.log("dataChannel setted:",e.channel)
    peerConnection.dc.addEventListener('open',()=> {
    console.log("Datachannel Opened")
    })

    peers[target] = [peerConnection,peerConnection.dc]
  })

  peerConnection.addEventListener("iceconnectionstatechange",(ev)=>{
    console.log("iceconnectionstatechange event:",ev)
    let iceConnectionState = peerConnection.iceConnectionState;
    if(iceConnectionState ==="failed"||iceConnectionState==="disconnected"||
    iceConnectionState==="closed") {
      delete peers[target];
      if(iceConnectionState!='closed'){
        peerConnection.close()
      }
      removeVideo(remoteVideo);
    }
  })

  peerConnection.addEventListener("icecandidate",(ev)=>{
    console.log("icecandidate event:",ev)
    if(ev.candidate){
      console.log("New icecandidate :",
        JSON.stringify(peerConnection.localDescription))
      sendSignalCandidate("ice.candidate",target,ev.candidate,group)
      return
    } else {
      sendSignalSDP('sdp.answer',target,
      peerConnection.localDescription,group
      )
    }
  })

  //setting remote description
  peerConnection.setRemoteDescription(desc)
  .then(()=>{
    console.log("Remote description setted for id:",target)

  }).then(()=>{
    return peerConnection.createAnswer()
  })
  .then(answer=>{
    console.log("Answer Created",answer)
    peerConnection.setLocalDescription(answer)
    
  })
}

function addLocalTracks(peer) {
  localStream.getTracks().forEach((track) => {
    peer.addTrack(track,localStream)
  })
}

function createVideo(target) {
  let vids = document.getElementById("video-others-wrapper")
  let vid = document.createElement('video')
  vid.id = 'video-'+target
  vid.autoplay=true
  vid.playsInline=true
  vids.appendChild(vid)

  return vid
}

function removeVideo(video) {
  let vids = video.parentNode
  vids.removeChild(video)
}

function setOnTrack(peer,remoteVideo) {
  let remoteStream = new MediaStream()
  remoteVideo.srcObject=remoteStream
  peer.addEventListener('track',async (ev) =>{
    console.log("adding remote stream to local:",remoteVideo.id)
    console.log("event:",ev)
    remoteStream.addTrack(ev.track,remoteStream)
  })
}

function call_by_id(){
  let j = {
    'request':'call.new',
    'target':callId.value
  }
  let t = JSON.stringify(j)
  console.log(t)
  ws.send(t)
}

function invite_by_id(){
  let j = {
    'request':'group.invite',
    'target':callId.value
  }
  let t = JSON.stringify(j)
  console.log(t)
  ws.send(t)
}

function creategroup(){
  let j = {
    'request':'group.new',
    'target':callId.value
  }
  let t = JSON.stringify(j)
  console.log(t)
  ws.send(t)
}
