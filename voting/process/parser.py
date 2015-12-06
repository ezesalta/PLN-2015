from iepy.preprocess.pipeline import BasePreProcessStepRunner, PreProcessSteps
from nltk.tree import Tree

__author__ = 'Ezequiel Medina'


class ParserRunner(BasePreProcessStepRunner):
    """Does Parsing over IEDocuments.

    - If override=True, no matter if are already computed or not, will do
    and store them on the doc.
    - If override=False and the step are done on the document, will
    do nothing.
    """

    def __init__(self, override=False, increment=False, lang='en'):
        if lang != 'en':
            # We are right now only providing english lemmatization.
            # But if you need something else, this
            # is a good place to do it.
            raise NotImplemented
        self.lang = lang
        self.override = override
        self.increment = increment
        self.step = PreProcessSteps.syntactic_parsing

    def __call__(self, doc):
        par_done = doc.was_preprocess_step_done(self.step)
        if self.override or not par_done:
            # Ok, let's do it
            result = parsing(doc)
            doc.set_syntactic_parsing_result(result['tree'])
            doc.save()


def parsing(doc):
    sentences = doc.sentences
    tokens = doc.tokens
    tree = Tree('S', [])
    for i, s in enumerate(sentences):
        if i < len(sentences) - 1:
            terminals = tokens[s: sentences[i+1]]
            t = Tree(str(s), terminals)
            tree.append(t)
    # tree.draw()

    return {'tree': tree}
