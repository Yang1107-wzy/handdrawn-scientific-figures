# Platforms and invocation

This is a portable Agent Skill folder. It does not bundle an image model or an API key.

## Codex

Install the full folder into the supported user skills location using the repository installer, or a project skill folder. Invoke:

```text
Use $handdrawn-scientific-figures to draw a method figure from this paper. Keep the source relations, and deliver a paper PNG/PDF/SVG with editable labels.
```

Use the host's built-in image-generation tool when present; the helper scripts do the accurate composition. Start a new session if the installed skill has not appeared. Do not install a paid API runner or change the user's endpoint just to emulate another environment.

Official discovery paths: [Codex skills](https://learn.chatgpt.com/docs/build-skills).

## Claude Code

Install the same full folder into the personal or project Claude Code skill location. Invoke:

```text
/handdrawn-scientific-figures Create a 16:9 research illustration for this method, preserving the feedback relationships.
```

If a connected raster image tool is available, use it. Otherwise prepare the complete art prompt and exact layer manifest, or produce a native SVG diagram where suitable. Do not claim the raster illustration was generated. The installer does not install Claude Code or upload a skill to Claude.ai.

Official discovery paths: [Claude Code skills](https://code.claude.com/docs/en/skills).

## ChatGPT and Claude chat

Paste [the master prompt](master-prompt.md), fill the CONTENT BRIEF and attach source material/reference art when available. Keep the same fixed visual language across tasks. When the chat can generate images, ask for original label-free art and then exact labels as separate layers where file/code tools exist.

Claude can create HTML/SVG diagrams and charts but does not itself generate photographs or raster illustrations like an image model. Use an available image tool for that layer. [Official Claude capabilities](https://support.claude.com/en/articles/9002504-can-claude-produce-images).

A plain prompt works without native skill installation. Prompt adherence, font substitution and tool capabilities vary; evaluate the actual output rather than promising identical pixels across models.
