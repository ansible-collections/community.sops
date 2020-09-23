## How the tests work

`ansible-test integration --docker ubuntu1804 -v var_sops` essentially executes `runme.sh`. That script does:

1. Make sure it isn't run for Ansible 2.9 (which does not support vars plugins);
2. Use the `setup.yml` playbook to install the requirements (sops);
3. Look at all subdirectories called `test-*`, and for each of them:
   1. Execute the playbook `playbook.yml` in it;
   2. Call `validate.sh` in it with parameters `<exit_code> <path_to_captured_output>`;
   3. If `validate.sh` exists with an exit code not equal to 0, the test has failed.

## Adding more tests

If possible, extend an existing test. If that's not possible, or if you are afraid to pollute one's test environment with more data, create a new one:

1. Create a subdirectory `test-<name_of_your_test>`;
2. Create a `playbook.yml` and `validate.sh` in there (copy from a similar test and adjust);
3. Create subdirectories `group_vars` and/or `host_vars` and fill them as needed.

For creating sops encrypted files, use the private GPG keys from https://raw.githubusercontent.com/mozilla/sops/master/pgp/sops_functional_tests_key.asc. There is a `.sops.yaml` file in this directory which makes sure that sops automatically uses the correct one of the keys provided in that file.
