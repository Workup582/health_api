from traversy import traverse
from dotty_dict import dotty
from copy import deepcopy
import requests

from chalicelib.fam import config

TRASLATEABLE_NODES = ['name', 'text', 'label']


def translate_terms(source_text, to_language, from_language=None):
    url = f'https://translation.googleapis.com/language/translate/v2?key={config.GOOGLE_TRANSLATE_API_KEY}'

    body = {
        'target': to_language,
        'format': "text",
        'q': source_text
    }

    if from_language:
        body['source'] = from_language

    response = requests.post(url, json=body, headers={
                             'Content-Type': 'application/json'})

    return response.json()


def translate_obj(obj, to_language):
    obj = dotty(deepcopy(obj))

    try:
        translations = {}

        for node in traverse(obj):
            key = node['key']
            parent_node = node['parent_node']
            path_str = node['path_str']

            if key in TRASLATEABLE_NODES:
                translations[path_str] = node['value']

        translate_keys = list(translations.keys())
        translate_values = list(translations.values())

        translated = translate_terms(translate_values, to_language, 'en')

        print('Translated terms:', translated)

        translated_values = [x['translatedText'].capitalize()
                             for x in translated['data']['translations']]

        translations = dict(zip(translate_keys, translated_values))

        for key, value in translations.items():
            obj[key] = value
    except Exception as ex:
        print('Exception during translation:', ex)

    return obj.to_dict()


def get_language(req):
    known_language = ['ab', 'aa', 'af', 'sq', 'am', 'ar', 'hy', 'as', 'ay', 'az', 'ba', 'eu', 'bn', 'dz', 'bh', 'bi',
                      'br', 'bg', 'my', 'be', 'km', 'ca', 'zh', 'co', 'hr', 'cs', 'da', 'nl', 'en', 'eo', 'et', 'fo',
                      'fj', 'fi', 'fr', 'fy', 'gd', 'gl', 'ka', 'de', 'el', 'kl', 'gn', 'gu', 'ha', 'iw', 'hi', 'hu',
                      'is', 'in', 'ia', 'ie', 'ik', 'ga', 'it', 'ja', 'jw', 'kn', 'ks', 'kk', 'rw', 'ky', 'rn', 'ko',
                      'ku', 'lo', 'la', 'lv', 'ln', 'lt', 'mk', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mo', 'mn', 'na',
                      'ne', 'no', 'oc', 'or', 'om', 'ps', 'fa', 'pl', 'pt', 'pa', 'qu', 'rm', 'ro', 'ru', 'sm', 'sg',
                      'sa', 'sr', 'sh', 'st', 'tn', 'sn', 'sd', 'si', 'ss', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv',
                      'tl', 'tg', 'ta', 'tt', 'te', 'th', 'bo', 'ti', 'to', 'ts', 'tr', 'tk', 'tw', 'uk', 'ur', 'uz',
                      'vi', 'vo', 'cy', 'wo', 'xh', 'ji', 'yo', 'zu']
    language = None

    try:
        language = req.json_body['language'].lower()
    except:
        pass

    if not language:
        try:
            language = req.query_params['language'].lower()
        except:
            pass

    if not language or language not in known_language:
        language = 'en'

    return language


if __name__ == '__main__':
    # {
    #     "sex": "male",
    #     "age": 33,
    #     "evidence": [
    #         {
    #             "id": "symptom_dg",
    #             "choice_id": "present",
    #             "source": "initial"
    #         },
    #         {
    #             "id": "symptom_bb",
    #             "choice_id": "present"
    #         },
    #         {
    #             "id": "patient_ha",
    #             "choice_id": "present"
    #         }
    #     ]
    # }

    resp = {
        "question": {
            "type": "group_single",
            "text": "How strong is your headache?",
            "items": [
                {
                    "id": "symptom_agh0",
                    "name": "Mild",
                    "choices": [
                        {
                            "id": "present",
                            "label": "Yes"
                        },
                        {
                            "id": "absent",
                            "label": "No"
                        },
                        {
                            "id": "unknown",
                            "label": "Don't know"
                        }
                    ]
                },
                {
                    "id": "symptom_agha",
                    "name": "Moderate",
                    "choices": [
                        {
                            "id": "present",
                            "label": "Yes"
                        },
                        {
                            "id": "absent",
                            "label": "No"
                        },
                        {
                            "id": "unknown",
                            "label": "Don't know"
                        }
                    ]
                },
                {
                    "id": "symptom_aaic",
                    "name": "Severe",
                    "choices": [
                        {
                            "id": "present",
                            "label": "Yes"
                        },
                        {
                            "id": "absent",
                            "label": "No"
                        },
                        {
                            "id": "unknown",
                            "label": "Don't know"
                        }
                    ]
                }
            ],
            "extras": {}
        },
        "conditions": [
            {
                "id": "condition_fhh",
                "name": "Ear barotrauma",
                "common_name": "Ear barotrauma",
                "probability": 0.1341
            },
            {
                "id": "condition_ac0",
                "name": "Acute otitis media",
                "common_name": "Middle ear infection",
                "probability": 0.0855
            },
            {
                "id": "condition_di",
                "name": "Migraine",
                "common_name": "Migraine",
                "probability": 0.0489
            },
            {
                "id": "condition_ige",
                "name": "Cervical strain",
                "common_name": "Neck strain",
                "probability": 0.0452
            },
            {
                "id": "condition_ee",
                "name": "Tension-type headaches",
                "common_name": "Stress headache",
                "probability": 0.0355
            },
            {
                "id": "condition_aca",
                "name": "Otitis externa",
                "common_name": "Inflammation of the external ear",
                "probability": 0.0293
            }
        ],
        "extras": {},
        "should_stop": False
    }

    res = translate_obj(resp, 'ru')
    print(res)
