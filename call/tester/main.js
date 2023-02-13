
// 1. get token from input
// 2. connect websocket
// 3. call or be called over server
// 4. exchange sdp over server
// 5. connect p2p

const websocket_url = "ws://127.0.0.1:8000/ws/call/"

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
      request,
      target : peer
    }
    if (accept) {
      answer.request = 'call.accept'
    } else {
      answer.request = 'call.reject'
    }
    ws.send(answer)
  } else if (req=="call.accept") {
    createOffer(peer,group)
  } else if (req=="call.reject") {
    alert("Call rejected by id:",peer)

    // manage group
  } else if (req=="group.new"){
    alert("Converted to group call :",data['group'])
    group = data['group']
    
  } else if (req=="group.invite"){
    accept = confirm("Accept group call invite from id:",peer," ?") 
    let answer = {
      request,
      target : peer
    }
    if (accept) {
      answer.request = 'group.accept'
      group = data['group']
    } else {
      answer.request = 'group.reject'
    }
    ws.send(answer)
  } else if (req="group.accept") {
    createOffer(peer,group)
  } else if (req="group.reject") {
    alert("Group call rejected by id:",peer)
  }

  if (type=='sdp.offer') { // receive a call
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

function sendSignal(type,target,sdp,group) {
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

function createOffer(target,group){
  let peerConnection = new RTCPeerConnection(null);
  addLocalTracks(peerConnection);


  let dataChannel= peerConnection.createDataChannel('channel')
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
      console.log("remove peer connection:",target)
      delete peers[target];
      if(iceConnectionState!='closed'){
        peerConnection.close()
      }
      removeVideo(remoteVideo);
    }
  })

  peerConnection.addEventListener("icecandidate",(ev)=>{
    if(ev.candidate){
      console.log("New icecandidate :",
        JSON.stringify(peerConnection.localDescription))
      return
    }

    sendSignal('sdp.offer',target,
      peerConnection.localDescription,group
    )
  })

  peerConnection.createOffer()
  .then(offer=>peerConnection.setLocalDescription(offer))
  .then(()=>{
    console.log('localDescription setted')
  })
}

function createAnswer(offer,target,group){
  let peerConnection = new RTCPeerConnection(null);
  addLocalTracks(peerConnection);

  let remoteVideo = createVideo(target)
  setOnTrack(peerConnection,remoteVideo)

  peerConnection.addEventListener("datachannel", e => {
    peerConnection.dc = e.channel
    console.log("dataChannel setted:",e.channel)
    peerConnection.dc.addEventListener('open',()=> {
    console.log("Datachannel Opened")
    })

    peers[target] = [peerConnection,peerConnection.dc]
  })

  peerConnection.addEventListener("iceconnectionstatechange",(ev)=>{
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
    if(ev.candidate){
      console.log("New icecandidate :",
        JSON.stringify(peerConnection.localDescription))
      return
    }

    sendSignal('adp.answer',target,
      peerConnection.localDescription,group
    )
  })

  peerConnection.setRemoteDescription(offer)
  .then(()=>{
    console.log("Remote description setted for id:",target)
    return peerConnection.createAnswer()
  })
  .then(answer=>{
    console.log("Answer Created",answer)
    peerConnection.setLocalDescription(answer)
  })
}

function addLocalTracks(peer) {
  localStream.getTracks().forEach(track => {
    peer.addTrack(track,localStream)
  });
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
    remoteStream.addTrack(ev.track,remoteStream)
  })
}

function call_by_id(){
  let j = {
    'request':'call.new',
    'target':callId.value
  }
  let t = JSON.stringify(j)
  ws.send(t)
}

function invite_by_id(){
  let j = {
    'request':'group.invite',
    'target':callId.value
  }
  let t = JSON.stringify(j)
  ws.send(t)
}

function creategroup(){
  let j = {
    'request':'group.new',
    'target':callId.value
  }
  let t = JSON.stringify(j)
  ws.send(t)
}
