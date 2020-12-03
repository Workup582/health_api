ENDPOINTS_TRANSLATOR = {
    'to': {
        'diagnosis': 'engdiag',
        'test': 'testdiag'
    },

    'from': {
        'engdiag': 'diagnosis',
        'testdiag': 'test'
    }
}

PREFIX_TRANSLATOR = {
    'to': {
        's': 'symptom',
        'p': 'patient',
        'c': 'condition',
        'lt': 'labtest'
    },

    'from': {
        'symptom': 's',
        'patient': 'p',
        'condition': 'c',
        'labtest': 'lt'
    }
}

POSTFIX_TRANSLATOR = {
    'to': str.maketrans(
        '123456789',
        'abcdefghi'
    ),

    'from': str.maketrans(
        'abcdefghi',
        '123456789'
    )
}


def translate_parameter(param, direction='from'):
    try:
        parts = param.split('_')
        prefix = parts[0]
        postfix = parts[1]

        prefix = PREFIX_TRANSLATOR[direction][prefix]
        postfix = str.translate(postfix, POSTFIX_TRANSLATOR[direction])

        parts[0] = prefix
        parts[1] = postfix

        return '_'.join(parts)
    except Exception as ex:
        print(f'info: untranslatable parameter {param}:', ex)
        return None


def translate_list_with_ids(entries_with_id, direction='from'):
    for entry in entries_with_id:
        try:
            new_id = translate_parameter(entry['id'], direction)

            if not new_id:
                raise ValueError('Unable to translate ID')

            for key, value in entry.items():
                if key == 'id':
                    entry['id'] = new_id
                else:
                    entry[key] = value
        except Exception as ex:
            print('info: unable to translate entry', entry, ex)


def translate_query_string(params_dict, direction='from'):
    if not params_dict:
        return {}

    new_params = {}

    for key, values in params_dict.items():
        try:
            new_key = translate_parameter(key, direction)

            if not new_key:
                raise ValueError()

            new_params[new_key] = values
        except Exception:
            # print('warn: unable to translate key', key)
            new_params[key] = values

    return new_params


def translate_url(url, direction='from'):
    try:
        parts = url.split('/')

        for index, part in enumerate(parts):
            parts[index] = ENDPOINTS_TRANSLATOR[direction][part]

        return '/'.join(parts)
    except Exception:
        pass

    return url


def intelligent_response_converter(obj, direction='from'):
    def deref_multi(data, keys):
        try:
            return deref_multi(data[keys[0]], keys[1:]) if keys else data
        except Exception:
            return None

    # last = deref_multi(exp, ['path','to','key'])

    known_pathes = [
        ['supporting_evidence'],
        ['question', 'items'],
        ['conditions'],
        ['serious'],
        ['mentions'],
        ['children'],
        ['results']
    ]

    if isinstance(obj, list):
        try:
            # obj = translate_list_with_ids(obj, direction)

            for entry in obj:
                intelligent_response_converter(entry, direction)

            print('|', obj)
        except Exception:
            pass
    elif isinstance(obj, object):
        if obj.get('id'):
            translate_list_with_ids([obj], direction)

        for known_path in known_pathes:
            entry = deref_multi(obj, known_path)

            if entry:
                intelligent_response_converter(entry, direction)

    return obj
