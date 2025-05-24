from langchain.prompts import PromptTemplate

prompt = """
You are a tool selector for a dating assistant.

Given a user's input, choose which tool to use and extract the required parameters.
Only extract what can be inferred from the prompt.
Do not guess user_id; that will be passed separately.

Available tools:
{tool_descriptions}

User Input: {input}

Respond in JSON with:
- tool_name: Name of the selected tool
- tool_args: dictionary of extracted arguments
"""

router_prompt = PromptTemplate.from_template(
    prompt
)

### Why are we doing like this? And not simply insert the tool node.