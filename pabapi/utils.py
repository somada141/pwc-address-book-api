# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import codecs
import chardet


def recode(
    string_encoded,
    decoding_hint="utf-8",
    decoding_fallback="utf-8",
    encoding_target="utf-8",
    error_handling="ignore"
):
    """Decodes a string with an arbitrary encoding"""

    # Check if the string is a unicode string and try to encode it into the
    # target encoding.
    if isinstance(string_encoded, unicode):
        try:
            filename_recoded = codecs.encode(
                obj=string_encoded,
                encoding=encoding_target,
                errors=error_handling
            )
            return filename_recoded
        except:
            pass

    # First, try decoding with the 'decoding_hint', if one was provided. If the
    # operation is successful then return the results.
    if decoding_hint is not None:
        try:
            string_decoded = codecs.decode(
                obj=string_encoded,
                encoding=decoding_hint,
                errors=error_handling
            )
            string_recoded = codecs.encode(
                obj=string_decoded,
                encoding=encoding_target,
                errors=error_handling
            )
            return string_recoded
        except:
            pass

    # Second, try to detect the encoding using 'chardet' and attempt to decode
    # the string using the 'guessed' encoding. Return if successful.
    encoding_original = chardet.detect(string_encoded)["encoding"]
    try:
        string_decoded = codecs.decode(
            obj=string_encoded,
            encoding=encoding_original,
            errors=error_handling
        )
        string_recoded = codecs.encode(
            obj=string_decoded,
            encoding=encoding_target,
            errors=error_handling
        )
        return string_recoded
    except:
        pass

    # Third, try to use the 'decoding_fallback' as a last resort. Should this
    # one fail as well then raise an exception.
    try:
        string_decoded = codecs.decode(
            obj=string_encoded,
            encoding=decoding_fallback,
            errors=error_handling
        )
        string_recoded = codecs.encode(
            obj=string_decoded,
            encoding=encoding_target,
            errors=error_handling
        )

        return string_recoded
    except Exception as exc:
        raise exc
