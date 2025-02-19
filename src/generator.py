from transformers import pipeline
from typing import List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResponseGenerator:
    """
    A class to generate responses using a pre-trained language model.
    """

    def __init__(self, model_name: str = "facebook/opt-1.3b"):
        """
        Initialize the generator with a pre-trained model.
        :param model_name: Name of the pre-trained model to use.
        """
        try:
            self.generator = pipeline("text-generation", model=model_name, truncation=True)
            logger.info(f"Loaded model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise

    def generate_response(self, query: str, context: List[str]) -> str:
        """
        Generate a response based on the given query and context.
        :param query: The question to be answered.
        :param context: A list of relevant context strings.
        :return: A generated response string.
        """
        try:
            context_str = "\n".join(context)

            prompt = f"""
            You are a GDPR compliance assistant. Answer the user's question based on the provided context.
            If the context does not provide enough information, say "I don't know."

            Context:
            {context_str}

            Question:
            {query}

            Answer:
            """

            response = self.generator(
                prompt,
                max_length=500,   # Ensures the response is meaningful
                num_return_sequences=1,
                truncation=True,  # Ensures that input is not too long
                pad_token_id=50256  # Fixes EOS token issues
            )
            
            generated_text = response[0]['generated_text']

            # Debugging log
            logger.info(f"RAW MODEL OUTPUT: {generated_text}")

            # Extract the answer after "Answer:"
            answer = generated_text.split("Answer:")[-1].strip()

            # Handle empty or nonsensical responses
            if not answer or answer.lower() in ["i don't know.", ""]:
                return "I'm sorry, but I don't have enough information to answer that."

            return answer
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I'm sorry, I couldn't generate a response. Please try again."
