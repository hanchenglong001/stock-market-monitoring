### 股票盯盘服务

#### 服务说明

```
    该服务是通过开源API行情接口: 新浪;
                    下单接口: 同花顺;
```

- 项目服务入口

* jk.py

#### 启动服务流程

- 获取项目依赖的三方库写入txt文件

* pip freeze > requirements.txt

- 拉取依赖库

* pip install -r requirements.txt