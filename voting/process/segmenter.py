from iepy.preprocess.pipeline import BasePreProcessStepRunner, PreProcessSteps
from collections import namedtuple
__author__ = 'Ezequiel Medina'

# Representation of Segments that a Segmenter found
RawSegment = namedtuple('RawSegment', 'offset offset_end entity_occurrences')

class SegmenterRunner(BasePreProcessStepRunner):
    """Does Segmentation over IEDocuments.

    - If override=True, no matter if are already computed or not, will do
    and store them on the doc.
    - If override=False and the step are done on the document, will
    do nothing.
    """

    def __init__(self, override=False, increment=False, lang='en'):
        if lang != 'en':
            # We are right now only providing english segmentation.
            # But if you need something else, this
            # is a good place to do it.
            raise NotImplemented
        self.lang = lang
        self.override = override
        self.increment = increment
        self.step = PreProcessSteps.segmentation

    def __call__(self, doc):
        seg_done = doc.was_preprocess_step_done(self.step)
        if self.override or not seg_done:
            # Ok, let's do it
            result = segmentation(doc)
            doc.set_segmentation_result(result['segments'])
            doc.save()


def segmentation(doc):
    sentences = doc.sentences
    tokens = doc.tokens
    segments = []
    entity_occs = list(doc.get_entity_occurrences())
    #segments.append(RawSegment(sentences[0], sentences[-1], entity_occs))

    for s, i in enumerate(sentences):
        if s >= len(sentences) - 1:
            break
        j = sentences[s + 1]
        segments.append(RawSegment(i, j, entity_occs))

    return {'segments': segments}
