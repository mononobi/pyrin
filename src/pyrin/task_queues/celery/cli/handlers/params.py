# -*- coding: utf-8 -*-
"""
celery cli handlers params module.
"""

import pyrin.configuration.services as config_services

from pyrin.task_queues.celery.cli.interface import CeleryCLIParamBase
from pyrin.cli.arguments import KeywordArgument, BooleanArgument, \
    PositionalArgument, CompositeKeywordArgument, CompositePositionalArgument, \
    JSONKeywordArgument


class LogFileParam(KeywordArgument, CeleryCLIParamBase):
    """
    log file param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of LogFileParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('logfile', '--logfile', default=default)


class PIDFileParam(KeywordArgument, CeleryCLIParamBase):
    """
    pid file param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of PIDFileParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('pidfile', '--pidfile', default=default)


class LogLevelParam(KeywordArgument, CeleryCLIParamBase):
    """
    log level param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of LogLevelParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('loglevel', '--loglevel', default=default)


class WorkerLogFileParam(LogFileParam):
    """
    worker log file param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of WorkerLogFileParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to `worker_log_file` value
                               form `celery` config store if not provided.
        """

        if default is None:
            default = config_services.get_active('celery', 'worker_log_file')

        super().__init__(default=default)


class WorkerPIDFileParam(PIDFileParam):
    """
    worker pid file param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of WorkerPIDFileParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to `worker_pid_file` value
                               form `celery` config store if not provided.
        """

        if default is None:
            default = config_services.get_active('celery', 'worker_pid_file')

        super().__init__(default=default)


class WorkerLogLevelParam(LogLevelParam):
    """
    worker log level param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of WorkerLogLevelParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to `worker_log_level` value
                               form `celery` config store if not provided.
        """

        if default is None:
            default = config_services.get_active('celery', 'worker_log_level')

        super().__init__(default=default)


class ConcurrencyParam(KeywordArgument, CeleryCLIParamBase):
    """
    concurrency param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of ConcurrencyParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to `worker_concurrency` value
                               form `celery` config store if not provided.
        """

        if default is None:
            default = config_services.get_active('celery', 'worker_concurrency')

        super().__init__('concurrency', '--concurrency', default=default)


class HostnameParam(KeywordArgument, CeleryCLIParamBase):
    """
    hostname param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of HostnameParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to `worker_hostname` value
                               form `celery` config store if not provided.
        """

        if default is None:
            default = config_services.get_active('celery', 'worker_hostname')

        super().__init__('hostname', '--hostname', default=default)


class BeatParam(BooleanArgument, CeleryCLIParamBase):
    """
    beat param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of BeatParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('beat', '--beat', default=default)


class AutoScaleParam(CompositeKeywordArgument, CeleryCLIParamBase):
    """
    autoscale param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of AutoScaleParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to `worker_autoscale` value
                               form `celery` config store if not provided.
        """

        if default is None:
            default = config_services.get_active('celery', 'worker_autoscale')

        super().__init__('autoscale', '--autoscale', separator=',', default=default)


class QueuesParam(CompositeKeywordArgument, CeleryCLIParamBase):
    """
    queues param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of QueuesParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to `worker_queues` value
                               form `celery` config store if not provided.
        """

        super().__init__('queues', '--queues', separator=',', default=default)


class WorkerQueuesParam(QueuesParam):
    """
    worker queues param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of WorkerQueuesParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to `worker_queues` value
                               form `celery` config store if not provided.
        """

        if default is None:
            default = config_services.get_active('celery', 'worker_queues')

        super().__init__(default=default)


class PurgeParam(BooleanArgument, CeleryCLIParamBase):
    """
    purge param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of PurgeParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('purge', '--purge', default=default)


class OptimizationParam(KeywordArgument, CeleryCLIParamBase):
    """
    optimization param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of OptimizationParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to `worker_optimization` value
                               form `celery` config store if not provided.
        """

        if default is None:
            default = config_services.get_active('celery', 'worker_optimization')

        super().__init__('optimization', '-O', default=default)


class BeatLogFileParam(LogFileParam):
    """
    beat log file param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of BeatLogFileParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to `beat_log_file` value
                               form `celery` config store if not provided.
        """

        if default is None:
            default = config_services.get_active('celery', 'beat_log_file')

        super().__init__(default=default)


class BeatPIDFileParam(PIDFileParam):
    """
    beat pid file param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of BeatPIDFileParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to `beat_pid_file` value
                               form `celery` config store if not provided.
        """

        if default is None:
            default = config_services.get_active('celery', 'beat_pid_file')

        super().__init__(default=default)


class BeatLogLevelParam(LogLevelParam):
    """
    beat log level param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of BeatLogLevelParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to `beat_log_level` value
                               form `celery` config store if not provided.
        """

        if default is None:
            default = config_services.get_active('celery', 'beat_log_level')

        super().__init__(default=default)


class TaskIDParam(PositionalArgument, CeleryCLIParamBase):
    """
    task id param class.
    """

    def __init__(self, index=None, default=None, **options):
        """
        initializes an instance of TaskIDParam.

        :param int index: zero based index of this param in cli command inputs.
                          defaults to 0 if not provided.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.
        """

        if index is None:
            index = 0

        super().__init__('task_id', index, default=default, **options)


class TracebackParam(BooleanArgument, CeleryCLIParamBase):
    """
    traceback param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of TracebackParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('traceback', '--traceback', default=default)


class TaskNameParam(KeywordArgument, CeleryCLIParamBase):
    """
    task name param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of TaskNameParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('task', '--task', default=default)


class InspectMethodParam(PositionalArgument, CeleryCLIParamBase):
    """
    inspect method param class.
    """

    def __init__(self, index=None, default=None, **options):
        """
        initializes an instance of InspectMethodParam.

        :param int index: zero based index of this param in cli command inputs.
                          defaults to 0 if not provided.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.
        """

        if index is None:
            index = 0

        super().__init__('method', index, default=default, **options)


class TimeoutParam(KeywordArgument, CeleryCLIParamBase):
    """
    timeout param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of TimeoutParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('timeout', '--timeout', default=default)


class DestinationParam(CompositeKeywordArgument, CeleryCLIParamBase):
    """
    destination param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of DestinationParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('destination', '--destination',
                         separator=',', default=default)


class JSONParam(BooleanArgument, CeleryCLIParamBase):
    """
    json param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of JSONParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('json', '--json', default=default)


class IncludeDefaultsParam(PositionalArgument, CeleryCLIParamBase):
    """
    include defaults param class.
    """

    def __init__(self, index=None, default=None, **options):
        """
        initializes an instance of IncludeDefaultsParam.

        :param int index: zero based index of this param in cli command inputs.
                          defaults to 0 if not provided.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.
        """

        if index is None:
            index = 0

        super().__init__('include_defaults', index, default=default, **options)


class SamplesCountParam(PositionalArgument, CeleryCLIParamBase):
    """
    samples count param class.
    """

    def __init__(self, index=None, default=None, **options):
        """
        initializes an instance of SamplesCountParam.

        :param int index: zero based index of this param in cli command inputs.
                          defaults to 0 if not provided.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.
        """

        if index is None:
            index = 0

        super().__init__('samples_count', index, default=default, **options)


class ObjectTypeParam(PositionalArgument, CeleryCLIParamBase):
    """
    object type param class.
    """

    def __init__(self, index=None, default=None, **options):
        """
        initializes an instance of ObjectTypeParam.

        :param int index: zero based index of this param in cli command inputs.
                          defaults to 0 if not provided.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.
        """

        if index is None:
            index = 0

        super().__init__('object_type', index, default=default, **options)


class CountParam(PositionalArgument, CeleryCLIParamBase):
    """
    count param class.
    """

    def __init__(self, index=None, default=None, **options):
        """
        initializes an instance of CountParam.

        :param int index: zero based index of this param in cli command inputs.
                          defaults to 0 if not provided.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.
        """

        if index is None:
            index = 0

        super().__init__('count', index, default=default, **options)


class MaxDepthParam(PositionalArgument, CeleryCLIParamBase):
    """
    max depth param class.
    """

    def __init__(self, index=None, default=None, **options):
        """
        initializes an instance of MaxDepthParam.

        :param int index: zero based index of this param in cli command inputs.
                          defaults to 0 if not provided.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.
        """

        if index is None:
            index = 0

        super().__init__('max_depth', index, default=default, **options)


class TaskIDListParam(CompositePositionalArgument, CeleryCLIParamBase):
    """
    task id list param class.
    """

    def __init__(self, index=None, default=None, **options):
        """
        initializes an instance of TaskIDListParam.

        :param int index: zero based index of this param in cli command inputs.
                          defaults to 0 if not provided.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.
        """

        if index is None:
            index = 0

        super().__init__('task_ids', index, default=default,
                         separator=' ', **options)


class AttributeListParam(CompositePositionalArgument, CeleryCLIParamBase):
    """
    attribute list param class.
    """

    def __init__(self, index=None, default=None, **options):
        """
        initializes an instance of AttributeListParam.

        :param int index: zero based index of this param in cli command inputs.
                          defaults to 0 if not provided.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.
        """

        if index is None:
            index = 0

        super().__init__('attributes', index, default=default,
                         separator=' ', **options)


class TaskNamePositionalParam(PositionalArgument, CeleryCLIParamBase):
    """
    task name positional param class.
    """

    def __init__(self, index=None, default=None, **options):
        """
        initializes an instance of TaskNamePositionalParam.

        :param int index: zero based index of this param in cli command inputs.
                          defaults to 0 if not provided.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.
        """

        if index is None:
            index = 0

        super().__init__('task', index, default=default, **options)


class ArgsParam(JSONKeywordArgument, CeleryCLIParamBase):
    """
    args param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of ArgsParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('args', '--args', default=default)


class KwargsParam(JSONKeywordArgument, CeleryCLIParamBase):
    """
    kwargs param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of KwargsParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('kwargs', '--kwargs', default=default)


class ETAParam(KeywordArgument, CeleryCLIParamBase):
    """
    eta param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of ETAParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('eta', '--eta', default=default)


class CountdownParam(KeywordArgument, CeleryCLIParamBase):
    """
    countdown param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of CountdownParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('countdown', '--countdown', default=default)


class ExpiresParam(KeywordArgument, CeleryCLIParamBase):
    """
    expires param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of ExpiresParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('expires', '--expires', default=default)


class SerializerParam(KeywordArgument, CeleryCLIParamBase):
    """
    serializer param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of SerializerParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('serializer', '--serializer', default=default)


class QueueParam(KeywordArgument, CeleryCLIParamBase):
    """
    queue param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of QueueParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('queue', '--queue', default=default)


class ExchangeParam(KeywordArgument, CeleryCLIParamBase):
    """
    exchange param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of ExchangeParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('exchange', '--exchange', default=default)


class RoutingKeyParam(KeywordArgument, CeleryCLIParamBase):
    """
    routing key param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of RoutingKeyParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('routing_key', '--routing-key', default=default)


class ControlMethodParam(PositionalArgument, CeleryCLIParamBase):
    """
    control method param class.
    """

    def __init__(self, index=None, default=None, **options):
        """
        initializes an instance of ControlMethodParam.

        :param int index: zero based index of this param in cli command inputs.
                          defaults to 0 if not provided.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.
        """

        if index is None:
            index = 0

        super().__init__('method', index, default=default, **options)


class QueuePositionalParam(PositionalArgument, CeleryCLIParamBase):
    """
    queue positional param class.
    """

    def __init__(self, index=None, default=None, **options):
        """
        initializes an instance of QueuePositionalParam.

        :param int index: zero based index of this param in cli command inputs.
                          defaults to 0 if not provided.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.
        """

        if index is None:
            index = 0

        super().__init__('queue', index, default=default, **options)


class ExchangePositionalParam(PositionalArgument, CeleryCLIParamBase):
    """
    exchange positional param class.
    """

    def __init__(self, index=None, default=None, **options):
        """
        initializes an instance of ExchangePositionalParam.

        :param int index: zero based index of this param in cli command inputs.
                          defaults to 0 if not provided.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.
        """

        if index is None:
            index = 0

        super().__init__('exchange', index, default=default, **options)


class ExchangeTypePositionalParam(PositionalArgument, CeleryCLIParamBase):
    """
    exchange type positional param class.
    """

    def __init__(self, index=None, default=None, **options):
        """
        initializes an instance of ExchangeTypePositionalParam.

        :param int index: zero based index of this param in cli command inputs.
                          defaults to 0 if not provided.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.
        """

        if index is None:
            index = 0

        super().__init__('type', index, default=default, **options)


class RoutingKeyPositionalParam(PositionalArgument, CeleryCLIParamBase):
    """
    routing key positional param class.
    """

    def __init__(self, index=None, default=None, **options):
        """
        initializes an instance of RoutingKeyPositionalParam.

        :param int index: zero based index of this param in cli command inputs.
                          defaults to 0 if not provided.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.
        """

        if index is None:
            index = 0

        super().__init__('routing_key', index, default=default, **options)


class MaxScaleParam(PositionalArgument, CeleryCLIParamBase):
    """
    max scale param class.
    """

    def __init__(self, index=None, default=None, **options):
        """
        initializes an instance of MaxScaleParam.

        :param int index: zero based index of this param in cli command inputs.
                          defaults to 0 if not provided.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.
        """

        if index is None:
            index = 0

        super().__init__('max_scale', index, default=default, **options)


class MinScaleParam(PositionalArgument, CeleryCLIParamBase):
    """
    min scale param class.
    """

    def __init__(self, index=None, default=None, **options):
        """
        initializes an instance of MinScaleParam.

        :param int index: zero based index of this param in cli command inputs.
                          defaults to 0 if not provided.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.
        """

        if index is None:
            index = 0

        super().__init__('min_scale', index, default=default, **options)


class PoolResizeParam(PositionalArgument, CeleryCLIParamBase):
    """
    pool resize param class.
    """

    def __init__(self, index=None, default=None, **options):
        """
        initializes an instance of PoolResizeParam.

        :param int index: zero based index of this param in cli command inputs.
                          defaults to 0 if not provided.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.
        """

        if index is None:
            index = 0

        super().__init__('resize', index, default=default, **options)


class RateLimitParam(PositionalArgument, CeleryCLIParamBase):
    """
    rate limit param class.
    """

    def __init__(self, index=None, default=None, **options):
        """
        initializes an instance of RateLimitParam.

        :param int index: zero based index of this param in cli command inputs.
                          defaults to 0 if not provided.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.
        """

        if index is None:
            index = 0

        super().__init__('rate_limit', index, default=default, **options)


class SignalParam(PositionalArgument, CeleryCLIParamBase):
    """
    signal param class.
    """

    def __init__(self, index=None, default=None, **options):
        """
        initializes an instance of SignalParam.

        :param int index: zero based index of this param in cli command inputs.
                          defaults to 0 if not provided.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.
        """

        if index is None:
            index = 0

        super().__init__('signal', index, default=default, **options)


class SoftSecondsParam(PositionalArgument, CeleryCLIParamBase):
    """
    soft seconds param class.
    """

    def __init__(self, index=None, default=None, **options):
        """
        initializes an instance of SoftSecondsParam.

        :param int index: zero based index of this param in cli command inputs.
                          defaults to 0 if not provided.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.
        """

        if index is None:
            index = 0

        super().__init__('soft_secs', index, default=default, **options)


class HardSecondsParam(PositionalArgument, CeleryCLIParamBase):
    """
    hard seconds param class.
    """

    def __init__(self, index=None, default=None, **options):
        """
        initializes an instance of HardSecondsParam.

        :param int index: zero based index of this param in cli command inputs.
                          defaults to 0 if not provided.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.
        """

        if index is None:
            index = 0

        super().__init__('hard_secs', index, default=default, **options)


class CameraParam(KeywordArgument, CeleryCLIParamBase):
    """
    camera param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of CameraParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('camera', '--camera', default=default)


class FrequencyParam(KeywordArgument, CeleryCLIParamBase):
    """
    frequency param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of FrequencyParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('frequency', '--frequency', default=default)


class DumpParam(BooleanArgument, CeleryCLIParamBase):
    """
    dump param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of DumpParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('dump', '--dump', default=default)


class MaxRateParam(KeywordArgument, CeleryCLIParamBase):
    """
    max rate param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of MaxRateParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('maxrate', '--maxrate', default=default)


class IPythonParam(BooleanArgument, CeleryCLIParamBase):
    """
    ipython param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of IPythonParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('ipython', '--ipython', default=default)


class BPythonParam(BooleanArgument, CeleryCLIParamBase):
    """
    bpython param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of BPythonParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('bpython', '--bpython', default=default)


class PythonParam(BooleanArgument, CeleryCLIParamBase):
    """
    python param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of PythonParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('python', '--python', default=default)


class WithoutTasksParam(BooleanArgument, CeleryCLIParamBase):
    """
    without tasks param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of WithoutTasksParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('without_tasks', '--without-tasks', default=default)


class EventletParam(BooleanArgument, CeleryCLIParamBase):
    """
    eventlet param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of EventletParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('eventlet', '--eventlet', default=default)


class GeventParam(BooleanArgument, CeleryCLIParamBase):
    """
    gevent param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of GeventParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('gevent', '--gevent', default=default)


class TopicParam(PositionalArgument, CeleryCLIParamBase):
    """
    topic param class.
    """

    def __init__(self, index=None, default=None, **options):
        """
        initializes an instance of TopicParam.

        :param int index: zero based index of this param in cli command inputs.
                          defaults to 0 if not provided.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.
        """

        if index is None:
            index = 0

        super().__init__('topic', index, default=default, **options)


class ForceParam(BooleanArgument, CeleryCLIParamBase):
    """
    force param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of ForceParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
        """

        super().__init__('force', '--force', default=default)


class ExcludeQueuesParam(CompositeKeywordArgument, CeleryCLIParamBase):
    """
    exclude queues param class.
    """

    def __init__(self, default=None):
        """
        initializes an instance of ExcludeQueuesParam.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to `worker_queues` value
                               form `celery` config store if not provided.
        """

        super().__init__('exclude_queues', '--exclude-queues',
                         separator=',', default=default)


class ActionParam(PositionalArgument, CeleryCLIParamBase):
    """
    action param class.
    """

    def __init__(self, index=None, default=None, **options):
        """
        initializes an instance of ActionParam.

        :param int index: zero based index of this param in cli command inputs.
                          defaults to 0 if not provided.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.
        """

        if index is None:
            index = 0

        super().__init__('action', index, default=default, **options)


class FilesParam(PositionalArgument, CeleryCLIParamBase):
    """
    files param class.
    """

    def __init__(self, index=None, default=None, **options):
        """
        initializes an instance of FilesParam.

        :param int index: zero based index of this param in cli command inputs.
                          defaults to 0 if not provided.

        :param object default: default value to be emitted to
                               cli if this param is not available.
                               if set to None, this param will not
                               be emitted at all.
                               defaults to None if not provided.

        :keyword bool validate_index: specifies that index of this argument
                                      must be validated. it could be helpful
                                      to set this to False when there are multiple
                                      arguments with the same index that will appear
                                      in different situations.
                                      defaults to True if not provided.
        """

        if index is None:
            index = 0

        super().__init__('files', index, default=default, **options)
