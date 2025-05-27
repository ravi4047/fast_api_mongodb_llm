from typing import Dict

# ==================== STREAM MANAGER ====================

# 🤔🤔 I don't think I can scale this to multiple servers? Also I don't think I can halt like in aws websocket api.
## As far as I remember, I can only connect to it.
## 💡 Wait, so halting can be like disconnect, wait If disconnected, then ok
## Wait so, we are just building websocket connection for 1-2 seconds only during the question/answer scenario.
## So, using websocket api doesn't seem to be a viable option

## That means technically we can't halt it. Or can we?

## First tell me, how long does the normal routes timeout for?

# https://chatgpt.com/c/683566b6-5d18-800d-8c07-16cf43f7345d
## 👉👉So, finally convinced that we will use route i.e. Rest API with streaming response i.e. keep-alive True one (which can wait for 1-2 minutes
## even). We will set high timeout

## 🤔 But wait, how will I halt then? Also, from the client side, I won't allow to chat again. But keeping security in check, you can simply
## route again and a new routing will work. So, how would you stop that in simple routes. It's technically not feasible then.
## Also the scaling issues if you have multiple servers? Then this stream manager is not possible. The main trouble is this halt mechanism.
## Should I remove this halt mechanism or should I simply use bi-directional websockets.
## 👉 When I said about my problems, chat-gpt started talking about websockets
## 👉👉But when I became more serious, it finally said that even chatbots like chat-gpt and all uses RestAPI with streaming. Hence, use that 
## only.

# https://claude.ai/chat/1760f327-87e7-41f0-b7b0-8ed9541afc65

# 👉👉👉 Now after interacting with chat-gpt I came to know that we can use CancelToken to halt the rest request during streaming.
# Hence, I don't think I need Stream manager.

### -------------------- UNUSED FOR NOW -------------------------- START
class StreamManager:
    """Manages active streams and halt requests"""
    
    def __init__(self):
        self.active_streams: Dict[str, bool] = {}  # stream_id -> should_continue
        self.halt_requests: Dict[str, bool] = {}   # stream_id -> halt_requested
    
    def start_stream(self, stream_id: str) -> None:
        """Register a new stream"""
        self.active_streams[stream_id] = True
        self.halt_requests[stream_id] = False
    
    def halt_stream(self, stream_id: str) -> None:
        """Request to halt a stream"""
        if stream_id in self.active_streams:
            self.halt_requests[stream_id] = True
            self.active_streams[stream_id] = False
    
    def should_continue(self, stream_id: str) -> bool:
        """Check if stream should continue"""
        return self.active_streams.get(stream_id, False)
    
    def is_halt_requested(self, stream_id: str) -> bool:
        """Check if halt was requested"""
        return self.halt_requests.get(stream_id, False)
    
    def cleanup_stream(self, stream_id: str) -> None:
        """Clean up stream data"""
        self.active_streams.pop(stream_id, None)
        self.halt_requests.pop(stream_id, None)
### -------------------- UNUSED FOR NOW -------------------------- STOP