from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from .orchestrator import ClusterManager
import asyncio
import json

app = FastAPI()
manager = ClusterManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/kill/{node_id}")
async def kill_node(node_id: str):
    manager.kill_node(node_id)
    return {"status": "killed"}

# NEW: Scale Up
@app.get("/api/spawn")
async def spawn_node():
    success = manager.spawn_node()
    return {"status": "spawned" if success else "failed"}

# NEW: Scale Down
@app.get("/api/remove")
async def remove_node():
    success = manager.remove_node()
    return {"status": "removed" if success else "failed"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            system_state = manager.get_system_health()
            
            # Auto-Recovery Loop
            for node in system_state["nodes"]:
                if node['status'] == 'CRITICAL':
                    print(f"Detecting failure in {node['name']}...")
                    manager.heal_node(node['id'])
            
            await websocket.send_text(json.dumps(system_state))
            await asyncio.sleep(.5)
    except Exception as e:
        print("Client disconnected")