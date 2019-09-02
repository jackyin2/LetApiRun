# LetApiRun

**框架设计思路：**

本次的框架设计，当前还处在迭代中， 按照功能完善程度来说，当前为V1.0版本，在设计这块，重点吸取了unittest的case管理模式和jmeter的参数化传递以及组件话的提取器和验证器思路，如果使用过unittest和jmeter的人都知道，jmeter具有很强大的组件库，unittest则给了大家很清晰的case管理方式，结合以上这些的一些各方面的优点，（小私心就是锻炼锻炼自己的代码能力，虽然不咋地）个人考虑开发一套框架用于公司内部后期测试简单api

**使用场景（适用场景简单）：**

http协议 and 前后端分离 and json

使用eg：
```
{
   
   "test": [{
     
     "name": "login_commuity_with_jack",

     "setupcase": {
       "success": "${__get_value('success')}",
       "abc":123,
       "c":3,
       "fun2":"${__get_value(a=1, b=2)}",
       "username": "jack",
       "a":"${__get_value(${abc}, ${c})}"
     },

     "requestor":{
        "url": "${host}/telwoy/device-mgr/api/auth/login",
        "method": "POST",
        "headers": {
          "content-type": "application/json"
       },
     "data": { "username": "${username}", "password": "111111"}
     },

     "validator": {
       "status_code": 200,
       "headers": {"Content-Type": "application/json;charset=UTF-8"},
       "assertEqStr": ["100000"],
       "assertEqJson":{"success":true}
     },

     "collector":{
       "json": {"token": "response.data.token"},
       "methods": {
         "cookie":"${__collect_value(re, 'headers', 'cookie')}"
       }
     },

     "teardowncase":{
       "clear_cookies": "clearcookies",
       "clearsession": "clearsession",
       "cleartoken": "cleartoken"
     }
   }]
}
```

简单谈下各部分的意义：
```
"test": 表示的时当前为一个需要测试的用例或者用例列表
"name": 本次测试用例用例的功能描述
"setupcase": 预设case执行前的预设条件
"requestor": api的主要核心部分
"validator": 检验器，用例case的执行完毕后结构校验
"collector": 收集器，主要针对将结果中重要信息回收给其他用例使用
"teardowncase": 回收，主要是销毁setup中的相关内容，减少垃圾
```
