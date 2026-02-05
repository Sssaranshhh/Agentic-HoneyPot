import random

class MockScammerAPI:
    """
    Simulates a scammer interacting with a victim.
    It has a set of scenarios and progresses through them.
    """
    def __init__(self):
        self.conversation_stage = 0
        self.scam_type = "lottery" # Default for this demo

    def initiate_conversation(self):
        """Returns the initial scam message."""
        self.conversation_stage = 1
        return "CONGRATULATIONS! You have won $1,000,000 in the International Lottery! Reply 'CLAIM' to receive your prize now!"

    def reply(self, user_message):
        """Generates a reply based on the conversation stage."""
        user_message = user_message.lower()
        
        if self.conversation_stage == 1:
            if "claim" in user_message or "yes" in user_message:
                self.conversation_stage = 2
                return "Great! To process your winning, we need to verify your identity. Please provide your Full Name and Bank Account Number."
            else:
                return "Sir, do not ignore this. This is a limited time offer. Reply 'CLAIM' immediately."
        
        elif self.conversation_stage == 2:
            self.conversation_stage = 3
            return "Thank you. Now, to transfer the funds, we need a small processing fee of $500. Please transfer to this secure UPI ID: scammer@upi or click this link to pay: http://secure-payment-gateway-fake.com/pay"
        
        elif self.conversation_stage == 3:
             return "I am waiting for the payment screenshot. Once done, money will be in your account in 5 minutes! Do not delay."

        return "Please send the processing fee immediately to scammer@upi."
