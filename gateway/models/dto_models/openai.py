from pydantic import BaseModel, Field
from typing import List, Optional, Union, Any, Dict

# Pydantic classes for OpenAI completions

class OpenAIMessage(BaseModel):
    """
    A class representing a message in the OpenAI chat format.
    """
    role: str = Field(..., description="The role of the message author.")
    content: Union[str, List[Dict[str, Any]]] = Field(..., description="The content of the message. Accepts a string or an array of content parts with a defined type.")
    name: Optional[str] = Field(default=None, description="An optional name for the participant. Provides the model information to differentiate between participants of the same role.")

class OpenAIRequest(BaseModel):
    """
    A class representing a request to the OpenAI chat API.
    """
    model: str = Field(..., description="ID of the model used to generate the response.")
    messages: List[OpenAIMessage] = Field(..., min_length=1, description="A list of messages comprising the conversation so far. Must contain at least 1.")
    temperature: Optional[float] = Field(default=None, ge=0.0, le=2.0, description="What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.")
    max_completion_tokens: Optional[int] = Field(default=None, description="An upper bound for the number of tokens that can be generated for a completion, including visible output tokens and reasoning tokens.")
    stream: Optional[bool] = Field(default=False, description="If set to true, the model response data will be streamed to the client as it is generated using server-sent events.")

# extra_body