"""Legacy manual entrypoint. Live verification moved to verification/live_smoke.py."""
if __name__ == "__main__":
    from llm import LocalLLM
    print(LocalLLM().generate("Explain conversational memory in one sentence."))
