# 🧪 Exercise: Build a Stateful Q&A Bot with MongoDB Checkpointer
https://chatgpt.com/c/6825946b-ea74-800d-8cf0-112c3e0b9e19


### 

A nice helper example
https://github.com/DzmitryPihulski/LangGraph-agent-on-MongoDB


>> I finally understood to include the setup of LLM in the graph.py and write it down separately and include it in the lifespan.
https://chatgpt.com/c/681f72e4-5ad0-800d-b706-dc2453ab111e


👉 Note by pylance message, I have upgraded the strictness of the system to Standard.

### MongoDB


#### We will include App functionalities also
- For example, User want to "Logout", then we will say Please do Logout from the settings.
- User want to know about why it's getting less matches etc.
- Uesr wants to know about their app stuff.


https://claude.ai/chat/fc84041b-e46b-4bc8-aa34-4334a48ef0b5
There is some scene in that. He doesn't use tools. He does say to the AI, and it brings the responses and we act like it. 


### 🤔🤔 How to assign the limit of the chat? 

### 🤔🤔 Now my app is becoming too complex. And passing llm to the down between different functions is quite bothering me. I think I should look for a new way/


### Using SubGraphs

[https://dev.to/sreeni5018/langgraph-subgraphs-a-guide-to-modular-ai-agents-development-31ob]
Best Practices for Using Subgraphs
- Shared State Keys – Ensure the parent graph and subgraph share at least one state key for smooth communication.

- State Transformation – When state structures differ, use a node function to manage the transformation.

- Modular Design – Think modular! Reusable subgraphs keep your workflows efficient and scalable.

- Clear Interfaces – Define precise input and output schemas to ensure seamless integration with parent graphs.

- By leveraging subgraphs in LangGraph, you can build AI systems that are more scalable, organized, and flexible. Whether you’re constructing multi-agent workflows or breaking down complex processes, subgraphs offer a structured approach to handling AI workflow challenges.

---
> I want to understand what about the rate limiting stuff.
https://claude.ai/chat/74a39efa-66d4-41a6-9240-38eea7937760

---

> I finally understood the dependency injection one. Finally got to know how to deal with objects. Finally understood how to work 
with Lifespan. And understood LangGraph nodes stuff.
> I have only one problem (which is not a big problem). But still. And that is using async await.


#### I will create the direct links also.
So, if they create on those, we will directly go to that subgraph (like the Indigo case one)



