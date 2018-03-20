# Some tools

## Time of attaching volume to `skip hlu 0`
```
# Collect the time used during attach.
python time_attach_skip_hlu_0.py test 2>&1 | tee attach-modify-hlu-clean.log
# Clean up the attachment of lun.
python time_attach_skip_hlu_0.py clean 2>&1 | tee attach-modify-hlu-clean.log
```
