# user's guide to GUN cmd

## Content

1. [gun key](#4.-gun-key)

2. [gun encrypt/decrypt](#5.-gun-encrypt/decrypt)

3. [gun account](#6.-gun-account-(configuring-accounts))

4. [gun db](#7.-gun-db-(configuring-db))

## 1. gun key

configuring rsa keys

### 1.1 show list of available keys

required args:

    list
        to list all keys
        usage: list

examples:

1. list keys

        > gun key list
        total keys: 2
        1. hcai
        2. default_key

### 1.2 show key detail

required args:

    show
        to show key details
        usage: show

    -k, --key_name
        the key to show
        usage: -k default_key

example:

1. show details of a key

        > gun key show -k hcai
        showing "hcai" keys:

        1. private_key (path: (hidden)):

        (hidden)

        2. public_key (path: /shared/key/hcai.pub):

        -----BEGIN PUBLIC KEY-----
        MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCfP4kKl5//Bzitwypl+g0CrCno
        4kZk76GYtFUp8r+oxS1YH1XrdDIeJdz+3PiHUitFehgZdRANPnx25z+CqF92EKH8
        /PPqW5oWZMALekheE/gEZ3YuCeCRLdAddhH4mOQXFryLuiw1nD7tgp3YCZ7F2jwf
        KDgjQQU8s+j9+LAWRwIDAQAB
        -----END PUBLIC KEY-----

        to save the public key in another location
        please create a file with name "hcai.pub"
        then copy/paste the above public key to the file (including the BEGIN/END lines)

### 1.3 add key

required args:

    new
        to add new key
        usage: new

    -k, --key_name
        the key to add
        usage: -k a_long_key_name

optional args:

    -f, --force
        to replace old key forcibly
        usage: -f

examples:

1. add a key

        > gun key new -k long_key_name
        showing "long_key_name" keys:

        1. private_key (path: (hidden)):

        (hidden)

        2. public_key (path: /shared/key/long_key_name.pub):

        -----BEGIN PUBLIC KEY-----
        MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCuVfvDFW6lGSv7bc4udIigoYBX
        p7FHsR3zS97okGAfMIlqNOfCx6FSVJcS4qXzV68MNiYZ/A3DNd5MLoMIbhGEC41U
        r4UkuTd41o7DnuhA8Pqz/Oz60mQ8J5Hp6S2iC9nTnRSo7FNVmv9gAmxOucF9gNc2
        U5zXXca+KpNh+CvDDwIDAQAB
        -----END PUBLIC KEY-----

        to save the public key in another location
        please create a file with name "long_key_name.pub"
        then copy/paste the above public key to the file (including the BEGIN/END lines)

2. add an existed key (failed)

        > gun key new -k long_key_name
        [warning] skip adding "long_key_name", key already existed
        to overwrite, please specify -f

### 1.4 remove key

required args:

    delete
        to delete a key
        usage: delete

    -k, --key_name
        name of the key to be deleted
        usage: -k key_name

example:

1. delete a key

        > gun key list
        total keys: 3
        1. hcai
        2. long_key_name
        3. default_key

        > gun key delete -k long_key_name
        [info] key "long_key_name" removed

        > gun key list
        total keys: 2
        1. hcai
        2. default_key

---

## 2. gun encrypt/decrypt

### 2.1 gun encrypt

to encrypt data

required args

    data (positional arg)
        data to encrypt
        usage: abcdefg

optional args

    -k, --key_name
        name of the key
        usage: -k key_name

example:

1. encrypt data

        > gun encrypt -k key_name this_is_data
        encrypted data:

        K9e4gSAn11WfmqtkNJdY4


### 2.2 gun decrypt

to decrypt data

required args

    data (positional arg)
        data to decrpt
        usage: K9e4gSAn11WfmqtkNJdY4S6dynxl2

optional args

    -k, --key_name
        name of the key
        usage: -k key_name

example:

1. decrypt data

        > gun decrypt -k key_name K9e4gSAn11WfmqtkNJdY4
        decrypted data:

        this_is_data

---

## 3. gun account (configuring accounts)

### 3.1. adding account config

required args:

    new
        indicate that we would like to add an account
        usage: new

    -a, --acc_tag
        specify the account tag
        usage: -a hcai_test


optional args:

    -k, --key_name
        an arbitrary string used to encrypt data
        do not specify this if the content was not encrypted
        usage: -k key_name

    -c, --content
        other user defined account config keys/valuesd
        note that it is your responsibility to encrypt the sensitive data with the specified key
        keys like "secret_key" and "password" will be automatically decrypted when used
        exmaple: -c key1:value2 key2:value2 key3:value3 ....

examples:

1. add an account

        > gun account new -a hcai_test -k default_key -c access_key:mn8ikls4qg-bcf44c5f-9e78d896-8737e secret_key:13cd22f0-93fd1275-eaebc9da-c0ac0
        done adding account "hcai_test"

        > gun account list
        total accounts: 1
        1. hcai_test
        {
            "access_key": "mn8ikls4qg-bcf44c5f-9e78d896-8737e",
            "secret_key": "13cd22f0-93fd1275-eaebc9da-c0ac0"
        }
        (encrypted with key "default_key")

---

### 3.2 list accounts

required args:

    list
        indicate that we would like to list account infos
        usage: list

exmaple:

1. list all accounts

        > gun account list
        total accounts: 1
        1. hcai_test
        {
            "access_key": "mn8ikls4qg-bcf44c5f-9e78d896-8737e",
            "secret_key": "13cd22f0-93fd1275-eaebc9da-c0ac0"
        }
        (encrypted with key "default_key")

---

### 3.3 delete account

required args:

    delete
        indicate that we would like to delete an account
        usage: -n

    -a, --acc_name
        account to be deleted
        usage: -a hcai_test

example:

    > gun account list
    total accounts: 1
    1. hcai_test
    {
        "access_key": "mn8ikls4qg-bcf44c5f-9e78d896-8737e",
        "secret_key": "13cd22f0-93fd1275-eaebc9da-c0ac0"
    }
    (encrypted with key "default_key")

    > gun account delete -a hcai_test
    to delete account "hcai_test"
    done!

    > gun account list
    total accounts: 0

## 4. gun db (configuring db)

### 4.1 create db

required args:

    create
        to create schema
        usage: create

optional args:

    --db
        schema name, default as "db_core"
        usage: --db db_core

exmaple:

    > gun db create
    creating databse "db_core"
    done!

### 4.2 init db

required args:

    init
        to init schema with tables
        usage: init

optional args:

    --db
        schema name, default as "db_core"
        usage: --db db_core

exmaple:

    > gun db init
    creating tables on db_core...
    done!

### 4.3 drop db

required args:

    drop
        to drop schema
        usage: drop

optional args:

    --db
        schema name, default as "db_core"
        usage: --db db_core

example:

    > gun db drop
    to drop db "db_core"...
    done!

### 4.4 show connection info

required args:

    print
        to print connection info
        usage: print

example:

    > gun db print
    <Database: -h52.79.80.0 -P3306 -uroot -p(hidden) db_core>