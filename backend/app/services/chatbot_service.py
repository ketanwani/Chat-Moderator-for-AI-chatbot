import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class ChatbotService:
    """Chatbot service that generates responses using LLMs"""

    def __init__(self):
        """Initialize chatbot with LLM provider"""
        self.llm_provider = os.getenv("LLM_PROVIDER", "openai").lower()
        self.llm_api_key = os.getenv("LLM_API_KEY", "")
        self.llm_model = os.getenv("LLM_MODEL", "")

        # System prompt for the chatbot
        self.system_prompt = """You are a helpful AI assistant. Provide clear, accurate, and helpful responses to user questions.
Be concise but informative. If you don't know something, admit it rather than making up information."""

        # Initialize the appropriate LLM client
        self.client = None
        self._initialize_llm()

    def _initialize_llm(self):
        """Initialize the LLM client based on provider"""
        try:
            if self.llm_provider == "openai":
                self._initialize_openai()
            elif self.llm_provider == "anthropic":
                self._initialize_anthropic()
            elif self.llm_provider == "ollama":
                self._initialize_ollama()
            else:
                logger.warning(f"Unknown LLM provider: {self.llm_provider}. Using fallback mode.")
        except Exception as e:
            logger.error(f"Error initializing LLM: {e}. Using fallback mode.")

    def _initialize_openai(self):
        """Initialize OpenAI client"""
        try:
            from openai import OpenAI

            if not self.llm_api_key:
                logger.warning("OpenAI API key not provided. Using fallback mode.")
                return

            self.client = OpenAI(api_key=self.llm_api_key)
            self.llm_model = self.llm_model or "gpt-3.5-turbo"
            logger.info(f"OpenAI client initialized with model: {self.llm_model}")
        except ImportError:
            logger.error("OpenAI library not installed. Run: pip install openai")
        except Exception as e:
            logger.error(f"Error initializing OpenAI: {e}")

    def _initialize_anthropic(self):
        """Initialize Anthropic Claude client"""
        try:
            import anthropic

            if not self.llm_api_key:
                logger.warning("Anthropic API key not provided. Using fallback mode.")
                return

            self.client = anthropic.Anthropic(api_key=self.llm_api_key)
            self.llm_model = self.llm_model or "claude-3-sonnet-20240229"
            logger.info(f"Anthropic client initialized with model: {self.llm_model}")
        except ImportError:
            logger.error("Anthropic library not installed. Run: pip install anthropic")
        except Exception as e:
            logger.error(f"Error initializing Anthropic: {e}")

    def _initialize_ollama(self):
        """Initialize Ollama (local) client"""
        try:
            import ollama

            self.client = ollama
            self.llm_model = self.llm_model or "llama2"
            logger.info(f"Ollama client initialized with model: {self.llm_model}")
        except ImportError:
            logger.error("Ollama library not installed. Run: pip install ollama")
        except Exception as e:
            logger.error(f"Error initializing Ollama: {e}")

    def generate_response(self, message: str, conversation_history: Optional[list] = None) -> str:
        """
        Generate a response to user message using LLM

        Args:
            message: User's message
            conversation_history: Optional list of previous messages

        Returns:
            Bot response
        """
        if not self.client:
            return self._fallback_response(message)

        try:
            if self.llm_provider == "openai":
                return self._generate_openai_response(message, conversation_history)
            elif self.llm_provider == "anthropic":
                return self._generate_anthropic_response(message, conversation_history)
            elif self.llm_provider == "ollama":
                return self._generate_ollama_response(message, conversation_history)
            else:
                return self._fallback_response(message)
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            return self._fallback_response(message)

    def _generate_openai_response(self, message: str, conversation_history: Optional[list] = None) -> str:
        """Generate response using OpenAI"""
        messages = [{"role": "system", "content": self.system_prompt}]

        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)

        # Add current message
        messages.append({"role": "user", "content": message})

        response = self.client.chat.completions.create(
            model=self.llm_model,
            messages=messages,
            max_tokens=500,
            temperature=0.7,
        )

        return response.choices[0].message.content

    def _generate_anthropic_response(self, message: str, conversation_history: Optional[list] = None) -> str:
        """Generate response using Anthropic Claude"""
        # Anthropic uses a different format for conversation history
        messages = []

        if conversation_history:
            messages.extend(conversation_history)

        messages.append({"role": "user", "content": message})

        response = self.client.messages.create(
            model=self.llm_model,
            max_tokens=500,
            system=self.system_prompt,
            messages=messages,
        )

        return response.content[0].text

    def _generate_ollama_response(self, message: str, conversation_history: Optional[list] = None) -> str:
        """Generate response using Ollama (local)"""
        messages = [{"role": "system", "content": self.system_prompt}]

        if conversation_history:
            messages.extend(conversation_history)

        messages.append({"role": "user", "content": message})

        response = self.client.chat(
            model=self.llm_model,
            messages=messages,
        )

        return response['message']['content']

    def _fallback_response(self, message: str) -> str:
        """
        Fallback response when LLM is not available
        Uses simple keyword-based responses
        """
        message_lower = message.lower()

        # Greeting
        if any(word in message_lower for word in ["hello", "hi", "hey", "greetings"]):
            return "Hello! I'm an AI assistant. How can I help you today?"

        # Financial
        elif any(word in message_lower for word in ["stock", "investment", "bitcoin", "crypto", "finance", "money", "trading"]):
            return "I can provide general information about finance and investing. However, for specific investment advice, please consult with a licensed financial advisor. What would you like to know?"

        # Medical
        elif any(word in message_lower for word in ["sick", "pain", "doctor", "medicine", "health", "symptom", "disease"]):
            return "For medical advice and diagnosis, please consult with a qualified healthcare professional. I can provide general health information. What's your question?"

        # Technology
        elif any(word in message_lower for word in ["code", "programming", "python", "javascript", "software"]):
            return "I can help with programming and technology questions. What specific topic would you like assistance with?"

        # Default
        else:
            return f"Thank you for your question. I'm currently running in fallback mode (LLM not configured). To enable full AI responses, please configure an LLM provider. Your message was: '{message[:50]}...'"


# Singleton instance
chatbot_service = ChatbotService()
