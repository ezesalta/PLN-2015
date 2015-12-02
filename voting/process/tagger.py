from iepy.preprocess.pipeline import BasePreProcessStepRunner, PreProcessSteps

__author__ = 'Ezequiel Medina'


class TaggerRunner(BasePreProcessStepRunner):
    """Does Tagging over IEDocuments.

    - If override=True, no matter if are already computed or not, will do
    and store them on the doc.
    - If override=False and the step are done on the document, will
    do nothing.
    """
    step = PreProcessSteps.tagging

    def __init__(self, override=False, increment=False, lang='en'):
        if lang != 'en':
            # We are right now only providing english tagging.
            # But if you need something else, this
            # is a good place to do it.
            raise NotImplemented
        self.lang = lang
        self.override = override
        self.increment = increment
        self.tagg_step = PreProcessSteps.tagging

    def __call__(self, doc):
        tagg_done = doc.was_preprocess_step_done(self.tagg_step)
        if self.override or not tagg_done:
            # Ok, let's do it
            result = tagging(doc.tokens)
            doc.set_tagging_result(result['tags'])
            doc.save()


def tagging(tokens):
    tags = []
    for token in tokens:
        tags.append('X')

    return {'tags': tags}
