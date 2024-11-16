from rich.console import Console
from rich.tree import Tree
from rich.panel import Panel
from rich.syntax import Syntax

from terrarium_tool import TerrariumTool, TerrariumToolInputSchema
from agent import code_generation_agent, CodeGenerationAgentInputSchema

console = Console()

response = code_generation_agent.run(
    CodeGenerationAgentInputSchema(
        task_description="Create a text analyzer that processes a string of text and returns statistics including: total word count, average word length, and most frequent word.",
        requirements=[
            "Must handle empty strings gracefully",
            "Should ignore case when counting words",
            "Should ignore punctuation",
            "Should handle ties for most frequent word by returning the first alphabetically",
        ],
    )
)

# Print internal thoughts as a list
console.print("\n[bold blue]Development Process:[/bold blue]")
for i, thought in enumerate(response.technical_analysis, 1):
    console.print(f"[cyan]{i}. {thought}[/cyan]")

# Print required imports
console.print("\n[bold blue]Required Imports:[/bold blue]")
for import_statement in response.imports:
    syntax = Syntax(import_statement, "python", theme="monokai")
    console.print(Panel(syntax))

# Print helper functions
console.print("\n[bold blue]Functions:[/bold blue]")
for i, function in enumerate(response.functions, 1):
    console.print(f"\n[bold green]Function {i}:[/bold green]")
    syntax = Syntax(
        function, "python", theme="monokai", line_numbers=True, word_wrap=True
    )
    console.print(Panel(syntax))

# Print main guard clause
console.print("\n[bold blue]Main Guard Clause:[/bold blue]")
main_syntax = Syntax(
    response.main_guard_clause, "python", theme="monokai", line_numbers=True
)
console.print(Panel(main_syntax))

# Execute the code using Terrarium
console.print("\n[bold blue]Code Execution Results:[/bold blue]")
terrarium_tool = TerrariumTool()

# Combine all code into a single string
full_code = "\n".join(
    [
        "\n".join(response.imports),
        "\n".join(response.functions),
        response.main_guard_clause,
    ]
)

# Execute the code
result = terrarium_tool.run(TerrariumToolInputSchema(code=full_code))

if result.success:
    console.print(Panel("[green]✓ Code executed successfully![/green]"))
    if result.std_out:
        console.print(Panel(result.std_out, title="Output"))
    if result.final_expression:
        console.print(Panel(result.final_expression, title="Final Expression"))
else:
    console.print(Panel(f"[red]✗ Error:[/red]\n{result.std_err}", title="Error"))

console.print(f"[dim]Execution time: {result.code_runtime}ms[/dim]")
