# Copyright (c) 2015 SUSE Linux GmbH.  All rights reserved.
#
# This file is part of kiwi.
#
# kiwi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# kiwi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kiwi.  If not, see <http://www.gnu.org/licenses/>
#
from tempfile import NamedTemporaryFile

# project
from kiwi.command import Command
from kiwi.defaults import Defaults


class Shell(object):
    """
    **Special character handling for shell evaluated code**
    """
    @classmethod
    def quote(self, message):
        """
        Quote characters which have a special meaning for bash
        but should be used as normal characters. actually I had
        planned to use pipes.quote but it does not quote as I
        had expected it. e.g 'name_wit_a_$' does not quote the $
        so we do it on our own for the scope of kiwi

        :param str message: message text

        :return: quoted text

        :rtype: str
        """
        # \\ quoting must be first in the list
        quote_characters = ['\\', '$', '"', '`', '!']
        for quote in quote_characters:
            message = message.replace(quote, '\\' + quote)
        return message

    @classmethod
    def quote_key_value_file(self, filename):
        """
        Quote given input file which has to be of the form
        key=value to be able to become sourced by the shell

        :param str filename: file path name

        :return: quoted text

        :rtype: str
        """
        temp_copy = NamedTemporaryFile()
        Command.run(['cp', filename, temp_copy.name])
        Shell.run_common_function('baseQuoteFile', [temp_copy.name])
        with open(temp_copy.name) as quoted:
            return quoted.read().splitlines()

    @classmethod
    def run_common_function(self, name, parameters):
        """
        Run a function implemented in config/functions.sh

        :param str name: function name
        :param list parameters: function arguments
        """
        Command.run(
            [
                'bash', '-c',
                'source ' + ''.join(
                    [
                        Defaults.get_common_functions_file(),
                        '; ', name, ' ', ' '.join(parameters)
                    ]
                )
            ]
        )
