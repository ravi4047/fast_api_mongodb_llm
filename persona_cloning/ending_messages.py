class EndingMessageHandler:
    """
    Check that either user is saying bye, good bye, good night, talk to you later, gn, see you later
    and is ready to end the message for now.
    So, you need to either end the message or if the topic is very important going on, then tell something about it.

    I mean do not hardcode. Leave to the model I guess.

    What if someone frames the conversation like this:
        User: Hey tell me, what do we say to the person at night before leaving. It's Good night
        Assistant: (The hardcoded one) Will feel like it's actually ending the conversation. But in reality no!. So, I need the ending probability also.
    """
    end_conversation_prob:float = 0.0

    @staticmethod
    def ending_message_confidence(mssg:str):
        # EndingMessageHandler.end_conversation_prob+=1
        
        pass