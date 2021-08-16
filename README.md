Heroku url: https://fsnd-capstone-weizhi.herokuapp.com/

## How to run tests locally

1. Create a db locally via `createdb castingcouch_test`.
2. Create a file `secret.sh` in repo root directory.
3. Enter environment variables into `secret.sh`.
4. Run command `. ./secret.sh` from repo root directory.
5. Run command `dropdb castingcouch_test && createdb castingcouch_test && python test_casting_couch.py` to test.