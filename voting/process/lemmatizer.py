from iepy.preprocess.pipeline import BasePreProcessStepRunner, PreProcessSteps

__author__ = 'Ezequiel Medina'


class LemmatizeRunner(BasePreProcessStepRunner):
    """Does Lemmatization over IEDocuments.

    - If override=True, no matter if are already computed or not, will do
    and store them on the doc.
    - If override=False and the step are done on the document, will
    do nothing.
    """
    step = PreProcessSteps.lemmatization

    def __init__(self, override=False, increment=False, lang='en'):
        if lang != 'en':
            # We are right now only providing english lemmatization.
            # But if you need something else, this
            # is a good place to do it.
            raise NotImplemented
        self.lang = lang
        self.override = override
        self.increment = increment
        self.lemm_step = PreProcessSteps.lemmatization

    def __call__(self, doc):
        lemm_done = doc.was_preprocess_step_done(self.lemm_step)
        if self.override or not lemm_done:
            # Ok, let's do it
            result = lemmatizer(doc.tokens)
            doc.set_lemmatization_result(result['lemmas'])
            doc.save()


def lemmatizer(tokens):
    lemmas = []
    for token in tokens:
        lemmas.append(token)

    return {'lemmas': lemmas}
