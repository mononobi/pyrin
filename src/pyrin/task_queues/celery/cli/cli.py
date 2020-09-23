# -*- coding: utf-8 -*-
"""
celery cli module.
"""

import pyrin.task_queues.celery.cli.services as celery_cli_services

from pyrin.cli.decorators import cli, cli_group
from pyrin.core.structs import CLI


@cli_group('celery')
class CeleryCLI(CLI):
    """
    celery cli class.

    this class exposes all celery cli commands.
    """

    _execute_service = celery_cli_services.execute

    @cli
    def worker(self, **options):
        """
        create a worker node.

        :keyword int concurrency: number of child processes processing the queue.
                                  the default is the number of cpus available on
                                  your system.

        :keyword str hostname: set custom hostname for worker node.

        :keyword bool beat: also run the `celery beat` periodic task scheduler.
                            please note that there must only be one instance of
                            this service.

        :keyword str | list[str] queues: list of queues to enable for this worker.
        :keyword bool purge: purges all waiting tasks before the daemon is started.

        :keyword str autoscale: enable autoscaling by providing
                                max_concurrency, min_concurrency.

        :keyword str logfile: path to log file. if no logfile is specified, `stderr` is used.

        :keyword str loglevel: logging level, choose between `DEBUG`, `INFO`, `WARNING`,
                               `ERROR`, `CRITICAL` or `FATAL`.

        :keyword str pidfile: optional file used to store the process pid.
                              the program won't start if this file already exists
                              and the pid is still alive.

        :keyword str optimization: optimization profile to be applied.
                                   it could be from: `default` and `fair`.

        :keyword bool help: show help for this command.
        """
        pass

    @cli
    def beat(self, **options):
        """
        start the beat periodic task scheduler.

        :keyword str logfile: path to log file. if no logfile is specified, `stderr` is used.

        :keyword str loglevel: logging level, choose between `DEBUG`, `INFO`, `WARNING`,
                               `ERROR`, `CRITICAL` or `FATAL`.

        :keyword str pidfile: optional file used to store the process pid.
                              the program won't start if this file already exists
                              and the pid is still alive.

        :keyword bool help: show help for this command.
        """
        pass

    @cli
    def result(self, task_id, **options):
        """
        gives the return value for a given task id.

        :param str task_id: id of the task.

        :keyword str task: name of the task (if custom backend).
        :keyword bool traceback: show traceback if any.
        :keyword bool help: show help for this command.
        """
        pass

    @cli
    def inspect(self, method, **options):
        """
        inspect the worker at runtime.

        :param str method: inspect method. it could be from these methods:
                           `active`, `active_queues`, `clock`, `conf`, `memdump`,
                           `memsample`, `objgraph`, `ping`, `query_task`, `registered`,
                           `report`, `reserved`, `revoked`, `scheduled` and `stats`.

        :keyword bool include_defaults: this is only for `conf` method.
        :keyword int samples_count: this is only for `memdump` method.
        :keyword str object_type: this is only for `objgraph` method.
        :keyword int count: this is only for `objgraph` method.
        :keyword int max_depth: this is only for `objgraph` method.
        :keyword str | list[str] task_ids: list of task ids.
                                           this is only for `query_task` method.

        :keyword str | list[str] attributes: this is only for `registered` method.
        :keyword str | list[str] destination: list of destination node names.
        :keyword float timeout: timeout in seconds waiting for reply.
        :keyword bool json: use json as output format.
        :keyword bool help: show help for this command.
        """
        pass

    @cli
    def amqp(self, **options):
        """
        amqp administration shell.

        also works for non-amqp transports (but not ones that
        store declarations in memory).

        :keyword bool help: show help for this command.
        """
        pass

    @cli
    def call(self, task, **options):
        """
        call a task by name.

        :param str task: task name.

        :keyword list args: task positional arguments.
        :keyword dict kwargs: task keyword arguments.
        :keyword str eta: scheduled time in `iso-8601` format.
        :keyword float | int countdown: eta in seconds from now.
        :keyword float | int | str expires: expiry time in seconds or an `iso-8601` date.
        :keyword str serializer: specify serializer to use (default is json).
        :keyword str queue: destination queue name.
        :keyword str exchange: destination exchange name (defaults to the queue exchange).
        :keyword str routing_key: destination routing key (defaults to the queue routing key).

        :keyword bool help: show help for this command.
        """
        pass

    @cli
    def control(self, method, **options):
        """
        workers remote control.

        :param str method: control method. it could be from these methods:
                           `add_consumer`, `autoscale`, `cancel_consumer`,
                           `disable_events`, `election`, `enable_events`,
                           `heartbeat`, `pool_grow`, `pool_restart`,
                           `pool_shrink`, `rate_limit`, `revoke`, `shutdown`,
                           `terminate` and `time_limit`.

        :keyword str queue: the queue name.
                            this is only for `add_consumer`
                            and `cancel_consumer` methods.

        :keyword str exchange: exchange name.
                               this is only for `add_consumer` method.

        :keyword str type: exchange type.
                           this is only for `add_consumer` method.

        :keyword str routing_key: routing key.
                                  this is only for `add_consumer` method.

        :keyword int max_scale: max value for autoscaling.
                                this is only for `autoscale` method.

        :keyword int min_scale: min value for autoscaling.
                                this is only for `autoscale` method.

        :keyword int resize: pool grow or shrink resize value.
                             this is only for `pool_grow` and `pool_shrink` methods.

        :keyword str task: task name.
                           this is only for `rate_limit` and `time_limit` methods.

        :keyword str rate_limit: rate limit value.
                                 for example: 5/s, 5/m or 5/h.
                                 this is only for `rate_limit` method.

        :keyword str | list[str] task_ids: list of task ids.
                                           this is only for `revoke`
                                           and `terminate` methods.

        :keyword str signal: signal name to use for stopping tasks.
                             this is only for `terminate` method.

        :keyword int | float soft_secs: soft time limit for task.
                                        this is only for `time_limit` method.

        :keyword int | float hard_secs: hard time limit for task.
                                        this is only for `time_limit` method.

        :keyword str | list[str] destination: list of destination node names.
        :keyword float timeout: timeout in seconds waiting for reply.
        :keyword bool json: use json as output format.
        :keyword bool help: show help for this command.
        """
        pass

    @cli
    def events(self, **options):
        """
        event-stream utilities.

        :keyword str camera: camera class fully qualified name.
        :keyword float | int frequency: frequency value.
        :keyword bool dump: dump events to stdout.
        :keyword str maxrate: max event streaming rate.
        :keyword bool help: show help for this command.
        """
        pass

    @cli
    def shell(self, **options):
        """
        start shell session with convenient access to celery symbols.

        :keyword bool python: force default python shell.
        :keyword bool ipython: force `ipython` implementation.
        :keyword bool bpython: force `bpython` implementation.
        :keyword bool without_tasks: don't add tasks to locals.
        :keyword bool eventlet: use `eventlet` monkey patches.
        :keyword bool gevent: use `gevent` monkey patches.
        :keyword bool help: show help for this command.
        """
        pass

    @cli
    def list(self, topic, **options):
        """
        get info from broker.

        :param str topic: topic to get info about.
                          for example: `bindings`.

        :keyword bool help: show help for this command.
        """
        pass

    @cli
    def purge(self, **options):
        """
        erase all messages from all known task queues.

        :keyword bool force: don't prompt for verification before deleting messages.
        :keyword str | list[str] queues: list of queue names to purge.
        :keyword str | list[str] exclude_queues: list of queue names not to purge.
        :keyword bool help: show help for this command.
        """
        pass

    @cli
    def logtool(self, action, **options):
        """
        the celery logtool command.

        :param str action: action to be executed. it could be from:
                           `stats`, `traces`, `errors`, `incomplete` and `debug`.

        :keyword str | list[str] files: list of file paths.
        :keyword bool help: show help for this command.
        """
        pass

    @cli
    def status(self, **options):
        """
        show list of worker nodes that are online.

        :keyword bool help: show help for this command.
        """
        pass

    @cli
    def report(self, **options):
        """
        shows information useful to include in bug-reports.

        :keyword bool help: show help for this command.
        """
        pass

    @cli
    def help(self):
        """
        show celery command line help.
        """
        pass
