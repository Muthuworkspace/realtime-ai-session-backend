Overview :

This project implements a real-time, session-based AI interaction backend using FastAPI WebSockets.
Each WebSocket connection represents a user session, where messages are exchanged in real time, persisted to a database, and summarized when the session ends.

The system is designed to demonstrate:

1) WebSocket lifecycle handling

2) Session and event persistence

3) Post-session processing

4) Clean, extensible backend architecture


Architecture Overview :

  Client (Browser)
   	   	↓ WebSocket
	FastAPI Backend
   		↓
	Supabase (PostgreSQL)

Application Flow :

1) WebSocket Connection

	Client connects to /ws/session/{session_id}
	A new session is created in the database

2) Realtime Messaging

	User messages are received via WebSocket
	Each message is stored as an event
	The backend generates an AI response
	AI responses are sent back in real time and stored

3) Session Termination

	When the WebSocket disconnects:

     All session events are fetched
     A session summary is generated
     Session end time and summary are saved


Core Components :

1) WebSocket Endpoint

	Maintains a long-lived, bidirectional connection
	Handles session lifecycle (connect → messages → disconnect)

2) Session Management

	Each WebSocket connection maps to a unique session_id
	Session metadata is stored in the sessions table

3) Event Logging

	Every user and assistant message is stored in the events table
	Enables conversation replay and analysis

4) Post-Session Processing

	On disconnect, the conversation is summarized
	Summary is stored for later review



sessions table :


Column	Description

session_id	Unique session identifier
start_time	Session start timestamp
end_time	Session end timestamp
summary	        Generated session summary

events table :

Column	Description

id		Event ID
session_id	Related session
role		user / assistant
content		Message text
created_at	Timestamp



AI Integration :

  For stability and ease of development, a mock AI response is used during local execution.

  The system is designed so that:
	     The mock response can be replaced with a real LLM provider
       No architectural changes are required to enable streaming or production models

  This approach ensures reliability while demonstrating full integration flow.

Technologies Used :

  1) Python

  2) FastAPI

  3) WebSockets

  4) Supabase (PostgreSQL)

  5) Uvicorn


HOW TO RUN :

   py -m uvicorn main:app --reload

Open the WebSocket test client and connect to :

   ws://127.0.0.1:8000/ws/session/test2

Key Takeaways :

   Demonstrates real-time backend communication
   Clean separation of session, events, and persistence
   Handles full WebSocket lifecycle
   Designed with extensibility in mind


Notes :

   Row Level Security (RLS) was disabled for server-side inserts during development
   The backend can be extended with real LLMs and streaming responses in production


Author :

MUTHUKUMARESAN V
Internship Assignment – Realtime AI Backend
