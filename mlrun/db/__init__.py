# Copyright 2018 Iguazio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .filedb import FileRunDB
from .base import RunDBInterface, RunDBError  # noqa
from os import environ
from urllib.parse import urlparse


def get_run_db(url=''):
    if not url:
        url = environ.get('MLRUN_META_DBPATH', './')

    p = urlparse(url)
    scheme = p.scheme.lower()
    if '://' not in url or scheme in ['file', 's3', 'v3io', 'v3ios']:
        db = FileRunDB(url)
    else:
        raise ValueError('unsupported run DB scheme ({})'.format(scheme))
    return db
