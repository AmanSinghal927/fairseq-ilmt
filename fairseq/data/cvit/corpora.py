from . import DATASET_REGISTRY
from . import dataset_register, data_abspath
from . import Corpus, sanity_check


@dataset_register('iitb-hi-en', ['train', 'dev', 'test'])
def IITB_meta(split):
    corpora = []
    for lang in ['en', 'hi']:
        sub_path = 'filtered-iitb/{}.{}'.format(split, lang)
        corpus = Corpus('iitb-hi-en', data_abspath(sub_path), lang)
        corpora.append(corpus)
    return corpora

@dataset_register('monolingual', ['train'])
def MONO_meta(split):
    corpora = []
    for lang in ['en','pa']:
        sub_path = 'monolingual-en-pa/train.{}'.format(split, lang)
        corpus = Corpus('monolingual', data_abspath(sub_path), lang)
        corpora.append(corpus)
    return corpora

@dataset_register('iitb-hi-en-bt', ['train', 'dev', 'test'])
def IITB_bt_meta(split):
    corpora = []
    for lang in ['en', 'hi']:
        sub_path = 'iitb_bt/{}.{}'.format(split, lang)
        corpus = Corpus('iitb-hi-en', data_abspath(sub_path), lang)
        corpora.append(corpus)
    return corpora

@dataset_register('odi-en-corp1.0', ['train','dev','test'])
def OdiEnCorp_meta(split):
    corpora = []
    for lang in ['en', 'or']:
        sub_path = 'OdiEnCorp/{}.{}'.format(split, lang)
        corpus = Corpus('odi-en-corp1.0', data_abspath(sub_path), lang)
        corpora.append(corpus)
    return corpora


@dataset_register('national-newscrawl', ['train', 'dev', 'test'])
def NationalNewscrawl_meta(split):
    if split in ['dev', 'test']:
        return []
    corpora = []
    for lang in ['en', 'hi']:
        sub_path = 'national-newscrawl/national.{}'.format(lang)
        corpus = Corpus('national-newscrawl', data_abspath(sub_path), lang)
        corpora.append(corpus)
    return corpora

# @dataset_register('monolingual_en_hi_pa', ['train'])
# def PIBOriya_meta(split):
#     corpora = []
#     for lang in ['en']:
#         sub_path = 'monolingual_en_hi_pa/train.{}'.format(lang)
#         corpus = Corpus('monolingual_en_hi_pa', data_abspath(sub_path), lang)
#         corpora.append(corpus)
#     return corpora


@dataset_register('wat-ilmpc', ['train'])
def WAT_meta(split):
    corpora = []
    #langs = ['bn', 'hi', 'ml', 'si', 'ta', 'te', 'ur']
    langs = ['ml']
    for lang in langs:
        for src in ['en',lang]:
            sub_path = 'indic_languages_corpus/bilingual/en-{}/{}.{}'.format(
                    lang, split, src
            )
            corpus_name = 'wat-ilmpc-{}-{}'.format('en',lang)
            corpus = Corpus(corpus_name, data_abspath(sub_path), src)
            corpora.append(corpus)
    return corpora

@dataset_register('ufal-en-tam', ['train'])
def UFALEnTam_meta(split):
    corpora = []
    for lang in ['en', 'pa']:
        sub_path = 'ufal-en-tam/{}.{}'.format(split, lang)
        corpus = Corpus('ufal-en-tam', data_abspath(sub_path), lang)
        corpora.append(corpus)
    return corpora

@dataset_register('ilci_pa', ['train', 'dev', 'test'])
def ILCI_meta(split):
    # if split in ['dev', 'test']:
    #     return []
    corpora = []
    langs = ['en', 'pa']
    # from .utils import canonicalize

    for lang in langs:
        sub_path = 'ilci_pa_en/{}.{}'.format(split,lang)
        # _lang = canonicalize(lang)
        corpus = Corpus('ilci_pa', data_abspath(sub_path), lang)
        corpora.append(corpus)
    return corpora

@dataset_register('bible-en-te', ['train', 'dev', 'test'])
def BIBLEEnTe_meta(split):
    corpora = []
    for lang in ['en', 'te']:
        sub_path = 'bible-en-te/bible.{}.{}'.format(split, lang)
        corpus = Corpus('bible-en-te', data_abspath(sub_path), lang)
        corpora.append(corpus)
    return corpora

@dataset_register('mann-ki-baat-test', ['test'])
def MannKiBaat_meta(split):
    corpora = []
    for lang in ['hi','en']:
        sub_path = 'mann-ki-baat-test/test.{}'.format(lang)
        corpus = Corpus('mann-ki-baat-test', data_abspath(sub_path), lang)
        corpora.append(corpus)
    return corpora

@dataset_register('eenadu-en-te', ['train'])
def EenaduBacktrans_meta(split):
    if split in ['dev', 'test']:
        return []

    corpora = []
    for lang in ['en','te']:
        sub_path = 'eenadu-en-te/train.{}'.format(lang)
        corpus = Corpus('eenadu-en-te', data_abspath(sub_path), lang)
        corpora.append(corpus)
    return corpora

if __name__ == '__main__':
    def merge(*_as):
        _ase = []
        for a in _as:
            _ase.extend(a)
        return _ase

    ls = []
    for key in DATASET_REGISTRY:
        splits, f = DATASET_REGISTRY[key]
        for split in splits:
            ls.append(f(split))

    _all = merge(*ls)
    sanity_check(_all)

