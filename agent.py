from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import noise_cancellation
from livekit.plugins.silero import VAD
from livekit.plugins.google.beta.realtime import RealtimeModel
from prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION
from tools import get_weather, search_web

load_dotenv()

class Assistant(Agent):
    def __init__(self) -> None:
        # ✅ Register tools in the Agent class
        super().__init__(
            instructions=AGENT_INSTRUCTION,
            tools=[get_weather, search_web]  # ✅ Tools go here in Agent
        )

async def entrypoint(ctx: agents.JobContext):
    # ✅ Female voice with caring personality
    model = RealtimeModel(
        instructions=AGENT_INSTRUCTION,
        voice="Aoede",  # ✅ Perfect female voice for caring companion
        temperature=0.9  # ✅ Slightly higher for more emotional warmth
    )
    
    # ✅ Clean AgentSession without tools parameter
    session = AgentSession(
        llm=model,
        vad=VAD.load()
        # ❌ REMOVE: tools parameter - doesn't exist here
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),  # ✅ Agent has the tools
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC()
        ),
    )

    await session.generate_reply(instructions=SESSION_INSTRUCTION)

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
