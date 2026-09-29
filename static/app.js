const sampleCode = `let num A be 10
let num B be 5
let num result be add A and B
print result

if result eq 15 then {
  print "result is 15"
} else {
  print "result is not 15"
} end

while A lt 15 do {
  set A = add A and 1
  print A
} end

func addOne(num x) {
  return add x and 1
} end

print call addOne(10)`;

const editor = document.getElementById("codeEditor");
const outputConsole = document.getElementById("outputConsole");
const runButton = document.getElementById("runButton");
const resetButton = document.getElementById("resetButton");

if (editor) editor.value = sampleCode;

function setOutput(value) {
    if (outputConsole) outputConsole.textContent = value;
}

async function run7to5(code) {
    const response = await fetch("/api/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code })
    });

    const data = await response.json();

    if (!response.ok || !data.ok) {
        throw new Error(data.error || "Code execution failed.");
    }

    return data.output || "Program executed successfully with no output.";
}

if (runButton) {
    runButton.addEventListener("click", async () => {
        try {
            setOutput("Running...");
            const output = await run7to5(editor.value);
            setOutput(output);
        } catch (error) {
            setOutput(`Runtime error: ${error.message}`);
        }
    });
}

if (resetButton) {
    resetButton.addEventListener("click", () => {
        if (editor) editor.value = sampleCode;
        setOutput("Ready.");
    });
}

setOutput("Ready.");
