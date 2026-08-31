import os

class TemplateParser:
    
    def __init__(self, language: str=None, default_language='en'):
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.default_language = default_language
        self.language = None

        self.set_language(language)

    def set_language(self, language: str):
        if not language:
            self.language = self.default_language

        language_path = os.path.join(self.current_path, "localies", language)
        if os.path.exists(language_path):
            self.language = language
        else:
            self.language = self.default_language

    def get(self, group: str, key: str, vars: dict={}):
        # Attributes Explaining:
        # group: go to rag.py template file in each language
        # key  : you will find attributes such as system_prompt, document_prompt, footer_prompt
        # vars : you will also find some variables in the prompt such as doc_num, and chunk_text

        if not group or not key:
            return None

        group_path = os.path.join(self.current_path, "localies", self.language, f"{group}.py")
        targeted_language = self.language
        if not os.path.exists(group_path):
            group_path = os.path.join(self.current_path, "localies", self.default_language, f"{group}.py")
            targeted_language = self.default_language

        if not os.path.exists(group_path):
             return None

        # import function for runtime importing
        module = __import__(f"src.stores.llm.templates.localies.{targeted_language}.{group}", fromlist=[group])

        if not module:
            return None

        key_attr = getattr(module, key)
        return key_attr.substitute(vars) 