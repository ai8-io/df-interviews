import inngest
import inngest.fast_api

client = inngest.Inngest(
    app_id="hr-chatbot",
    api_base_url="http://localhost:8388",
    event_api_base_url="http://localhost:8388",
    signing_key="DEADBEEF",
    event_key="event-key",
    is_production=True,
)
