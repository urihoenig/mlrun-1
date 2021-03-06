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

from pathlib import Path
import shutil
from copy import deepcopy
from os import environ

here = Path(__file__).absolute().parent
results = here / 'test_results'

shutil.rmtree(results, ignore_errors=True, onerror=None)

rundb_path = f'{results}/rundb'
out_path = f'{results}/out'
root_path = str(Path(here).parent)
examples_path = Path(here).parent.joinpath('examples')
environ['PYTHONPATH'] = root_path
environ['MLRUN_DBPATH'] = rundb_path

Path(f'{results}/kfp').mkdir(parents=True, exist_ok=True)
environ['KFPMETA_OUT_DIR'] = f'{results}/kfp/'


from mlrun.utils import update_in
from mlrun import RunTemplate, RunObject


def tag_test(spec: RunTemplate, name) -> RunTemplate:
    spec = spec.copy()
    spec.metadata.name = name
    spec.metadata.labels['test'] = name
    return spec


def has_secrets():
    return Path('secrets.txt').is_file()


def verify_state(result: RunObject):
    state = result.status.state
    assert state == 'completed', 'wrong state ({}) {}'.format(state, result.status.error)
