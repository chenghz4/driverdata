from sys import stderr

from tastypie.validation import Validation

from dds.models import Query, QueryFilter, CensusField


def uri_to_pk(uri):
    """
    Returns the integer PK part of a URI.

    Assumes ``/api/v1/resource/123/`` format. If conversion fails, this just
    returns the URI unmodified.

    Also handles lists of URIs
    """

    if uri is None:
        return None

    # convert everything to lists
    multiple = not isinstance(uri, basestring)
    uris = uri if multiple else [uri]

    # handle all passed URIs
    converted = []
    for one_uri in uris:
        try:
            # hopefully /api/v1/<resource_name>/<pk>/
            converted.append(int(one_uri.split('/')[-2]))
        except (IndexError, ValueError):
            raise ValueError(
                "URI %s could not be converted to PK integer." % one_uri)

    # convert back to original format
    return converted if multiple else converted[0]


class QueryFilterValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'Missing data.'}
        query = Query.objects.filter(pk=uri_to_pk(bundle.data['query']))
        field = CensusField.objects.filter(pk=uri_to_pk(bundle.data['field']))
        if query.count() == 0:
            return {'query': 'Unknown query.'}
        if field.count() == 0:
            return {'field': 'Unknown field.'}
        query = query[0]
        field = field[0]
        for qf in query.queryfilter_set.iterator():
            if field == qf.field:
                return {'field': 'Duplicate field for query'}
        return {}