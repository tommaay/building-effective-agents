# Building Effective Agents

**Dec 20, 2024**

Over the past year, we've worked with dozens of teams building large language model (LLM) agents across industries. Consistently, the most successful implementations weren't using complex frameworks or specialized libraries. Instead, they were building with simple, composable patterns.

In this post, we share what we’ve learned from working with our customers and building agents ourselves, and give practical advice for developers on building effective agents.

---

## What Are Agents?

"Agent" can be defined in several ways. Some customers define agents as fully autonomous systems that operate independently over extended periods, using various tools to accomplish complex tasks. Others use the term to describe more prescriptive implementations that follow predefined workflows. At Anthropic, we categorize all these variations as agentic systems but draw an important architectural distinction between workflows and agents:

- **Workflows**: Systems where LLMs and tools are orchestrated through predefined code paths.
- **Agents**: Systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks.

Below, we will explore both types of agentic systems in detail. In **Appendix 1** (“Agents in Practice”), we describe two domains where customers have found particular value in using these kinds of systems.

---

## When (and When Not) to Use Agents

When building applications with LLMs, we recommend finding the simplest solution possible and only increasing complexity when needed. This might mean not building agentic systems at all. Agentic systems often trade latency and cost for better task performance, and you should consider when this tradeoff makes sense.

- **Workflows**: Offer predictability and consistency for well-defined tasks.
- **Agents**: Are better suited for flexibility and model-driven decision-making at scale.

For many applications, optimizing single LLM calls with retrieval and in-context examples is usually enough.

---

## When and How to Use Frameworks

There are many frameworks that make agentic systems easier to implement, including:

- **LangGraph** from LangChain
- **Amazon Bedrock's AI Agent framework**
- **Rivet**, a drag-and-drop GUI LLM workflow builder
- **Vellum**, another GUI tool for building and testing complex workflows

These frameworks simplify tasks like calling LLMs, defining tools, and chaining calls together. However, they can obscure underlying prompts and responses, making debugging harder. Start by using LLM APIs directly, and if you use a framework, ensure you understand the underlying code.

---

## Building Blocks, Workflows, and Agents

### Building Block: The Augmented LLM

The basic building block of agentic systems is an LLM enhanced with augmentations such as retrieval, tools, and memory. Key aspects to focus on:

1. **Tailor these capabilities** to your specific use case.
2. **Provide an easy, well-documented interface** for your LLM.

---

### Workflow Patterns

#### **1. Prompt Chaining**

Decomposes a task into a sequence of steps where each LLM call processes the output of the previous one.

**When to Use**: Tasks easily decomposed into fixed subtasks, where latency is traded for higher accuracy.

**Examples**:

- Generating marketing copy, then translating it.
- Writing an outline, validating it, then creating a document.

---

#### **2. Routing**

Classifies an input and directs it to specialized follow-up tasks.

**When to Use**: Complex tasks with distinct categories handled separately.

**Examples**:

- Directing customer queries to appropriate downstream processes.
- Routing easy questions to smaller models and hard ones to more capable models.

---

#### **3. Parallelization**

Simultaneous task execution, either by sectioning or voting.

**When to Use**: Tasks that benefit from speed (sectioning) or diverse perspectives (voting).

**Examples**:

- Sectioning: Evaluating different aspects of model performance in parallel.
- Voting: Reviewing code for vulnerabilities using multiple prompts.

---

#### **4. Orchestrator-Workers**

A central LLM dynamically breaks down tasks, delegates them, and synthesizes results.

**When to Use**: Complex, unpredictable tasks where subtasks aren’t predefined.

**Examples**:

- Coding products making changes to multiple files.
- Search tasks requiring analysis from multiple sources.

---

#### **5. Evaluator-Optimizer**

One LLM generates responses while another evaluates and provides feedback in a loop.

**When to Use**: Clear evaluation criteria and measurable iterative improvement.

**Examples**:

- Literary translation refined through critiques.
- Iterative searches for comprehensive information.

---

## Agents

Agents operate autonomously, planning and executing tasks based on dynamic inputs. They rely on environmental feedback to assess progress and adjust actions.

### **When to Use Agents**

- For open-ended problems with unpredictable steps.
- When flexibility and autonomy outweigh costs and risks.

### **Examples**:

- **Coding Agents**: Solve tasks involving edits across multiple files.
- **Customer Support Agents**: Combine conversation with actions like issuing refunds.

---

## Combining and Customizing Patterns

These building blocks and workflows are not prescriptive. Developers can combine and adapt them based on specific use cases. The key to success is measuring performance and iterating on implementations.

---

## Summary

Success in the LLM space isn't about building the most sophisticated system. It's about building the right system for your needs. Start with simple prompts, optimize them, and only add complexity when simpler solutions fall short.

### Core Principles:

1. Maintain simplicity in design.
2. Prioritize transparency in planning steps.
3. Carefully craft the agent-computer interface (ACI).

---

## Acknowledgements

Written by Erik Schluntz and Barry Zhang. This work draws upon our experiences building agents at Anthropic and the valuable insights shared by our customers.

---

## Appendix 1: Agents in Practice

### A. **Customer Support**

- Combines conversational flow with tool integration.
- Success measured through resolution rates.

### B. **Coding Agents**

- Verifiable through automated tests.
- Iterates on solutions using test feedback.

---

## Appendix 2: Prompt Engineering Your Tools

### Best Practices:

- Give the model enough tokens to "think."
- Use natural formats for tools (e.g., JSON or markdown).
- Avoid unnecessary formatting overhead.

### Key Tips:

- Include example usage and edge cases in tool definitions.
- Test extensively to refine tool interfaces.
- Simplify parameters to minimize errors.

---
