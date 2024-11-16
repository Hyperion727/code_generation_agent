import os
from typing import List
from atomic_agents.agents.base_agent import BaseAgent, BaseAgentConfig
from atomic_agents.lib.components.system_prompt_generator import SystemPromptGenerator
from atomic_agents.lib.base.base_io_schema import BaseIOSchema
import instructor
import openai
from pydantic import Field


class CodeGenerationAgentInputSchema(BaseIOSchema):
    """Schema for input to the CodeGenAgent"""

    task_description: str = Field(
        ..., description="Instructions for the code generation"
    )
    requirements: List[str] = Field(
        ...,
        description="List of requirements for the code generation",
    )


class CodeGenerationAgentOutputSchema(BaseIOSchema):
    """This schema defines the output schema for the CodeGenerationAgent."""

    technical_analysis: List[str] = Field(
        ...,
        description=(
            "A step-by-step breakdown of the problem to be solved and how it could be approached, including:\n"
            "1. Problem analysis\n"
            "2. Design considerations\n"
            "3. Potential challenges\n"
            "4. Implementation strategy\n"
            "5. Testing approach"
        ),
        min_length=3,
        max_length=10,
    )
    imports: List[str] = Field(
        ...,
        description=(
            "List of import statements required for the solution. "
            "Each item should be a complete import statement. "
            "Example: ['import re', 'from collections import Counter']"
        ),
    )
    functions: List[str] = Field(
        ...,
        description=(
            "List of functions needed for the solution. "
            "Each item in the array should be a complete function definition, including google-style docstrings and type hints. "
            "Example: "
            'def example_function(a: int, b: int) -> int:\\n    """Example function with two integer inputs and an integer output."""\\n    ...\\n    return a + b\\n'
        ),
    )
    main_guard_clause: str = Field(
        ...,
        description=(
            "The primary guard clause that uses the helper functions to solve the problem. "
            "Must include both the main guard clause definition AND a '__main__' guard clause "
            "that demonstrates example usage. Format should be:\n"
            "if __name__ == '__main__':\n"
            "    # example usage"
        ),
    )


# NOTE: Make sure your API key is set in your environment variables
# This tutorial uses OpenAI with gpt-4o-mini, but you can use any other LLM
# from any other provider. See: https://github.com/instructor-ai/instructor
code_generation_agent = BaseAgent(
    BaseAgentConfig(
        client=instructor.from_openai(
            openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        ),
        model="gpt-4o-mini",
        input_schema=CodeGenerationAgentInputSchema,
        output_schema=CodeGenerationAgentOutputSchema,
        system_prompt_generator=SystemPromptGenerator(
            background=[
                "You are an AI assistant that is an expert in Python code generation.",
                "This AI has access to a sandboxed environment based on Piodide, meaning it has access to popular libraries like:",
                "numpy, pandas, matplotlib, scipy, scikit-learn, sympy, seaborn, nltk, networkx, requests, etc.",
            ],
            steps=[
                "Analyze the user's instructions and determine the necessary functions and main guard clause to solve the problem.",
                "Generate the code for all necessary functions except the main guard clause.",
                "Finally, generate the main guard clause that uses the helper functions to solve the problem. ",
            ],
            output_instructions=[
                "Your output should be as clean and professional as possible, featuring proper separation of concerns."
            ],
        ),
    )
)
