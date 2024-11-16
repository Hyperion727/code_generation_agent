import requests
from typing import Optional
from pydantic import Field

from atomic_agents.agents.base_agent import BaseIOSchema
from atomic_agents.lib.base.base_tool import BaseTool, BaseToolConfig


################
# INPUT SCHEMA #
################
class TerrariumToolInputSchema(BaseIOSchema):
    """
    Schema for input to execute Python code in a sandboxed Terrarium environment.
    Returns the execution results including stdout, stderr, and runtime metrics.
    """

    code: str = Field(
        ..., description="Python code to execute in the Terrarium environment"
    )


####################
# OUTPUT SCHEMA(S) #
####################
class TerrariumToolOutputSchema(BaseIOSchema):
    """Schema representing the output from Terrarium code execution"""

    success: bool = Field(..., description="Whether the code execution was successful")
    std_out: Optional[str] = Field(
        None, description="Standard output from code execution"
    )
    std_err: Optional[str] = Field(
        None, description="Standard error from code execution"
    )
    final_expression: Optional[str] = Field(
        None, description="Result of the final expression evaluated"
    )
    code_runtime: float = Field(..., description="Execution time in milliseconds")


#################
# CONFIGURATION #
#################
class TerrariumToolConfig(BaseToolConfig):
    """Configuration for the TerrariumTool"""

    base_url: str = Field(
        default="http://localhost:8081",
        description="Base URL for the Terrarium service",
    )
    timeout: int = Field(
        default=30, description="Timeout in seconds for code execution"
    )


#####################
# MAIN TOOL & LOGIC #
#####################
class TerrariumTool(BaseTool):
    """
    Tool for executing Python code in a sandboxed Terrarium environment.

    Attributes:
        input_schema (TerrariumToolInputSchema): The schema for the input data
        output_schema (TerrariumToolOutputSchema): The schema for the output data
    """

    input_schema = TerrariumToolInputSchema
    output_schema = TerrariumToolOutputSchema

    def __init__(self, config: TerrariumToolConfig = TerrariumToolConfig()):
        """
        Initializes the TerrariumTool.

        Args:
            config (TerrariumToolConfig): Configuration for the tool
        """
        super().__init__(config)
        self.base_url = config.base_url
        self.timeout = config.timeout

    def run(self, params: TerrariumToolInputSchema) -> TerrariumToolOutputSchema:
        """
        Executes Python code in the Terrarium environment.

        Args:
            params (TerrariumToolInputSchema): The input parameters containing the code to execute

        Returns:
            TerrariumToolOutputSchema: The execution results

        Raises:
            requests.RequestException: If the request to Terrarium service fails
        """
        try:
            response = requests.post(
                self.base_url,
                json={"code": params.code},
                headers={"Content-Type": "application/json"},
                timeout=self.timeout,
            )

            result = response.json()

            return TerrariumToolOutputSchema(
                success=result.get("success", False),
                std_out=result.get("std_out"),
                std_err=result.get("std_err"),
                final_expression=result.get("final_expression"),
                code_runtime=result.get("code_runtime", 0),
            )

        except requests.RequestException as e:
            return TerrariumToolOutputSchema(
                success=False,
                std_err=f"Error connecting to Terrarium service: {str(e)}",
                code_runtime=0,
            )
