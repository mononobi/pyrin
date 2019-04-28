# from datetime import datetime
#
# from bshop.core.api.deserializer.decorators import register_deserializer
# from bshop.core.api.deserializer.handlers.base import StringDeserializerBase
#
#
# @register_deserializer()
# class DateDeserializer(StringDeserializerBase):
#     """
#     date deserializer class.
#     """
#
#     def __init__(self, **options):
#         """
#         creates an instance of DateDeserializer.
#
#         :keyword list[tuple(str, int)] accepted_formats: a list of all accepted string formats
#                                                          and their length for date deserialization.
#
#         :type accepted_formats: list[tuple(str format, int length)]
#         """
#
#         StringDeserializerBase.__init__(self, **options)
#
#         self._accepted_formats = [('%Y-%m-%d', 10),
#                                   ('%Y/%m/%d', 10),
#                                   ('%Y.%m.%d', 10)]
#
#         accepted_formats = options.get('accepted_formats', [])
#         self._accepted_formats.extend(accepted_formats)
#
#     def deserialize(self, value, **options):
#         """
#         deserializes the given value.
#         returns None if deserialization fails.
#
#         :param str value: value to be deserialized.
#
#         :rtype: date
#         """
#
#         if not self.is_deserializable(value, **options):
#             return None
#
#         value = value.strip()
#         date_length = len(value)
#         converted_date = None
#
#         for format_string, length in self._accepted_formats:
#             if date_length != length:
#                 continue
#
#             try:
#                 converted_date = datetime.strptime(value, format_string)
#                 if converted_date is not None:
#                     break
#
#                 continue
#             except ValueError:
#                 continue
#
#         if converted_date is not None:
#             return converted_date.date()
#
#         return converted_date
