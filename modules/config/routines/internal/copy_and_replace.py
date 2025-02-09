from typing                 import List
from .parsing               import CopySpec
from .internal.copy_util    import copy
from .internal.replace_util import replace

#log tools is inserted into path before this comes into scope
from log_tools import log, err

"""""""""""""""""""""""""""""""""""""""""""""""""""
copy_configs
  function to perform config copies, with specific
  replacements. 

mode:
  0 for backup, 1 for deploy

copies:
  host_data should be a dictionary returned by
  yaml.safe_load().

host_data:
  copies should be a list of CopySpec objects.

on success:
  returns True
on failure:
  returns False
"""""""""""""""""""""""""""""""""""""""""""""""""""
def copy_configs(mode, copies, host_data, default_data):
    if not isinstance(copies, List):
        err("Provided list of copies is not formatted correctly as CopySpec objects.")
        return False

    for cp in copies:
        if not isinstance(cp, CopySpec):
            err("Copy in list is not CopySpec object.")
            continue
        
        log(f"{cp.from_path} => {cp.to_path}")

        #do the cp
        copy(cp.from_path, cp.to_path) 

        #spec replacements
        for rel_f_path, repl_key, repl_kv, host_key in cp.file_specs:
            replace(mode, rel_f_path, repl_key, repl_kv, host_key, host_data, default_data)

    return True
