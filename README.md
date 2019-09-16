# LetApiRun



**前言**

    个人一个普通的测试人员，一直在从事业务测试和项目管理方面的工作，随着时代的发展，测试这个职业也在快速升级中，更高的要求也在激励着我往更深一层次去发展，锻炼自己开发这个脚本框架目的只有一个，我没有那么高的职业理想，仅仅希望自己不被市场淘汰，也许不完美，但是我努力过，所以基于公司的前后端分离项目为背景，我尝试开发了一套接口测试框架
 
 **框架介绍**
 ####1 框架简介
    本框架是基于py3进行开发，功能方面目前主要解决的是前后端分离框架下的普通http协议的接口相关的测试。
    
 ####2 设计思路
    1. 首先设计的灵感是基于unittest的框架的case管理方式
    2. 其次基于jmeter中的提取器和验证器的设计思路
    3. debugtalk大神的json、yaml的管理方式
    当然（小私心就是锻炼锻炼自己的代码能力，虽然不咋地）

**功能介绍**
    1. 支持全局参数化，
    2. 支持自定义方法
    3. 支持接口的返回验证及结果自动提取
    4. 支持自定义错误异常的收集和返回
    5. 支持命令行模式
    6. 支持api测试报告的自动生成和结果统计
    7. 支持http协议下常用（get， post， patch）

**测试样本**
```
{
   "test": [{
     "name": "login_commuity_with_jack_中文",
     "setupcase": {
       "success": "${__get_value('success')}",
       "abc":123,
       "c":3,
       "d":"anc",
       "fun2":"${__get_value(a=1, b=2)}",
       "username": "jack2",
       "a":"${__get_value(${abc}, ${c}, '${d}')}"
     },

     "requestor":{
        "url": "${host}/fosdga/device-mgr/api/auth/login",
        "method": "POST",
        "headers": {
          "content-type": "application/json"
       },
        "data": { "username": "${username}", "password": "111111"}
     },

     "validator": {
       "assertEqCode": 200,
       "assertEqHeaders": {"Content-Type": "application/json;charset=UTF-8"},
       "assertEqStr": ["100000"],
       "assertEqJson":{"success":true}
     },

     "collector":{
       "json": {"token": "response.data.token"}
     },

     "teardowncase":{
       "clear_cookies": "clearcookies",
       "clearsession": "clearsession",
       "cleartoken": "cleartoken"
     }
   }]
}

简单谈下各部分的意义：
"test": 表示的时当前为一个需要测试的用例或者用例列表
"name": 本次测试用例用例的功能描述
"setupcase": 预设case执行前的预设条件
"requestor": api的主要核心部分
"validator": 检验器，用例case的执行完毕后结构校验
"collector": 收集器，主要针对将结果中重要信息回收给其他用例使用
"teardowncase": 回收，主要是销毁setup中的相关内容，减少垃圾
```

暂不支持：
```
1. 命令行执行单个json文件和批量执行文件夹下的内容
2. 缺少log文件的输出，只能通过控制台查看执行过程
3. 支持的http请求太过于简单需要主流覆盖（get， delete, post, patch，put等）（重要）
4. htmlreport的升级与美化，当前只能查看错误api的记录
5. 用例组织的编排，用例的组织顺序逻辑（重要）
```

