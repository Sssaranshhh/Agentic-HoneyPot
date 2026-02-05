import re
import json
import random

class HoneyPotAgent:
    def __init__(self, persona="naive_elderly"):
        self.persona = persona
        self.conversation_history = []
        self.extracted_data = {
            "upi_ids": [],
            "bank_accounts": [],
            "phishing_links": []
        }
        self.state = "INITIAL" # INITIAL, ENGAGED, COMPLYING, STALLING
        self.last_scammer_message = ""
        self.turn_count = 0

    def detect_scam(self, message):
        """
        Improved detection logic.
        """
        message = message.lower()
        scam_score = 0
        
        keywords = {
            "money": 2, "winner": 3, "lottery": 3, "fund": 2,
            "claim": 2, "urgent": 1, "immediately": 1, "bank": 2,
            "password": 3, "otp": 3, "fee": 2, "verify": 1
        }
        
        for word, score in keywords.items():
            if word in message:
                scam_score += score
                
        return scam_score >= 2

    def _get_random_response(self, intent):
        """Returns a randomized response based on the intent."""
        templates = {
            "shock_and_awe": [
                "Oh my goodness! Is this really true? I never win anything!",
                "Wow! God has finally answered my prayers. Are you sure?",
                "I am shaking right now. This is the best news ever!"
            ],
            "confusion": [
                "I am not very good with computers. My grandson usually helps me.",
                "Wait, I am confused. Which button do I press?",
                "Can you explain that one more time? I am a bit slow."
            ],
            "compliance": [
                "Okay, I will do exactly as you say. I don't want to lose the prize.",
                "CLAIM", 
                "YES, I want to claim it.",
                "I am doing it now."
            ],
            "hesitation": [
                "But why do I need to pay a fee if I won money?",
                "My neighbor said this might be dangerous. Are you a real person?",
                "I don't have online banking. Can I send cash?"
            ],
            "stalling": [
                "Hold on, my internet is very slow today...",
                "I am looking for my reading glasses. Please wait.",
                "The page is buffering. Just a moment dear."
            ]
        }
        return random.choice(templates.get(intent, ["I don't understand."]))

    def generate_response(self, message):
        """
        Generates a context-aware response using a simple state machine.
        """
        self.last_scammer_message = message
        message = message.lower()
        response = ""

        # Update State based on Scammer's input
        if "reply 'claim'" in message or "reply claim" in message:
            self.state = "COMPLYING"
        elif "fee" in message or "pay" in message or "transfer" in message:
            self.state = "STALLING"
        elif self.state == "INITIAL":
            self.state = "ENGAGED"

        # Generate Response based on State
        if self.state == "COMPLYING":
            # If asked to claim, we must comply to progress the scam
            response = self._get_random_response("compliance")
            # Reset state to engaged after complying to see what happens next
            self.state = "ENGAGED" 
        
        elif self.state == "STALLING":
             # If asked for money, stall to keep them on the line
             response = self._get_random_response("stalling")
        
        elif self.state == "ENGAGED":
            if "bank" in message or "account" in message:
                response = self._get_random_response("confusion")
            elif "lottery" in message:
                response = self._get_random_response("shock_and_awe")
            else:
                response = self._get_random_response("hesitation")
        
        else:
             response = self._get_random_response("confusion")

        self.conversation_history.append({"role": "agent", "content": response})
        self.turn_count += 1
        return response

    def extract_intelligence(self, message):
        """
        Extracts complex logic for intelligence using Regex.
        """
        # Improved Regex for UPI (e.g., name@bank, phone@upi)
        upi_pattern = r"\b[a-zA-Z0-9.\-_]+@[a-zA-Z]{3,}\b"
        upis = re.findall(upi_pattern, message)
        self.extracted_data["upi_ids"].extend(upis)

        # Improved Regex for URLs (http, https, www)
        url_pattern = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(?:/[-\w./?%&=]*)?"
        urls = re.findall(url_pattern, message)
        self.extracted_data["phishing_links"].extend(urls)
        
        # Simple Bank Account (9-18 digits, avoiding likely timestamps/phones if possible)
        # We look for digits that are NOT part of a larger string
        account_pattern = r"(?<!\d)\d{9,18}(?!\d)"
        accounts = re.findall(account_pattern, message)
        # Simple filter: Assume bank accounts usually don't start with 0 or 1 maybe? 
        # For now, just detecting digits is enough for the prototype.
        self.extracted_data["bank_accounts"].extend(accounts)

    def get_structured_intelligence(self):
         # Deduplicate lists
        self.extracted_data["upi_ids"] = list(set(self.extracted_data["upi_ids"]))
        self.extracted_data["bank_accounts"] = list(set(self.extracted_data["bank_accounts"]))
        self.extracted_data["phishing_links"] = list(set(self.extracted_data["phishing_links"]))
        
        return json.dumps(self.extracted_data, indent=4)
