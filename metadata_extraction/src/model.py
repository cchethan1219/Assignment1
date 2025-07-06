from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering

class MetadataExtractorModel:
    def __init__(self, model_name="deepset/roberta-base-squad2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForQuestionAnswering.from_pretrained(model_name)
        self.qa_pipeline = pipeline("question-answering", model=self.model, tokenizer=self.tokenizer)

        self.questions = {
            "Agreement Value": "What is the agreement value?",
            "Agreement Start Date": "What is the agreement start date?",
            "Agreement End Date": "What is the agreement end date?",
            "Renewal Notice": "What is the renewal notice period?",
            "Party One": "Who is the first party?",
            "Party Two": "Who is the second party?"
        }

    def extract_metadata(self, context):
        results = {}
        for field, question in self.questions.items():
            try:
                answer = self.qa_pipeline({"context": context, "question": question})
                results[field] = answer["answer"]
            except:
                results[field] = ""
        return results
