# 文件扫单部署文档

## 〇.环境要求

    Windows 10 Pro
    Python 3.7

## 一.容器配置

### 下载 Docker 镜像

    docker pull puyuantech/traderslink:0.6.19

### 启动容器

    docker run -d -it -p 9000-9007:9000-9007 --name traderslink puyuantech/traderslink:0.6.19

### 进入容器

    docker exec -it traderslink bash

### 修改配置文件

如果需要对外暴露服务，也就是跨机器运行的话，需要更改默认配置:

    在 /shared/etc/config.json 文件中找到 "env_infos",
    将 "env_infos" 中 "env_name" 为 "env1" 所在项的 "public_ip" 改为机器实际 ip (默认为 "127.0.0.1")
    例如:
    {
        ......
        "env_infos": [
            {
                "public_ip": "11.111.111.111",
                "env_name": "env1",
                "private_ip": "127.0.0.1"
            }
        ],
        ......
    }

### 启动 master 和交易路由

    gun start master
    gun start tr -f trade1

## 二.交易网关配置

### 2.1 安装 Python 依赖包

    pip install tlclient==0.6.19
    pip install dbfread

### 2.2 请联系 Puyuan Tech 获取 impl-pytg

    解压 impl-pytg 压缩包

### 2.3 日志文件配置

可以通过配置环境变量 `CONSOLE_LOG_LEVEL` 为 `error`、`warning`、`info`、`debug` 等来查看不同输出级别的控制台 log。(默认为 `error`)

可以通过配置环境变量 `FILE_LOG_LEVEL` 为 `error`、`warning`、`info`、`debug` 等来查看不同输出级别的文件 log。(默认为 `info`)

可以通过配置环境变量 `FILE_LOG_PATH` 来指定文件 log 的存储路径。(默认为 `c:/tmp/linker/log`)

### 2.4 兴业扫单配置

#### 2.4.1 账户配置

在 `impl-pytg/python/gateways/xyzq/tg_xyzq.py` 文件最后

    填入 `account_id`(资金账户) 和 `file_dir`(指令文件目录)。
    指令文件目录要求与扫单程序的指令文件目录一致。

`file_dir` 填写格式为 `'c:\\code\\xyzq'` 或者 `r'c:\code\xyzq'` 或者 `'c:/code/xyzq'`

#### 2.4.2 启动兴业扫单程序，开启指令订单模式

#### 2.4.3 启动兴业交易网关

在 `impl-pytg/python` 目录下执行 `python -m gateways.xyzq.tg_xyzq` 即可。

### 2.5 CATS 扫单配置

#### 2.5.1 账户配置

在 `impl-pytg/python/gateways/cats/tg_cats.py` 文件最后

    填入 `account_type`(账户类型)、`account_id`(账户ID) 和 `file_dir`(指令文件目录)。
    指令文件目录要求与扫单程序的指令文件目录一致。

`file_dir` 填写格式为 `'c:\\code\\cats'` 或者 `r'c:\code\cats'` 或者 `'c:/code/cats'`

#### 2.5.2 启动 CATS 扫单程序，开启 CSV 文件扫单策略

#### 2.5.3 启动 CATS 交易网关

在 `impl-pytg/python` 目录下执行 `python -m gateways.cats.tg_cats` 即可。

### 2.6 QMT 扫单配置

#### 2.6.1 账户配置

在 `impl-pytg/python/gateways/qmt/tg_qmt.py` 文件最后

    填入 `file_dir`(指令文件目录)。
    指令文件目录要求与扫单策略中的指令文件目录一致。

`file_dir` 填写格式为 `'c:\\code\\qmt'` 或者 `r'c:\code\qmt'` 或者 `'c:/code/qmt'`

#### 2.6.2 在 QMT 程序中添加文件扫单策略

请使用 `impl-pytg/resource/FILEORDER_TIMER.py` 作为本程序配套的策略。

在策略文件中的 `init` 函数中

    填入 `ContextInfo.acc_id`(账户ID) 和 `file_dir`(指令文件目录)。

#### 2.6.3 启动 QMT 交易网关

在 `impl-pytg/python` 目录下执行 `python -m gateways.qmt.tg_qmt` 即可。

## 三.注意事项

### 3.1 CATS 多账户配置说明

    CATS 在账户配置中如果配置了多账户的话。
    下单、查持仓、查账户、查全量订单接口中都需要传入参数 sub_account，并且 sub_account 需要是配置的多账户中的一项，否则均会拒单。
    ps: 撤单不需要传入参数 sub_account，只需要传入 order_id 即可。
    ps: 只配置了单账户的话，所有接口均不需要传入参数 sub_account。

### 3.2 CATS 缓存订单数据库配置说明

    CATS 在扫单配置中如果配置了 `cached_orders_path` 字段的话，就会在该数据库中缓存下当前的所有订单，并且在网关重启后也会重新读取缓存的订单。
    ps: 删除 `cached_orders_path` 字段或者值填为空，不会配置缓存订单数据库。

### 3.3 QMT 回报会触发两次推送

    在策略的模型日志 debug 是可以发现 QMT 的回报会被触发两次调用的，时间间隔极短。（可以在写的文件中看到数据有重复）
    所以目前通过更新时间不带毫秒，就能得到两条一模一样的推送，然后去重，在程序中只推送一遍。
    但是像撤单这种，无论撤单成功还是失败都会导致推送多条状态为 已撤/已拒 的订单，并且有时还会隔一段时间就推送一次这些 order，而且由于时间不一样，因此无法去重过滤。

### 3.4 QMT 无撤单反馈

    由于 QMT 文档中没有撤单结果的回调，因此只能通过 order 的状态是否为已撤来判断是否撤单成功。

## 四.测试

在 `impl-pytg/scripts` 目录下配置了一些测试脚本，可以用来测试下单、撤单、查账户、查持仓、查全量订单和查全量成交等。
