from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from supabase import create_client, Client


app = FastAPI()


SUPABASE_URL = "https://uvntrmkmectomqlpldor.supabase.co"
SUPABASE_KEY = "sb_publishable_JhnViODyavc0ysmH-CJKew_Lpbc_CAt"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.get("/")
async def health():
    return {"status": "ok"}

@app.websocket("/ws/session/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    await websocket.send_text(f"Connected to session {session_id}")

    supabase.table("sessions").insert({
        "session_id": session_id
    }).execute()

    try:
        while True:
            user_msg = await websocket.receive_text()

            supabase.table("events").insert({
                "session_id": session_id,
                "role": "user",
                "content": user_msg
            }).execute()

            
            assistant_text = f"AI reply to: {user_msg}"

            supabase.table("events").insert({
                "session_id": session_id,
                "role": "assistant",
                "content": assistant_text
            }).execute()

            await websocket.send_text(assistant_text)

    except WebSocketDisconnect:
        events = supabase.table("events") \
            .select("role, content") \
            .eq("session_id", session_id) \
            .execute()

        summary = " | ".join(
            f"{e['role']}: {e['content']}" for e in events.data
        )[:1000] 

        supabase.table("sessions").update({
            "end_time": "now()",
            "summary": summary
        }).eq("session_id", session_id).execute()

        print(f"Session {session_id} closed and saved")
