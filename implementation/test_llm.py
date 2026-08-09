from llm import LocalLLM


llm = LocalLLM()

response = llm.generate(
    "Explain what conversational memory is in one sentence."
)

print("\nLLM RESPONSE:")
print(response)