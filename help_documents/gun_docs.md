# user's guide to GUN cmd

## Content

0. [gun help](#0.-gun-help)

0. [gun version](#1.-gun-version)

0. [gun status](#2.-gun-status)

0. [gun runs](#3.-gun-runs)

0. [gun key](#4.-gun-key)

0. [gun encrypt/decrypt](#5.-gun-encrypt/decrypt)

0. [gun account](#6.-gun-account-(configuring-accounts))

0. [gun db](#7.-gun-db-(configuring-db))

0. [gun run](#8.-gun-run)

0. [gun start](#9.-gun-start)

0. [gun config](#10.-gun-config)

0. [gun cmd](#12.-gun-cmd)

0. [gun env](#13.-gun-env)

0. [gun proxy](#14.-gun-proxy)

0. [gun inspect](#15.-gun-inspect)

0. [gun ip](#16.-gun-ip)

0. [gun remote](#17.-gun-remote)

---

## 0. gun help

examples:

    > gun help
    (help info, skipped)

---

## 1. gun version

examples:

    > gun version
    (version info, skipped)

---

## 2. gun status

examples:

    > gun status
    (status info, skipped)

---

## 3. gun runs

run integration tests

(skipped)

---

## 4. gun key

configuring rsa keys

### 4.1 show list of available keys

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

### 4.2 show key detail

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

### 4.3 add key

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

### 4.4 remove key

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

## 5. gun encrypt/decrypt

### 5.1 gun encrypt

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


### 5.2 gun decrypt

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

## 6. gun account (configuring accounts)

### 6.1. adding account config

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

### 6.2 list accounts

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

### 6.3 delete account

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

---

## 7. gun db (configuring db)

### 7.1 create db

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

### 7.2 init db

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

### 7.3 drop db

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

### 7.4 show connection info

required args:

    print
        to print connection info
        usage: print

example:

    > gun db print
    <Database: -h52.79.80.0 -P3306 -uroot -p(hidden) db_core>

---

## 8. gun run

required args:

    [fist type]
        options: master tg mg tr mr oms rms bs algo rr nn

optional args:

    -f --fist_name, fist name
    -g --gateway_name, gateway name, e.g. ctp, huobi
    -a --acc_tag, account name
    -r --router_name, router name for gateway
    -p --package_name, specify python gateway package, e.g. -p cryptofx
    --proxy, use the proxy in config.json

examples:

    > gun run master
    (skipped, master log)

    > gun run tr -f trade1
    (skipped, tr log)

    > gun run mr -f market1
    (skipped, mr log)

    > gun run tg -g huobi -a pyhb -r trade1 -p cryptofx
    (skipped, huobi tg log)


---

## 9. gun start

(daemon version of gun start, skipped)

---

## 10. gun config

optional args:

    -d, --config_dir, config directory, default: /shared/etc/

### 10.1 edit config file

example:

    > gun config
    (skipped, config file opened with text editor)

### 10.2 upgrade config

example:

    > gun config --upgrade
    (skipped, upgrade info)

### 10.3 check config file version

example:

    > gun config --check
    (skipped, check info)

---

## 12. gun cmd

example:

    > gun cmd -f master -c '{"cmd_type":"start_fist", "fist_name": "test1", "fist_type":"TRADE_GATEWAY","run_cmd":"gun start -f test1 -t tg -d -a test -g sim -p cryptofx"}'

---

## 13. gun env

### 13.1 show env info

    > gun env ls
    current env: env3

### 13.2 init env config

    > gun env init --env_name env1 --private_ip 127.0.0.1 --public_ip 127.0.0.1
    [env] set env name "env1"

---

## 14. gun proxy

### 14.1 show proxy info

    > gun proxy ls
    http_proxy: http://127.0.0.1:50032

### 14.2 set proxy

    > gun proxy set --http_proxy http://127.0.0.1:1212
    http_proxy: http://127.0.0.1:1212

---

## 15. gun inspect

1. 获取fist列表：
```
> gun inspect fists
  sid  env    name            type           running      pid  start_time         end_time
-----  -----  --------------  -------------  ---------  -----  -----------------  ----------
    0  env1   master          MASTER         True       29814  20200110-01:40:01  -
    1  env1   market1         MARKET_ROUTER  True       29845  20200110-04:40:04  -
    2  env1   trade1          TRADE_ROUTER   True       29885  20200110-07:40:07  -
    3  env1   trade2          TRADE_ROUTER   True       29934  20200110-12:40:12  -
    4  env1   trade3          TRADE_ROUTER   True       29952  20200110-15:40:15  -
    5  env2   _gun_inspector  -              True       30357  20200110-49:41:49  -
    6  env2   trade4          TRADE_ROUTER   True       30280  20200110-37:41:37  -
    7  env2   trade5          TRADE_ROUTER   True       30298  20200110-41:41:41  -
```


2. fist列表根据env分组：
```
> gun inspect fists -g env
env            sid  name            type           running      pid  start_time         end_time
-----------  -----  --------------  -------------  ---------  -----  -----------------  ----------
group: env1
                 0  master          MASTER         True       29814  20200110-01:40:01  -
                 1  market1         MARKET_ROUTER  True       29845  20200110-04:40:04  -
                 2  trade1          TRADE_ROUTER   True       29885  20200110-07:40:07  -
                 3  trade2          TRADE_ROUTER   True       29934  20200110-12:40:12  -
                 4  trade3          TRADE_ROUTER   True       29952  20200110-15:40:15  -

group: env2
                 5  _gun_inspector  -              True       30372  20200110-55:41:55  -
                 6  trade4          TRADE_ROUTER   True       30280  20200110-37:41:37  -
                 7  trade5          TRADE_ROUTER   True       30298  20200110-41:41:41  -
```


3. fist列表分组后，根据start_time排序
```
> gun inspect fists -g env -s start_time
env            sid  name            type           running      pid  start_time         end_time
-----------  -----  --------------  -------------  ---------  -----  -----------------  ----------
group: env1
                 0  master          MASTER         True       29814  20200110-01:40:01  -
                 1  market1         MARKET_ROUTER  True       29845  20200110-04:40:04  -
                 2  trade1          TRADE_ROUTER   True       29885  20200110-07:40:07  -
                 3  trade2          TRADE_ROUTER   True       29934  20200110-12:40:12  -
                 4  trade3          TRADE_ROUTER   True       29952  20200110-15:40:15  -

group: env2
                 5  _gun_inspector  -              True       30462  20200110-15:42:15  -
                 6  trade4          TRADE_ROUTER   True       30280  20200110-37:41:37  -
                 7  trade5          TRADE_ROUTER   True       30298  20200110-41:41:41  -
```


4. fist列表分组后，根据start_time倒序排列：
```
> gun inspect fists -g env -s start_time -r
env            sid  name            type           running      pid  start_time         end_time
-----------  -----  --------------  -------------  ---------  -----  -----------------  ----------
group: env1
                 4  trade3          TRADE_ROUTER   True       29952  20200110-15:40:15  -
                 3  trade2          TRADE_ROUTER   True       29934  20200110-12:40:12  -
                 2  trade1          TRADE_ROUTER   True       29885  20200110-07:40:07  -
                 1  market1         MARKET_ROUTER  True       29845  20200110-04:40:04  -
                 0  master          MASTER         True       29814  20200110-01:40:01  -

group: env2
                 7  trade5          TRADE_ROUTER   True       30298  20200110-41:41:41  -
                 6  trade4          TRADE_ROUTER   True       30280  20200110-37:41:37  -
                 5  _gun_inspector  -              True       30498  20200110-18:42:18  -
```

---

## 16. gun ip

example:

    > gun ip
    current public ip:  36.112.76.206

---

## 17. gun remote

gun remote命令，可以用来给禁止登录的托管机发送命令，并取回标准输出。

1. 在本地(假设ip地址111.192.86.134)运行dispatcher
```
> gun remote run -s dispatcher
```

2. 在托管机上运行executor（连接到本地111.192.86.134上的dispatcher）
```
> gun remote run -s executor -H 111.192.86.134
```

3. 在本地运行requester
（requester把命令发送到dispatcher，由dispatcher发送到executor执行，执行完后返回output）
```
> gun remote exec -c 'cat master.log' -d 'shared/log'
*********** output ***********
(content of master.log)
```