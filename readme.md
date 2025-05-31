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



#### Response
As said by https://claude.ai/chat/65809e9e-d583-47e9-aea3-adfe9499d9a7, we are doing SSE (Server Side Events)


### Use case of Redis
- For api rate limiting in fastapi_limiter library https://stackoverflow.com/questions/65491184/ratelimit-in-fastapi
- Also for saving it in memory. I mean use as a MemorySaver.
Actually if there I can't find any solution, I will switch to openai which has max tokens limit.


### I am still finding something innovative.
In the Dating App, I am able to create a good bio using LLM and also conversation

But this is AI, people just don't want to work a lot and just needs AI to work on their behalf.

### We will have a conversation bot. Actually we will having different bots for different purposes.
- Related to conversation bots
    - There will be various characters
    - Like Alex - Who likes to build trust by staying grounded.
    - Like Adam - Who is quite flirty and who is quite willing to risk it all.
    - etc. You can build custom ones also.
    - People can build animals type too. (Maybe funny) Like seen in character.ai. (Now this is interesting)

#### Level of Hardness of Bots
- Matchmaking one - Hard
- Conversation one - Medium
- Bio one - Easy
- Personal bot - Conveys about your app.

**If user asks anything irrelevant then you may say that Sorry I am subjected to help you based on the given criteria. You may take help of other bos like Conversation one - To help you related to interaction, Personal bot - Which talks related to your profile, Bio bot - Which is responsible for creating a bio for you**

*I mean any relationship advice, it can ask with normal chatgpt also. Why waste time and money on that? So I am done. I undertsood that we will be creating different bots.*

Ok so I will build this conversation one.


##### So it means the MatchMaking one is the most difficult one. I should be very cautious also how to create that.

### Ravi, focus on making good softwares. Don't over complicate yourself. Three bots are enough.
> You have focused on privacy, right. And personal stuff. There is a difference between dating app and social media.

### TODO After thinking a lot, I will now focus on these 3 bots only at initial phase.
https://chatgpt.com/c/6838a5ef-9088-800d-9be3-a7446720c13c

👉 Later, If I want to build more stuff like AI Coaching to interact with women etc, I will build it.

👉 But AI Coaching looks lot like a spoon feeding.

### 👉 I need to make them addicted. So, I would need free version + upgrade version.


### 🔁 Overview of Personal Cloning stack
Model Type	Purpose
Base Model	Chat generation: understands context, produces answers in your style
Embedding Model	Finds relevant past conversations / behaviors (memory + style recall)
Sentiment/Emotion Model	Analyzes emotional content of messages for empathy & style cloning