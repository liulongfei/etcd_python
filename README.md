~~etcd_python~~  
在 Kubernetes 编排中，使用 ConfigMap 是最佳解决方案。

### 功能

与 `etcd` 交互的脚本

* 普通文本上传；
* 文本文件内容上传，并可以转码为 url 编码；
* 可以获取普通文本数据；
* url 编码获取真实数据，并写入文件；

### 环境说明

* Python2 或 Python3；
* python-etcd 第三方库；

### 使用说明

* `-h` 获取帮助信息；
* `-H` etcd 主机列表，`127.0.0.1:2379` 或 `127.0.0.1:2379,127.0.0.2:2379`；

例如：

`$ python etcd_python.py -H 10.78.170.65:2379 -t put  -k logstash/crmapp.conf -v ./crmapp.conf -e`
