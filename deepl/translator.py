import requests
import json
import re

request_id = 0


def translate(text, source="auto", target=None, preferred_langs=[]):
    paragraphs = _split_paragraphs(text)
    sentences = _request_split_sentences(paragraphs, source, preferred_langs)
    result = _request_translate(sentences, source, target, preferred_langs)
    translation = _insert_translation(result["translations"], text)

    return translation, {
        "source": result["source"],
        "target": result["target"]
    }


def _split_paragraphs(text):
    cleaned_paragraphs = []

    # Split into paragraphs
    parts = re.split(r'(?:\s*\n)+\s*', text)
    for part in parts:
        re.sub(r'\s+', " ", part)
        part = part.lstrip().rstrip()
        if len(part) > 0:
            cleaned_paragraphs.append(part)

    return cleaned_paragraphs


def _request_split_sentences(paragraphs, source, preferred_langs):
    request_paragraphs = []
    request_paragraph_ids = []

    splitted_paragraphs = []

    for i, paragraph in enumerate(paragraphs):
        # Check if the paragraph contains more than one sentence.
        if re.search(r'[.!?\":].*\S.*$', paragraph, re.M):
            request_paragraphs.append(paragraph)
            request_paragraph_ids.append(i)
            splitted_paragraphs.append([])
        else:
            splitted_paragraphs.append([paragraph])

    global request_id
    request_id += 1

    current_id = request_id

    url = "https://www.deepl.com/jsonrpc"
    headers = {}  # {'content-type': 'application/json'}

    payload = {
        "method": "LMT_split_into_sentences",
        "params": {
            "texts": [p for p in request_paragraphs],
            "lang": {
                "lang_user_selected": source,
                "user_preferred_langs": json.dumps(preferred_langs),
            },
        },
        "jsonrpc": "2.0",
        "id": current_id,
    }

    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    assert response["jsonrpc"]
    assert response["id"] == current_id

    for i, paragraph in enumerate(response["result"]["splitted_texts"]):
        splitted_paragraphs[request_paragraph_ids[i]] = paragraph

    sentences = [s for paragraph in splitted_paragraphs for s in paragraph]

    return sentences


# TODO (claudius): Do this while preserving original formatting
def _insert_translation(translated_sentences, original_text):
    return "\n".join(translated_sentences)


def _request_translate(sentences, source, target, preferred_langs):
    global request_id
    request_id += 1

    current_id = request_id

    url = "https://www.deepl.com/jsonrpc"
    headers = {}  # {'content-type': 'application/json'}

    payload = {
        "method": "LMT_handle_jobs",
        "params": {
            "jobs": [
                {
                    "raw_en_sentence": sentence
                } for sentence in sentences
            ],
            "lang": {
                "user_preferred_langs": preferred_langs,
            },
        },
        "jsonrpc": "2.0",
        "id": current_id,
    }

    if not source is None:
        payload["params"]["lang"]["source_lang_user_selected"] = source

    if not target is None:
        payload["params"]["lang"]["target_lang"] = target

    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    assert response["jsonrpc"]
    assert response["id"] == current_id

    return_ = {
        "translations": [
            # FIXME: Not very readable
            response["result"]["translations"][i]["beams"][0]["postprocessed_sentence"]
            if len(response["result"]["translations"][i]["beams"]) else ""
            for i in range(len(response["result"]["translations"]))
        ],
        "source": response["result"]["source_lang"],
        "target": response["result"]["target_lang"]
    }

    return return_
