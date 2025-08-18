## Prompt Configuration Comparison

| Aspect                 | Instructions                                                                                                                                               | Prompt                                                                                                     |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Configuration Style    | In-code (embedded in Python script).                                                                                                                       | External (via OpenAI API/dashboard).                                                                       |
| Static vs. Dynamic     | Can be static string or dynamic function (sync/async, context-aware).                                                                                      | Inherently dynamic; uses DynamicPromptFunction or API IDs for runtime changes.                             |
| Scope                  | Primarily the system prompt text.                                                                                                                          | Broader: Can configure instructions, tools, and other agent params dynamically.                            |
| Precedence/Interaction | Takes effect directly if provided; may conflict if prompt is also set (unresolved in docs GitHub issue notes potential overrides, but no official answer). | Likely overrides or merges with instructions when both are used, especially for dashboard-managed prompts. |
| Usability              | Works with any model; simple for prototyping.                                                                                                              | Limited to OpenAI models; requires Responses API integration.                                              |
| Customization          | Code-based, version-controlled.                                                                                                                            | Platform-based, for A/B testing or team collaboration without code changes.                                |


## Use Cases

### Instructions:

`Prototyping and Simple Agents`: Ideal for quick setups where the agent's behavior is fixed or lightly context-dependent. E.g., a weather agent with static instructions: "Respond with current weather data in bullet points." Use dynamic instructions for personalization, like injecting user-specific details (e.g., "Greet the user by name from context").
Multi-Agent Systems: In handoffs, instructions define specialties (e.g., "Handle only math queries").
When to Choose: For developer-controlled, code-centric apps. Avoid for production if frequent prompt tweaks are needed, as it requires code updates.


### Prompt:

`Production and Scalable Deployments`: Perfect for environments where prompts need updating without code changes, like A/B testing response styles or integrating with OpenAI's prompt management dashboard. E.g., a customer support agent where admins update guidelines via the dashboard.
Dynamic, API-Driven Workflows: Use with Responses API for runtime config, such as loading prompts based on user sessions or experiments.
When to Choose: For teams separating prompt engineering from coding, or when leveraging OpenAI's ecosystem tools. Not suitable for non-OpenAI models or offline prototyping.


`Combined Use Cases`: In hybrid scenarios, instructions could provide a baseline, with prompt overriding for specific deployments (e.g., instructions for dev, prompt for prod). However, test carefully due to potential overlaps.
