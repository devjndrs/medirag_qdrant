import re
from core.interfaces import BaseCleaner

class MedicalTextCleaner(BaseCleaner):

    def clean(self, text: str) -> str:
        text = re.sub('\\s+', ' ', text).strip()
        text = re.sub('\\[\\d+\\]', '', text)
        text = re.sub('http\\S+', '', text)
        text = text.replace('•', '')
        return text