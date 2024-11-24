import requests
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax


def send_to_terrarium(code: str) -> dict:
    response = requests.post(
        "http://localhost:8080",
        json={"code": code},
        headers={"Content-Type": "application/json"},
        timeout=30,
    )
    return response.json()


# Initialize console for rich output
console = Console()

# Python code to generate Fibonacci sequence
fibonacci_code = """
def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]

    sequence = [0, 1]
    while len(sequence) < n:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence

# Generate first 10 numbers
result = fibonacci(10)
print(f"Fibonacci sequence: {result}")
"""

# Display the code we're sending
console.print(
    Panel(
        Syntax(fibonacci_code, "python", theme="monokai"),
        title="📤 Sending Code",
        border_style="blue",
    )
)

# Send code to Terrarium and handle the response
try:
    result = send_to_terrarium(fibonacci_code)

    # Display the output if the execution was successful
    if result.get("success"):
        console.print(
            Panel(
                result.get("std_out", "No output"),
                title="📥 Result",
                border_style="green",
            )
        )

        # Optionally display the final expression if available
        if result.get("final_expression"):
            console.print(
                Panel(
                    str(result["final_expression"]),
                    title="🔄 Final Expression",
                    border_style="yellow",
                )
            )
    else:
        # Display error message if execution failed
        console.print(
            Panel(
                result.get("std_err", "Unknown error"),
                title="❌ Error",
                border_style="red",
            )
        )

    # Display execution time
    console.print(
        f"⏱️  Execution time: {result.get('code_runtime', 0)}ms", style="italic"
    )

except requests.RequestException as e:
    # Handle connection errors
    console.print(f"[red]Error connecting to Terrarium service: {e}[/red]")
