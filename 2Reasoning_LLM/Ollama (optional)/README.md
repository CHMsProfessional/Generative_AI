# Khipus.ai
# Running Large Language Models Locally with **Ollama** on Windows
# © Copyright Notice 2025, Khipus.ai - All Rights Reserved.

> Prepared by **Said Nikjou** (Data Scientist & Professor, Khipus.ai)
>
> Last updated: 2025‑07‑18

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Download & Install](#download--install)
3. [Verify the CLI](#verify-the-cli)
4. [Pull Your First Model](#pull-your-first-model)
5. [Run the Model](#run-the-model)
6. [Serving Ollama as an API](#serving-ollama-as-an-api)
7. [Updating / Removing](#updating--removing)
8. [Troubleshooting](#troubleshooting)
9. [Additional Resources](#additional-resources)

---

## Prerequisites

| Requirement                | Notes                                                                                      |
| -------------------------- | ------------------------------------------------------------------------------------------ |
| **Windows 10 or 11** (x64) | Administrator rights are needed for the installer.                                         |
| **Internet connection**    | \~10 GB download for the example model.                                                    |
| **Disk space**             | Allow at least 15 GB free to store models locally.                                         |
| **(Optional) GPU**         | A CUDA‑capable GPU with ≥ 6 GB VRAM greatly accelerates inference, but CPU‑only works too. |

---

## Download & Install

1. Open [https://ollama.com](https://ollama.com) in your browser.&#x20;
2. Click **Download** and select **Windows**.&#x20;
3. Run the downloaded **OllamaSetup.exe** from your *Downloads* folder.&#x20;
4. In the wizard, press **Install** and wait until it finishes.&#x20;
5. Close the installer when it reports **Completed**.

> **Tip 🛈** The installer automatically adds `ollama.exe` to your *PATH* so it is available in any new terminal session.

---

## Verify the CLI

Open **Command Prompt** or **PowerShell** and run:

```powershell
ollama --help
```

You should see a list of commands such as `serve`, `run`, `pull`, etc.&#x20;

If the command isn’t recognised, sign out and back in or restart the terminal so the updated *PATH* is re‑loaded.

---

## Pull Your First Model

Ollama stores models locally.  Let’s download the 14‑billion‑parameter **DeepSeek‑R1** model:

```powershell
ollama pull deepseek-r1:14b
```

The download is \~9 GB and may take several minutes.  When finished you should see `success`.&#x20;

> Check your collection at any time with:
>
> ```powershell
> ollama list
> ```
>
>

---

## Run the Model

Start an interactive session:

```powershell
ollama run deepseek-r1:14b
```

Type a prompt, e.g. `what is your name?`, and wait for the reply.&#x20;

Use **Ctrl + C** to exit.

---

## Serving Ollama as an API

If you want a REST endpoint on ``, run:

```powershell
ollama serve
```

Keep the window open while you experiment, or create a Windows service so it starts automatically.

---

## Updating / Removing

| Task               | Command                                                                                        |
| ------------------ | ---------------------------------------------------------------------------------------------- |
| **Upgrade Ollama** | Download the latest installer from the website and run it – settings and models are preserved. |
| **Update a model** | `ollama pull <model>:<tag>` again (new layers are fetched incrementally).                      |
| **Remove a model** | `ollama rm <model>:<tag>`                                                                      |

---

## Troubleshooting

| Symptom                              | Likely Cause               | Fix                                                      |
| ------------------------------------ | -------------------------- | -------------------------------------------------------- |
| `ollama` command not found           | PATH not refreshed         | Re‑open terminal or reboot.                              |
| Download stalls or never starts      | Corporate proxy / firewall | Use a different network or configure proxy settings.     |
| **CUDA error** / *GPU out of memory* | Model too large for GPU    | Choose a smaller model (e.g. `llama3:8b`) or run on CPU. |
| Very slow responses on CPU           | Expected on large models   | Try quantised variants (Q4, Q5) or use GPU acceleration. |

---

## Additional Resources

- **Model Library:** [https://ollama.com/library](https://ollama.com/library)
- **GitHub Repo:** [https://github.com/ollama/ollama](https://github.com/ollama/ollama)
- **Community Discord:** [https://discord.gg/ollama](https://discord.gg/ollama)

---

*Happy prompting!*  If you run into issues, open a discussion on the Ollama GitHub or contact the Khipus.ai team for assistance.

