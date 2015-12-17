from iepy.preprocess.pipeline import BasePreProcessStepRunner, PreProcessSteps

__author__ = 'Ezequiel Medina'


class SentencerRunner(BasePreProcessStepRunner):
    """Does Segmentation over IEDocuments.

    - If override=True, no matter if are already computed or not, will do
    and store them on the doc.
    - If override=False and the step are done on the document, will
    do nothing.
    """
    step = PreProcessSteps.sentencer

    def __init__(self, override=False, increment=False, lang='en'):
        if lang != 'en':
            # We are right now only providing english segmentation.
            # But if you need something else, this
            # is a good place to do it.
            raise NotImplemented
        self.lang = lang
        self.override = override
        self.increment = increment
        self.snt_step = PreProcessSteps.sentencer

    def __call__(self, doc):
        snt_done = doc.was_preprocess_step_done(self.snt_step)
        if self.override or not snt_done:
            # Ok, let's do it
            result = sentencer(doc.tokens)
            doc.set_sentencer_result(result['sentences'])
            doc.save()


def sentencer(tokens):
    sentences = [0]
    votes = ['AFIRMATIVO', 'NEGATIVO', 'ABSTENCION', 'AUSENTE']
    for j, token in enumerate(tokens):
        if token in votes:
            sentences.append(j + 1)
    if sentences[-1] != len(tokens):
        sentences.append(len(tokens))

    return {'sentences': sentences}
