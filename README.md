# archlinuxcn-pkgstats

一个基于 access_log 的 Archlinux CN 软件包信息分析器

---

## 原理

通过正则解析 access_log 日志，分析出每个 Archlinux CN 软件包的使用、流行情况

## 支持的镜像源

- https://repo.archlinuxcn.org (official)
- https://mirrors.tuna.tsinghua.edu.cn (tuna-neo tuna-nano)

## 目前提供的服务

### https://build.archlinuxcn.org/grafana/d/LToKLAzMz/pkgstats

一个基于 Grafana 的可视化界面，可以快速查看软件包历史趋势，使用者分布等情况

### https://archlinuxcn-pkgstats.imlonghao.workers.dev/

一个基于 Cloudflare Worker 的 API 接口，能够根据不同的条件统计出请求次数

用法：将参数以 url params 的形式拼在链接后即可

|     参数     |           含义          |         实例        |
|:------------:|:-----------------------:|:-------------------:|
|    timelt    |         时间小于        |      1590680000     |
|    timegt    |         时间大于        |      1590680000     |
|   protocol   |     连接所使用的协议    |        https        |
|    source    |           来源          |      tuna-nano      |
|      ua      | 连接所使用的 User-Agent |     Pacman/1.2.3    |
| address_type |        IP 的类型        |          4          |
|      asn     |        IP 的 ISP        |        133846       |
|     arch     |           架构          |        x86_64       |
|    country   |           国家          |          CN         |
|    region    |     一级行政区 / 省     |        Hubei        |
|     city     |    二级行政区 / 城市    |        Wuhan        |
|     name     |         软件包名        | archlinuxcn-keyring |
|    pkgver    |        软件包版本       |        1.2.3        |
|    pkgrel    |         软件包次        |          1          |

举个例子：查看软件包 `archlinuxcn-keyring` 在 `tuna-nano` 镜像的访问次数

```
https://archlinuxcn-pkgstats.imlonghao.workers.dev/?name=archlinuxcn-keyring&source=tuna-nano
```

## IP 库

本项目中使用到了 [IP2Location Lite](https://lite.ip2location.com) 的 IP 库数据
