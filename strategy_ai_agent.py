import os
import requests
import json

class StrategyAIAgent:
    def __init__(self):
        self.api_key = os.environ.get("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.market_trends = {
            "Mobile-first": "Prioritizing mobile user experience in all digital strategies",
            "Video Content": "Short-form videos, live streaming, and interactive video content",
            "Personalization": "Tailoring content and offers to individual user preferences",
            "AI-driven Marketing": "Utilizing AI for predictive analytics and automated marketing tasks",
            "Voice Search Optimization": "Adapting content for voice-activated devices and searches",
            "Sustainability": "Eco-friendly practices and messaging in marketing campaigns"
        }

    def analyze_market_trends(self, product, additional_info=None):
        """Provide detailed market trend analysis."""
        prompt = f"Conduct a comprehensive market trend analysis for {product}. Your analysis should include:\n"
        prompt += "1. Identification and detailed description of at least 5 significant trends impacting the industry\n"
        prompt += "2. Quantitative data supporting each trend (market size, growth rates, adoption rates, etc.)\n"
        prompt += "3. Analysis of how each trend specifically impacts the marketing and sales of {product}\n"
        prompt += "4. Potential opportunities and threats arising from these trends\n"
        prompt += "5. Recommendations for leveraging positive trends and mitigating risks from negative ones\n"
        prompt += "6. Short-term (6-12 months) and long-term (2-5 years) projections for each trend\n"
        if additional_info:
            prompt += f"\nConsider the following additional context in your analysis:\n{additional_info}"
        return self.call_openrouter_api(prompt)

    def call_openrouter_api(self, prompt):
        """Make a streaming API call to OpenRouter's Anthropic Claude-3.5-sonnet model."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "anthropic/claude-3.5-sonnet",
            "messages": [{"role": "user", "content": prompt}],
            "stream": True
        }
        response = requests.post(self.base_url, headers=headers, json=data, stream=True)
        if response.status_code == 200:
            full_response = ""
            for line in response.iter_lines():
                if line:
                    chunk = line.decode('utf-8')
                    if chunk.startswith("data: "):
                        chunk_data = json.loads(chunk[6:])
                        if chunk_data['choices'][0]['finish_reason'] is None:
                            content = chunk_data['choices'][0]['delta'].get('content', '')
                            full_response += content
                            print(content, end='', flush=True)
            print()  # Print a newline at the end
            return full_response
        else:
            return f"Error: {response.status_code}, {response.text}"

    def respond_to_agent(self, message):
        """Respond to messages from other agents."""
        prompt = f"As a strategy AI agent, respond to the following message from another agent: {message}"
        return self.call_openrouter_api(prompt)
