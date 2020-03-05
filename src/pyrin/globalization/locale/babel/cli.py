# -*- coding: utf-8 -*-
"""
babel cli module.
"""

import pyrin.globalization.locale.babel.services as babel_services

from pyrin.cli.decorators import cli
from pyrin.core.context import CLI


class BabelCLI(CLI):
    """
    babel cli class.
    this class exposes all babel cli commands.
    """

    _execute_service = babel_services.execute

    @cli
    def init(self, locale, width=None, no_wrap=False, help=False):
        """
        create new message catalogs from a `.pot` file.

        :param str locale: locale name for the new localized catalog.
                           for example: `en` or `fr` or ...

        :keyword int width: set output line width.
                            defaults to 76 if not provided.

        :keyword bool no_wrap: do not break long message lines, longer
                               than the output line width, into several lines.
                               defaults to False in not provided.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """
        pass

    @cli
    def update(self, locale=None, omit_header=False, width=None,
               no_wrap=False, ignore_obsolete=False, no_fuzzy_matching=False,
               update_header_comment=False, previous=False, help=False):
        """
        update existing message catalogs from a `.pot` file.

        :keyword str locale: locale name of the catalog to compile.
                             it will compile all catalogs if not provided.

        :keyword bool omit_header: do not include msgid entry in header.
                                   defaults to False if not provided.

        :keyword int width: set output line width.
                            defaults to 76 if not provided.

        :keyword bool no_wrap: do not break long message lines, longer
                               than the output line width, into several lines.
                               defaults to False in not provided.

        :keyword bool ignore_obsolete: whether to omit obsolete messages from
                                       the output. defaults to False if not provided.

        :keyword bool no_fuzzy_matching: do not use fuzzy matching.
                                         defaults to False if not provided.

        :keyword bool update_header_comment: update target header comment.
                                             defaults to False if not provided.

        :keyword bool previous: keep previous msgids of translated messages.
                                defaults to False if not provided.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """
        pass

    @cli
    def extract(self, include_pyrin=True, include_app=True, charset=None,
                keywords=None, no_default_keywords=False, no_location=False,
                add_location=None, omit_header=False, width=None, no_wrap=False,
                sort_output=False, sort_by_file=False, msgid_bugs_address=None,
                copyright_holder=None, project=None, version=None, add_comments=None,
                strip_comments=False, help=False):
        """
        extract messages from source files and generate a `.pot` file.

        :keyword bool include_pyrin: specifies that it must extract pyrin localizable
                                     messages as well. defaults to True if not provided.

        :keyword bool include_app: specifies that it must extract application localizable
                                   messages as well. defaults to True if not provided.

        :note include: at least of `include_pyrin` or `include_app` must be True.

        :keyword str charset: charset to use in the output file.
                              defaults to `utf-8` if not provided.

        :keyword Union[str, list[str]] keywords: single keyword or list of keywords
                                                 to look for in addition to the defaults.
                                                 it may be repeated multiple times.

        :keyword bool no_default_keywords: do not include the default keywords.
                                           defaults to False if not provided.

        :keyword bool no_location: do not include location comments
                                   with filename and line number.
                                   defaults to False if not provided.

        :keyword str add_location: location lines format. if it is not given or `full`,
                                   it generates the lines with both file name and line
                                   number. if it is `file`, the line number part is
                                   omitted. if it is `never`, it completely suppresses
                                   the lines, same as `no_location=True`.
                                   default to None if not provided.

        :keyword bool omit_header: do not include msgid entry in header.
                                   defaults to False if not provided.

        :keyword int width: set output line width.
                            defaults to 76 if not provided.

        :keyword bool no_wrap: do not break long message lines, longer
                               than the output line width, into several lines.
                               defaults to False in not provided.

        :keyword bool sort_output: generate sorted output.
                                   defaults to False if not provided.

        :keyword bool sort_by_file: sort output by file location.
                                    defaults to False if not provided.

        :keyword str msgid_bugs_address: set report address for msgid.
                                         defaults to None if not provided.

        :keyword str copyright_holder: set copyright holder in output.
                                       defaults to None if not provided.

        :keyword str project: set project name in output.
                              defaults to None if not provided.

        :keyword str version: set project version in output.
                              defaults to None if not provided.

        :keyword Union[str, list[str]] add_comments: place comment block with tag or
                                                     those preceding keyword lines in
                                                     output file. it could be a single
                                                     value or a list of values.
                                                     defaults to None if not provided.

        :keyword bool strip_comments: strip the comment tags from the comments.
                                      defaults to False if not provided.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """
        pass

    @cli
    def compile(self, locale=None, use_fuzzy=False,
                statistics=False, help=False):
        """
        compile message catalogs to `.mo` files.

        :keyword str locale: locale name of the catalog to compile.
                             it will compile all catalogs if not provided.

        :keyword bool use_fuzzy: also include fuzzy translations.
                                 defaults to False if not provided.

        :keyword bool statistics: print statistics about translations.
                                  defaults to False if not provided.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """
        pass

    def rebuild(self, include_pyrin=True,
                include_app=True, locale=None,
                help=False):
        """
        it will do the three complete steps needed to update
        and compile locales with new messages.

        it will do:
            1. extract
            2. update
            3. compile

        this command is defined for convenient of usage, but if you need
        to do these steps separately, you could ignore this command and
        use the relevant command for each step.

        :keyword bool include_pyrin: specifies that it must extract pyrin localizable
                                     messages as well. defaults to True if not provided.

        :keyword bool include_app: specifies that it must extract application localizable
                                   messages as well. defaults to True if not provided.

        :keyword str locale: locale name of the catalog to compile.
                             it will compile all catalogs if not provided.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """

        self.extract(include_pyrin=include_pyrin, include_app=include_app, locale=locale)
        self.update(locale=locale)
        self.compile(locale=locale)
